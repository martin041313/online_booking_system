# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the admin page is processed
'''  
from adminInfo.forms import UploadFileForm
from booking.models import company, city, flight, flight_discount, \
    hotel, room_num, room_discount, flight_record, hotel_record
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
# 检查用户是否已经登录，并且是管理员
def is_admin(user):
    '''
    @param user: the user object
    @return: bool true or false
    it tells whether the user is admin user
    '''
    return user.is_authenticated() and user.is_staff
def is_valid_what_type(typeWant):
    '''
    @param typeWant: the data type 
    @return: bool true or false
    it tells whether type is one of this:
    [company ,city ,flight ,flight_discount ,hotel ,room_num ,room_discount ,flight_record ,hotel_record ,User]
    '''
    if  typeWant in [company , city , flight , flight_discount , hotel , room_num , room_discount , flight_record , hotel_record , User]:
        return True
    else:
        return False
# 下面的所有页面均需管理员权限
@user_passes_test(is_admin, login_url="/accounts/login/")
def index(request):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing all my admin things
    you can see all your data
    '''
    return render_to_response('sys_index.html', {}, context_instance=RequestContext(request))
# 显示某个表的所有行
@user_passes_test(is_admin, login_url="/accounts/login/")
def show(request, what):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for showing one of the admin things
    you can see all your data of what type
    '''
    typeWant = globals().get(what)
    if is_valid_what_type(typeWant):
        rs = typeWant.objects.all()
        paginator = Paginator(rs, 10)
        page = request.GET.get('p', '1')
        try:
            gg = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            gg = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            gg = paginator.page(paginator.num_pages)
               
        return render_to_response('show.html', {'what':what, 'rs':gg, }, context_instance=RequestContext(request))
    else:
        raise Http404
# 编辑某个表的行
@user_passes_test(is_admin, login_url="/accounts/login/")
def edit(request, what, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for editing one of the admin things
    you can edit  all your data of what type
    '''
    typeWant = globals().get(what)
    if is_valid_what_type(typeWant):
        class rsForm(ModelForm):
                class Meta:
                    model = typeWant
        r = typeWant.objects.get(pk=pk_id)
        if request.method == 'POST':
            form = rsForm(request.POST)
            if form.is_valid():
                names = typeWant.objects.model._meta.get_all_field_names()
                for i in range(0, len(names)):
                    if(names[i] != u'id'):
                        r.__dict__[names[i]] = form.cleaned_data[names[i]]              
                r.save()
                return HttpResponseRedirect('/sys/{}/{}/'.format(what, r.pk))
        
            
        form = rsForm(model_to_dict(r))
        return render_to_response('edit.html', {'what':what, 'form':form, 'pk_id':pk_id}, \
                                      context_instance=RequestContext(request))
    else:
        raise Http404
# 给某个表新增一行
@user_passes_test(is_admin, login_url="/accounts/login/")
def add(request, what):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for adding one of one of the admin things
    you can add one of all your data of what type
    '''
    typeWant = globals().get(what)
    if is_valid_what_type(typeWant):
        class rsForm(ModelForm):
                class Meta:
                    model = typeWant
        if request.method == 'POST':
            form = rsForm(request.POST)
            if form.is_valid():
                
            
                names = typeWant.objects.model._meta.get_all_field_names()
                data = {}
                for i in range(0, len(names)):
                    if(names[i] != u'id'):
                        data[names[i]] = form.cleaned_data[names[i]]
                obj = typeWant.objects.create(**data)
                                    
                obj.save()
                return HttpResponseRedirect('/sys/{}/{}/'.format(what, obj.pk))
           
        else:
            form = rsForm()
        return render_to_response('add.html', {'what':what, 'form':form}, context_instance=RequestContext(request))
    else:
        raise Http404
# 删除某个表的某一行
@user_passes_test(is_admin, login_url="/accounts/login/")
def delete(request, what, pk_id):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for deleting one of one of the admin things
    you can delete one of all your data of what type
    '''
    typeWant = globals().get(what)
    if is_valid_what_type(typeWant):
        r = typeWant.objects.get(pk=pk_id)
        if request.method == 'POST':
            if request.POST['post'] == 'yes':
                
                r.delete()
             
            return HttpResponseRedirect('/sys/{}/'.format(what))
        else:
            return render_to_response('delete.html', {'what':what, 'r':r}, context_instance=RequestContext(request))
    else:
        raise Http404
# 批量导入数据到某个表
@user_passes_test(is_admin, login_url="/accounts/login/")
def load(request, what):
    '''
    @param request: is the request that ask for
    @return: is the http response content
    @note: this class is the request for load a lot of one of the admin things
    you can load a lot of all your data of what type
    '''
    typeWant = globals().get(what)
    if is_valid_what_type(typeWant):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                load_file = request.FILES['file']
                for chunk in load_file.chunks():
                    lines = chunk.split('\r\n')
                    
                    for line in lines:
                        try:
                            if line == '':continue
                            row = line.split(',')
                            names = typeWant.objects.model._meta.get_all_field_names()
                            data = {}
                            for i in range(0, len(names)):
                                if(names[i] == 'city_id' or names[i] == 'starting_id'  or names[i] == 'destination_id'):
                                    data[names[i]] = city.objects.get(pk=row[i])
                                elif(names[i] == 'company_id'):
                                    data[names[i]] = company.objects.get(pk=row[i])
                                elif(names[i] == 'hotel_id'):
                                    data[names[i]] = hotel.objects.get(pk=row[i])
                                elif(names[i] == 'flight_id'):
                                    data[names[i]] = flight.objects.get(pk=row[i])
                                elif(names[i] == 'user_id'):
                                    data[names[i]] = User.objects.get(pk=row[i])
                                elif(names[i] == 'none_stop'):
                                    data[names[i]] = True if row[i] == 'T'else False
                                else:
                                    data[names[i]] = row[i]
                            obj = typeWant.objects.create(**data)
                            
                            obj.save()
                        except IntegrityError:
                            return HttpResponse('IntegrityError at line {}'.format(line))
                            
                return HttpResponseRedirect('/sys/{}/'.format(what))
            else:
                messages.add_message(request, messages.INFO,'The form is invalid.')         
            
        
        form = UploadFileForm(initial={'title':what})
        return render_to_response('load.html', {'form': form, 'what':what}, context_instance=RequestContext(request))
    else:
        raise Http404
