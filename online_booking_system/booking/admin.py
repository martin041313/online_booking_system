# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the admin will be managed
'''  
from booking.models import company, city, flight, flight_discount, hotel, \
    room_num, room_discount, flight_record, hotel_record
from django.contrib import admin

#这个页面注册了admin可以管理的表的内容


admin.site.register(city)

admin.site.register(company)

admin.site.register(flight)
admin.site.register(hotel)

admin.site.register(room_num)


admin.site.register(room_discount)
admin.site.register(flight_discount)

admin.site.register(flight_record)
admin.site.register(hotel_record)

