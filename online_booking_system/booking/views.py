# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the page is produced
'''  
from booking.forms import flightForm,hotelForm
from booking.data import  COMPANY_CHOICES
from booking.models import company, city, flight, flight_discount, hotel,room_num, room_discount, flight_record, hotel_record
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
import json
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


# 这是预订某个酒店各种类型房间的页面，同时会显示其他人对这次预订的看法
@login_required
def pay_hotel(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for last ensuring of the hotel booking
    this require login
    and also you can see diffrent option for searching.
    you can see other's idea of the hotel
    '''


    hr = hotel_record.objects.get(pk=pk_id)
    if(hr.stat=='1'):
        messages.add_message(request, messages.INFO, 'You have payed it already!')
        return HttpResponseRedirect(request.url)
    if 'application/json' in request.META.get('CONTENT_TYPE'):
        if request.POST.get('post') == 'yes':
            hr.stat = '1'
            hr.save()    
        return HttpResponseRedirect(request.url)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)               
            if(data['post']=='yes'):
                hr.stat = '1'
                hr.save()
            string = "<title>302 Found</title>Resource has been modified.\n"
            response = HttpResponse(string,status=302,)
            response['Location'] = request.url
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
                
            return response
        except ValueError as e:
            string =u" "
            string += str(e)
            string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
            response = HttpResponse(string,status=400,)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
            return response         

    
    
    return render_to_response('payment_hotel.html', {'rs':hr, }, context_instance=RequestContext(request))

# 这是预订某个酒店各种类型房间的页面，同时会显示其他人对这次预订的看法
@login_required
def pay_flight(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for last ensuring of the hotel booking
    this require login
    and also you can see diffrent option for searching.
    you can see other's idea of the hotel
    '''


    fr = flight_record.objects.get(pk=pk_id)
    if(fr.stat=='1'):
        messages.add_message(request, messages.INFO, 'You have payed it already!')
        return HttpResponseRedirect(request.url)
    if 'application/json' in request.META.get('CONTENT_TYPE'):
        if request.POST.get('post') == 'yes':
            fr.stat = '1'
            fr.save()    
        return HttpResponseRedirect(request.url)
        
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)               
            if(data['post']=='yes'):
                fr.stat = '1'
                fr.save()
            string = "<title>302 Found</title>Resource has been modified.\n"
            response = HttpResponse(string,status=302,)
            response['Location'] = request.url
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
                
            return response
        except ValueError as e:
            string =u" "
            string += str(e)
            string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
            response = HttpResponse(string,status=400,)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
            return response         

    
    
    return render_to_response('payment_hotel.html', {'rs':fr, }, context_instance=RequestContext(request))


# 这是查询自己的所有航班预订记录的页面，以列表方式列出，同时做了分页处理
@login_required
def my_flight_record(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing all my flight record
    you can see all your booking items
    '''
    frs = flight_record.objects.filter(user_id=request.user)
    paginator = Paginator(frs, 10)
    page = request.GET.get('p', '1')
    try:
        fr = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fr = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fr = paginator.page(paginator.num_pages)
    
    if request.method == 'GET' and 'application/json' in request.META.get('HTTP_ACCEPT'):
        dlist = []
        for r in fr:
            data = model_to_dict(r)
            data['book_date'] = data.get('book_date').strftime('%Y-%m-%d')
            data['book_time'] = data.get('book_time').strftime('%H:%M:%S')
            #assert False
            dlist.append(data)
        dlist.append({'p':fr.number,'all':fr.paginator.num_pages})
        encodeData = json.dumps(dlist,sort_keys=True,indent=2)
        return HttpResponse(encodeData, content_type="application/json")
    else:
        return render_to_response('show_fr.html', {'rs':fr,}, \
                                  context_instance=RequestContext(request))
# 这是查询自己的所有酒店预订记录的页面，以列表方式列出，同时做了分页处理
@login_required
def my_hotel_record(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing all my hotel record
    you can see all your booking items
    '''
    hrs = hotel_record.objects.filter(user_id=request.user)
    
    paginator = Paginator(hrs, 10)
    page = request.GET.get('p', '1')
    try:
        hr = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        hr = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        hr = paginator.page(paginator.num_pages)
    
    if request.method == 'GET' and 'application/json' in request.META.get('HTTP_ACCEPT'):
        dlist = []
        for r in hr:
            data = model_to_dict(r)
            data['book_date'] = data.get('book_date').strftime('%Y-%m-%d')
            data['checkin_date'] = data.get('checkin_date').strftime('%Y-%m-%d')
            data['book_time'] = data.get('book_time').strftime('%H:%M:%S')
            #assert False
            dlist.append(data)
        dlist.append({'p':hr.number,'all':hr.paginator.num_pages})
        encodeData = json.dumps(dlist,sort_keys=True,indent=2)
        return HttpResponse(encodeData, content_type="application/json")
    else:
        return render_to_response('show_hr.html', {'rs':hr,}, \
                                  context_instance=RequestContext(request))
# 这是查询自己的具体航班预订记录的页面，同时可以填写评分和评论
@login_required
def flight_record_view(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing the seleted one flight record
    you can make comment for the item of flight
    '''
    try:
        fr = flight_record.objects.get(pk=pk_id)
        if fr.scores!=-1:
            messages.add_message(request, messages.INFO, 'this record has already been scored. It can\'t been scored again!')
            return HttpResponseRedirect('/booking/my_record/flight/') 
        if fr.flight_id.arrive_date >= (datetime.date.today()):
            messages.add_message(request, messages.INFO, 'You have not experienced the flight yet, go back after that!')
            return HttpResponseRedirect('/booking/my_record/flight/') 
        if request.method == 'POST':
            fr.comment = request.POST.get('comment')
            fr.scores = request.POST.get('score')
            fr.save()
            return HttpResponseRedirect('/booking/my_record/flight/')
        elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads( request.body)
                fr.comment = data['comment']
                fr.scores = data['score']
                fr.save()
                string = "<title>302 Found</title>Resource has been modified.\n"
                response = HttpResponse(string,status=302,)
                response['Location'] = '/booking/my_record/flight/'
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response
            except ValueError:
                string = "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                
                return response
        else:    
            return render_to_response('fr_detail.html', {'fr':fr, }, \
                                      context_instance=RequestContext(request))
    except flight_record.DoesNotExist:
        raise Http404


@login_required
def hotel_record_view(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing the seleted one hotel record
    you can make comment for the item of hotel
    '''
    try:
        hr = hotel_record.objects.get(pk=pk_id)
        if hr.scores!=-1:
            messages.add_message(request, messages.INFO, 'this record has already been scored. It can\'t been scored again!')
            return HttpResponseRedirect('/booking/my_record/hotel/') 
        if hr.checkin_date >= (datetime.date.today()-datetime.timedelta(days=hr.num)):
            messages.add_message(request, messages.INFO, 'You have not experienced the hotel yet, go back after that!')
            return HttpResponseRedirect('/booking/my_record/hotel/') 
        if request.method == 'POST':
                
                hr.comment = request.POST.get('comment')
                hr.scores = (int)(request.POST.get('score'))
                hr.save()
                
                f = hr.hotel_id
                new_num = f.commented_num+1
                if f.scores==-1:
                    f.scores = hr.scores
                else:
                    f.scores = (f.scores*f.commented_num+hr.scores)/new_num
                f.commented_num = new_num
                f.save()
                return HttpResponseRedirect('/booking/my_record/hotel/')    
        elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
                try:
                    data = json.loads( request.body)
                    hr.comment = data['comment']
                    hr.scores = int(data['score'])
                    hr.save()
                    
                    f = hr.hotel_id
                    new_num = f.commented_num+1
                    if f.scores==-1:
                        f.scores = hr.scores
                    else:
                        f.scores = (f.scores*f.commented_num+hr.scores)/new_num
                    f.commented_num = new_num
                    f.save()
                
                    string = "<title>302 Found</title>Resource has been modified.\n"
                    response = HttpResponse(string,status=302,)
                    response['Location'] = '/booking/my_record/hotel/'
                    response['Vary'] = 'Accept-Encoding'
                    response['Content-Length'] = len(string)
                    return response
                except ValueError:
                    string = "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
                    response = HttpResponse(string,status=400,)
                    response['Vary'] = 'Accept-Encoding'
                    response['Content-Length'] = len(string)
                    
                    return response
        else:
            return render_to_response('hr_detail.html', {'hr':hr, }, \
                                          context_instance=RequestContext(request))
    except hotel_record.DoesNotExist:
        raise Http404

# 这是预订某个酒店各种类型房间的页面，同时会显示其他人对这次预订的看法
@login_required
def book_hotel(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for last ensuring of the hotel booking
    this require login
    and also you can see diffrent option for searching.
    you can see other's idea of the hotel
    '''

    h = hotel.objects.get(pk=pk_id)
    start = request.session.get('start')
    
    if start!=None:
        if(type(start)==type(u'dd')):
            start_day = datetime.datetime.strptime(start,'%Y-%m-%d').date()
        else:
            start_day = start #datetime.datetime.strptime(start,'%Y-%M-%d').date()
        #assert False
    else:
        start_day = datetime.date.today()
    last = int(request.session.get('last','1'))
    last_day = datetime.timedelta(days=last)
    end = start_day+last_day
    rs = room_num.objects.filter(hotel_id=h).filter(date__lt=end).filter(date__gte=start_day)
    
    if len(rs)==0:
        messages.add_message(request, messages.INFO, 'hotel room number from {} to {} not enough!'.format(start_day,end))
        return HttpResponseRedirect('/booking/hotel/') 
    if request.method == 'POST':
        if request.POST.get('post') == 'yes':
            num = int(request.POST.get('num','1'))
            if num<=0:
                messages.add_message(request, messages.INFO, 'hotel room number invalid!')
                return HttpResponseRedirect('/booking/hotel/{}/'.format(pk_id)) 
            for r in rs:
                if(r.room_number < num):
                    messages.add_message(request, messages.INFO, 'hotel room number at {} not enough!'.format(r.date))
                    return HttpResponseRedirect('/booking/hotel/{}/'.format(pk_id)) 
                        
                        
            for r in rs:
                r.room_number = r.room_number - num
                r.save()
            price = num*int(last)*h.price
            hr = hotel_record.objects.create(\
                user_id=request.user, checkin_date = start_day,\
                num = num,last = last,hotel_id=h, book_date=datetime.date.today(), \
                book_time=datetime.datetime.now().time(),
                price = price)
            hr.save()
                    
            h.hot_level = h.hot_level+1
                
            h.save()
                
            return HttpResponseRedirect('/booking/my_record/hotel/')
        
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
        try:
            data = json.loads(request.body)               
            num = int(data.get('num','1'))
            if num<=0:
                string =u" "
                string += "<title>400, hotel room number invalid!\n"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response
            for r in rs:
                if(r.room_number < num):
                    messages.add_message(request, messages.INFO, )
                    string =u" "
                    string += "<title>400,hotel room number at {} not enough!".format(r.date)
                    response = HttpResponse(string,status=400,)
                    response['Vary'] = 'Accept-Encoding'
                    response['Content-Length'] = len(string)
                    return response
                        
                        
            for r in rs:
                r.room_number = r.room_number - num
                r.save()
            hr = hotel_record.objects.create(user_id=request.user, checkin_date = start_day,num = num,last = last,hotel_id=h, book_date=datetime.date.today(), book_time=datetime.datetime.now().time())
            hr.save()
                    
            h.hot_level = h.hot_level+1
                
            h.save()
            string = "<title>302 Found</title>Resource has been modified.\n"
            response = HttpResponse(string,status=302,)
            response['Location'] = '/booking/my_record/hotel/{}/'.format(hr.pk)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
                
            return response
        except ValueError as e:
            string =u" "
            string += str(e)
            string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
            response = HttpResponse(string,status=400,)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
            return response         

    
    sr = hotel_record.objects.filter(hotel_id=h)
    paginator = Paginator(sr, 10)
    page = request.GET.get('p', '1')
    try:
        gg = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gg = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gg = paginator.page(paginator.num_pages)
    return render_to_response('ensure_hotel.html', {'rs':rs, 'h':h, 'sr':gg}, context_instance=RequestContext(request))

@login_required
def book_flight(request, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for last ensuring of the flight booking
    this require login
    and also you can see diffrent option for searching.
    you can see other's idea of the flight
    '''
    
    f = flight.objects.get(pk=pk_id)
    if request.method == 'POST':
        if request.POST.get('post') == 'yes':
            num = int(request.POST.get('num',1))
            if num<=0:
                messages.add_message(request, messages.INFO, 'flight room number invalid!')
                return HttpResponseRedirect('/booking/flight/{}/'.format(pk_id)) 
            if(f.leave_number < num):
                messages.add_message(request, messages.INFO, 'There is no such ticket to book')
                return HttpResponseRedirect('/booking/flight/{}/'.format(pk_id))
            
            f.leave_number = f.leave_number -int(num)
            
            fr = flight_record.objects.create(user_id=request.user, \
                flight_id=f, num=num, book_date=datetime.date.today(), \
                book_time=datetime.datetime.now().time(),stat='0')
            fr.save()
            f.save()
            return HttpResponseRedirect('/booking/my_record/flight/')
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
        try:
            data = json.loads(request.body)               
            num = int(data.get('num','1'))
            if num<=0:
                string =u" "
                string += "<title>400, hotel room number invalid!\n"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response
            if(f.leave_number < num):
                string =u" "
                string += "<title>400,There is no such ticket to book"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response

            f.leave_number = f.leave_number -int(num)
            price = num*f.price
            fr = flight_record.objects.create(user_id=request.user, \
                flight_id=f, num=num, book_date=datetime.date.today(), \
                book_time=datetime.datetime.now().time(),stat='0',price= price)
            fr.save()
            f.save()
            string = "<title>302 Found</title>Resource has been modified.\n"
            response = HttpResponse(string,status=302,)
            response['Location'] = '/booking/my_record/flight/{}/'.format(fr.pk)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
                
            return response
        except ValueError as e:
            string =u" "
            string += str(e)
            string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
            response = HttpResponse(string,status=400,)
            response['Vary'] = 'Accept-Encoding'
            response['Content-Length'] = len(string)
            return response         

        
    sr = flight_record.objects.filter(flight_id=f.id)  
    paginator = Paginator(sr, 10)
    page = request.GET.get('p', '1')
    try:
        gg = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gg = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gg = paginator.page(paginator.num_pages)
    return render_to_response('ensure_flight.html', {'f':f, 'sr':gg}, context_instance=RequestContext(request))
# 这是搜索航班的页面 
@login_required
def search_flight(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for searching the flight infomation
    this require no login
    '''
    if request.method == 'POST':
        form = flightForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            
            messages.add_message(request, messages.INFO, 'form invalid')
            return render_to_response('search_flight.html', { 'form':form}, context_instance=RequestContext(request))
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads(request.body)
            except ValueError as e:
                string =u" "
                string += str(e)
                string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response    
    else:
            form = flightForm()
            return render_to_response('search_flight.html', { 'form':form}, context_instance=RequestContext(request))
    g = flight.objects.filter(starting_id=(city.objects.get(name=data['start'])))
                
    g = g.filter(destination_id=(city.objects.get(name=data['des'])))
    date = data['date']
                
    g = g.filter(leave_date=date)
                
    if data['non_stop'] != '0':
        g = g.filter(none_stop=False if data['non_stop'] == 1 else True)
    if data['level'] != '0':
        g = g.filter(plane_type=data['level'])
    if data['company'] != '0':
        g = g.filter(company_id=company.objects.get(name=COMPANY_CHOICES[int(data['company'])][1]))
    if data['I_or_D'] != '0' and data['sort_by'] != '0':
        if data['I_or_D'] == '1':
            g = g.order_by(data['sort_by'])
        else:
            g = g.order_by('-' + data['sort_by'])
                
                
    paginator = Paginator(g, 10)
    page = request.GET.get('p', '1')
    try:
        gg = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gg = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gg = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        return render_to_response('search_flight.html', { 'form':form,'rs':gg}, context_instance=RequestContext(request))
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
        dlist = []
        for r in gg:
            data = model_to_dict(r)
            data['leave_date'] = data.get('leave_date').strftime('%Y-%m-%d')
            data['leave_time'] = data.get('leave_time').strftime('%H:%M:%S')
            data['arrive_date'] = data.get('arrive_date').strftime('%Y-%m-%d')
            data['arrive_time'] = data.get('arrive_time').strftime('%H:%M:%S')
            data['starting_id'] = city.objects.get(pk=data.get('starting_id')).name
            data['destination_id'] = city.objects.get(pk=data.get('destination_id')).name
            
            #assert False
            dlist.append(data)
        dlist.append({'p':gg.number,'all':gg.paginator.num_pages})
        encodeData = json.dumps(dlist,sort_keys=True,indent=2)
        return HttpResponse(encodeData, content_type="application/json")
@login_required
def search_hotel(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for searching the hotel infomation
    this require no login
    '''
    if request.method == 'POST':
        form = hotelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            messages.add_message(request, messages.INFO, 'form invalid')
            return render_to_response('search_hotel.html', {'form':form }, context_instance=RequestContext(request))
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
            try:
                data = json.loads(request.body)
            except ValueError as e:
                string =u" "
                string += str(e)
                string += "<title>400 Bad Request</title>Badly-formed JSON sent.\n"
                response = HttpResponse(string,status=400,)
                response['Vary'] = 'Accept-Encoding'
                response['Content-Length'] = len(string)
                return response    
    else:
        form = hotelForm()
        return render_to_response('search_hotel.html', {'form':form }, context_instance=RequestContext(request)) 
    c = city.objects.get(name=data['city'])
    g = hotel.objects.filter(city_id=c)
                
    if data['keyword'] != '':
        g = g.filter(name__contains=data['keyword'])
    if data['star'] != '0':
        g = g.filter(hotel_star=data['star'])
    if data['room_type'] != '0':
        g = g.filter(room_type=data['room_type'])
    if data['I_or_D'] != '0' and data['sort_by'] != '0':
        if data['I_or_D'] == '1':
            g = g.order_by(data['sort_by'])
        else:
            g = g.order_by('-' + data['sort_by'])
    request.session['start'] = data['start']
    request.session['last'] = data['last']
                
    paginator = Paginator(g, 10)
    page = request.GET.get('p', '1')
    try:
        gg = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        gg = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        gg = paginator.page(paginator.num_pages)

    if request.method == 'POST':            
        return render_to_response('search_hotel.html', { 'form':form,'rs':gg, }, context_instance=RequestContext(request))
    elif request.method == 'PUT' and 'application/json' in request.META.get('CONTENT_TYPE'):
        dlist = []
        for r in gg:
            data = model_to_dict(r)
            data['city_id'] = city.objects.get(pk=data.get('city_id')).name
            #assert False
            dlist.append(data)
        dlist.append({'p':gg.number,'all':gg.paginator.num_pages})
        encodeData = json.dumps(dlist,sort_keys=True,indent=2)
        return HttpResponse(encodeData, content_type="application/json")
        
    

def index(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for the main page of the site
    this also shows the discount infomation
    '''
    hds = room_discount.objects.all()
    fds = flight_discount.objects.all()
    
    p1 = request.GET.get('p1', '1')
    paginator1 = Paginator(hds, 10)
    try:
        g1 = paginator1.page(p1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        g1 = paginator1.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        g1 = paginator1.page(paginator1.num_pages)
    
    p2 = request.GET.get('p2', '1')
    paginator2 = Paginator(fds, 10)
    try:
        g2 = paginator2.page(p2)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        g2 = paginator2.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        g2 = paginator2.page(paginator2.num_pages)
    if request.method == 'GET' and 'application/json' in request.META.get('HTTP_ACCEPT'):
        dlist = []
        d1 = []
        d2 = []
        for r in g1:
            data = model_to_dict(r)
            d1.append(data)
        for r in g2:
            data = model_to_dict(r)
            d2.append(data)
        dlist.append(d1)
        dlist.append(d2)
        dlist.append({'p1':g1.number,'all1':g1.paginator.num_pages,'p2':g2.number,'all2':g2.paginator.num_pages})
        encodeData = json.dumps(dlist,sort_keys=True,indent=2)
        return HttpResponse(encodeData, content_type="application/json")
    else:
        return render_to_response('index.html', \
        {"hls": g1, "fls":g2,},\
        context_instance=RequestContext(request))

