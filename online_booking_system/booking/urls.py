# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the url is processed
'''  
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                    url(r'^$','booking.views.index'),
                    
                    url(r'^flight/$','booking.views.search_flight'),
                    url(r'^hotel/$','booking.views.search_hotel'),
                    
                    url(r'^flight/(?P<pk_id>\d+)/$','booking.views.book_flight'),
                    url(r'^hotel/(?P<pk_id>\d+)/$','booking.views.book_hotel'),
                    url(r'^my_record/flight/$','booking.views.my_flight_record'),
                    url(r'^my_record/hotel/$','booking.views.my_hotel_record'),
                    url(r'^my_record/flight/(?P<pk_id>\d+)/$','booking.views.flight_record_view'),
                    url(r'^my_record/hotel/(?P<pk_id>\d+)/$','booking.views.hotel_record_view'),
)
