'''
@version: v2.0
'''
from django.db import models
from django import forms
from django.contrib.auth.models import User
from ItemInfo.models import *
#from UserInfo.models import *

class ItemBuyInfo(models.Model):
    '''
    In an order, customer may buy one kind of
    item for more than one piece, so we need this model
    @type item: item field
    @type num: number field
    @type comment: buyer's comment on this item
    '''
    item = models.ForeignKey(ItemInfo)
    num = models.PositiveIntegerField(default=0)
    comment = models.TextField(max_length=256)
#	seller = models.ForeignKey(User)
#	src_address = models.CharField(max_length = 100)

class Order(models.Model):
    '''
    Record an order's all information
    @type buyer: customer field
    @type seller: seller field
    @type items: items field
    @type status: status field
    @type create_time: when order created
    @type pay_time: when order paid
    @type ship_time: when order shipped
    @type arrive_time: when order arrived
    @type complete_time: when order completed
    @type cancel_req_time: when customer ask for refund
    @type close_time: when order closed
    @type comment_time: when order commented
    '''
#	order_id = models.AutoField(primary_key = True)
    buyer = models.ForeignKey(User, related_name='user_0')
    seller = models.ForeignKey(User, related_name='user_1')
    items = models.ManyToManyField(ItemBuyInfo)
    status = models.SmallIntegerField()
    create_time = models.DateTimeField(auto_now_add = True)
    pay_time = models.DateTimeField(null =True,blank = True)
    ship_time = models.DateTimeField(null =True,blank = True)
    arrive_time = models.DateTimeField(null =True,blank = True)
    complete_time = models.DateTimeField(null =True,blank = True)
    cancel_req_time = models.DateTimeField(null =True,blank = True)
    close_time = models.DateTimeField(null =True,blank = True)
    comment_time = models.DateTimeField(null =True,blank = True)
    
    def total(self):
        '''
        @param self:
        @return: the total cost of the cose
        @rtype: positive integer
        '''
        allItem = self.items.all()
        count = 0
        for itemBuyInfo in allItem:
            count += itemBuyInfo.item.price * itemBuyInfo.num
        return count

    def getData(self):
        '''
        get data of one order

        keys of the dict:
         - 'id'
         - 'status'
         - 'items'
         - |---'id'
         - |---'name'
         - |---'price'
         - |---'pic'
         - |---'rating'
         - |---'comment'
         - 'buyer'
         - 'seller'
         - 'create_time'
         - 'pay_time'
         - 'ship_time'
         - 'arrive_time'
         - 'complete_time'
         - 'refund_time'
         - 'comment_time'

        @param self:
        @return: all required information of an order
        @rtype: a dict
        '''
        data = {}
        data['id'] = self.id
        data['status'] = self.status
        items = []
        for itemBuyInfo in self.items.all():
            tempItem = {}
            tempItem['id'] = itemBuyInfo.item.id
            tempItem['name'] = itemBuyInfo.item.name
            tempItem['price'] = itemBuyInfo.item.price
            tempItem['num'] = itemBuyInfo.num
            tempItem['pic'] = itemBuyInfo.item.pic
            tempItem['rating'] = itemBuyInfo.item.rating
            tempItem['comment'] = itemBuyInfo.comment
            items.append(tempItem)
        data['items'] = items
        data['buyer'] = self.buyer.username
        #data['buyer_addr'] = AccountInfo.objects.get(user=buyer).address
        data['seller'] = self.seller.username
        #data['seller_addr'] = AccountInfo.objects.get(user=seller_addr).address
        g = lambda x : x and x.strftime("%Y-%m-%d %X") or None
        data['create_time'] = g(self.create_time)
        data['pay_time'] = g(self.pay_time)
        data['ship_time'] = g(self.ship_time)
        data['arrive_time'] = g(self.arrive_time)
        data['complete_time'] = g(self.complete_time)
        data['refund_time'] = g(self.cancel_req_time)
        data['close_time'] = g(self.close_time)
        data['comment_time'] = g(self.comment_time)
        return data
