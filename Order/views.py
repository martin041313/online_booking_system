# encoding=UTF-8
'''
@version: v2.0
'''
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.contrib.auth import authenticate

from datetime import *
from decimal import *

from userena.models import UserenaSignup, AccountInfo, payDetail
from Order.models import *
from Order.forms import *
from ItemInfo.models import *
from Order.status import *
from Order.encoder import *

@login_required
def viewCreateOrder(request):
    '''
    API: to create an order

    First get the POST request's data,
    check the data if is valid. If valid,
    for the same seller, we create an order and add the items into the order.
    That is to say, if the customer wants to buy some items from different seller,
    we will create more than one order.
    One order should have only one seller's address.

    When adding items into the order, the stock of such item will decrease.
    @param request: Django view request with POST method
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''
    print request.POST
    if request.method == 'POST':
        user = request.user
        itemIdList = request.POST.getlist('item_list')
        if len(itemIdList) == 0:
            request.session["create_error"] = u'不能创建空订单'
            return HttpResponseRedirect('/items/')

        num = {}
        for i in itemIdList:
            itemInfo = ItemInfo.objects.get(id=i)
            numTarget = 'num-'+str(i)
            try:
                num[i] = int(request.POST[numTarget])
                if num[i] > itemInfo.stock:
                    raise ValueError
            except ValueError:
                request.session["create_error"] = u'不合法的商品数量'
                return HttpResponseRedirect('/items/')


        seller = None
        for i in itemIdList:
            itemInfo = ItemInfo.objects.get(id=i)
            if itemInfo.seller != seller:
                seller = itemInfo.seller
                newOrder = Order(buyer=user, seller=seller, status=ORDER_UNPAID)
                newOrder.save()
            temp = ItemBuyInfo(item=itemInfo, num=num[i])
            itemInfo.stock -= num[i]
            temp.save()
            itemInfo.save()
            newOrder.items.add(temp)
        return HttpResponseRedirect("/order/")
    else:
        return HttpResponse("create failed, use POST method")

@login_required
def viewMyOrder(request):
    '''
    display the customer or the seller's order.
    @param request: Django view request
    @return: HttpResponse containing the user's all order
    @rtype: Django HttpResponse
    '''
    context = {}
    if 'operate_error' in request.session:
        del request.session['operate_error']
        context['error'] = u'非法的订单操作'
    if 'balance_error' in request.session:
        del request.session['balance_error']
        context['error'] = u'您的余额不足'
    if 'success' in request.session:
        context['success'] = request.session['success']
        del request.session['success']

    if 'application/json' in request.META['HTTP_ACCEPT']:
        return viewAllOrderJSON(request)

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)
    orders = Order.objects.filter(buyer=user).order_by('-id')
    seller_orders = Order.objects.filter(seller=user).order_by('-id')

    context['user'] = user
    context['info'] = userInfo
    context['orders'] = orders
    context['seller_orders'] = seller_orders
    return render_to_response('order/orders.html', context, context_instance=RequestContext(request))

@login_required
def viewAllOrderJSON(request):
    '''
    display the customer or the seller's order using JSON data format.
    @param request: Django view request
    @return: HttpResponse of type "application/json"
    @rtype: Django HttpResponse
    '''
    user = request.user
    
    orders = [order.getData() for order in Order.objects.filter(buyer=user)]
    seller_orders = [ order.getData() for order in Order.objects.filter(seller=user)]
    return HttpResponse(
            getJson(buyer_orders=orders, seller_orders=seller_orders),
            content_type="application/json")

# All the following functions are used to change order status
# Some priviledge check is needed!

@login_required
def viewOneOrderJSON(request, orderId):
    '''
    display the customer or the seller's one specified order using JSON data format.
    @param request: Django view request
    @return: HttpResponse of type "application/json"
    @rtype: Django HttpResponse
    '''
    user = request.user
    try:
        order = Order.objects.get(id=orderId)
        if order.buyer != user and order.seller != user:
            raise ValueError
    except Exception:
        error = "invalid request"
        return HttpResponse(getJson(error=error), content_type="application/json")

    return HttpResponse(getJson(order=order.getData()), content_type="application/json")

@login_required
def viewCancel(request, orderId):
    '''
    API cancel an order

    Before the order is paid, customer can cancel this order.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''
    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_UNPAID:
            raise ValueError
        if order.buyer != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    items = order.items.all()
    for itemBuyInfo in items:
        itemBuyInfo.item.stock += itemBuyInfo.num
        itemBuyInfo.item.save()

    order.status = ORDER_CLOSED
    order.close_time = datetime.now()
    order.save()

    request.session['success'] = u'订单已取消'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewPay(request, orderId):
    '''
    API pay an order

    Before the order is paid, customer can pay this order.

    1.Check the order id
    2.Check the order's status
    3.Check the user
    4.Check the user's balance

    if all check succeed, process the request
    @note: the customer's balance will have a cost
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_UNPAID:
            raise ValueError
        if order.buyer != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    if userInfo.balance < order.total():
        request.session['balance_error'] = True
        return HttpResponseRedirect('/order/')

    userInfo.balance -= Decimal(order.total())
    userInfo.pay(Decimal(order.total()), "This is a brief")
    order.status = ORDER_PAID
    order.pay_time = datetime.now()

    userInfo.save()
    order.save()

    request.session['success'] = u'付款成功'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewShip(request, orderId):
    '''
    API ship an order

    After the order is paid, seller can ship the items.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_PAID:
            raise ValueError
        if order.seller != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    order.status = ORDER_SHIPPING
    order.ship_time = datetime.now()
    order.save()

    request.session['success'] = u'订单已发货'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewArrive(request, orderId):
    '''
    API mark the order arrived

    After the order is shipped, customer can mark the order arrived.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_SHIPPING:
            raise ValueError
        if order.buyer != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    order.status = ORDER_ARRIVE
    order.arrive_time = datetime.now()
    order.save()

    request.session['success'] = u'订单已查收'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewComplete(request, orderId):
    '''
    API complete an order

    After the order is arrived, customer can complete this order.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @note: the seller should receive the money
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_ARRIVE:
            raise ValueError
        if order.buyer != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    sellerInfo = AccountInfo.objects.get(user=order.seller)
    sellerInfo.balance += Decimal(order.total())

    order.status = ORDER_COMPLETED
    order.complete_time = datetime.now()

    sellerInfo.save()
    order.save()

    request.session['success'] = u'订单已完成'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewRefund(request, orderId):
    '''
    API request for refund

    After the order is arrived, customer can request for refund.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_ARRIVE:
            raise ValueError
        if order.buyer != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    order.status = ORDER_REFUND_PENDING
    order.cancel_req_time = datetime.now()
    order.save()

    request.session['success'] = u'退款申请已提交'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewClose(request, orderId):
    '''
    API close an order

    After the order is in refund pending status, seller can close the order.

    1.Check the order id
    2.Check the order's status
    3.Check the user

    if all check succeed, process the request
    @note: the money should be returned to customer
    @note: the stock of items should be returned to original one
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_REFUND_PENDING:
            raise ValueError
        if order.seller != user:
            raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    items = order.items.all()
    for itemBuyInfo in items:
        itemBuyInfo.item.stock += itemBuyInfo.num
        itemBuyInfo.item.save()

    buyerInfo = AccountInfo.objects.get(user=order.buyer)
    buyerInfo.balance += order.total()

    order.status = ORDER_CLOSED
    order.close_time = datetime.now()

    buyerInfo.save()
    order.save()

    request.session['success'] = u'交易关闭'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')

@login_required
def viewComment(request, orderId):
    '''
    API make comments

    After the order is in complete status, buyer can comment on items.

    1.Check the order id
    2.Check the order's status
    3.Chcek the request method
    4.Check the user

    if all check succeed, process the request
    @note: rating will be the new average of all ratings
    @note: rating_count plus 1
    @param request: Django view request
    @param orderId: the order's id in database
    @type orderId: unsigned integer
    @return: HttpResponse, if failed there will be an error in session
    @rtype: Django HttpResponse
    '''

    user = request.user
    userInfo = AccountInfo.objects.get(user=user)

    print request.POST

    try:
        order = Order.objects.get(id=orderId)
        if order.status != ORDER_COMPLETED:
            raise ValueError
        if order.buyer != user:
            raise ValueError
        if request.method != 'POST':
            raise ValueError
        for itemBuyInfo in order.items.all():
            score = float(request.POST['score'+str(itemBuyInfo.item.id)])
            if score < 0 or score > 5:
                raise ValueError
    except Exception:
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponse(getJson(is_success=0), 'application/json')
        request.session['operate_error'] = True
        return HttpResponseRedirect('/order/')

    for itemBuyInfo in order.items.all():
        item = itemBuyInfo.item
        i = item.id
        score = float(request.POST['score'+str(i)])
        comment = request.POST['comment'+str(i)]
        itemBuyInfo.comment = comment
        item.rating = (item.rating * item.rating_count + score) / (item.rating_count + 1)
        item.rating_count += 1

        itemBuyInfo.save()
        item.save()

    order.status = ORDER_COMMENTED
    order.comment_time = datetime.now()
    order.save()

    request.session['success'] = u'商品已评价'
    if 'application/json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(getJson(is_success=1), 'application/json')
    return HttpResponseRedirect('/order/')


