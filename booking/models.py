# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the data is stored in the database
'''  
from django.db import models

from django.contrib.auth.models import User #我们小组不负责用户和管理员的注册和登录验证，所以为了方便测试，我们使用了django自带的验证工具
class city(models.Model):#这是城市的表 可以添加更多数据 加强功能
    '''
    @note this is the city object.
    '''
    pinyin = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=256, unique=True)
    
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return self.name
class company(models.Model):
    '''
    @note this is the company object.
    '''
    name = models.CharField(max_length=256, unique=True)
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return self.name
FLIGHT_CHOICES = (
        ('1','economy'),
        ('2','business'),
        ('3','first class'),
    )
class flight(models.Model):
    '''
    @note this is the flight infomation object.
    '''
    starting_id  = models.ForeignKey(city,related_name='+',verbose_name ="出发地点");#models.CharField(max_length=4, choices=CITY_CHOICE,verbose_name ="出发城市")
    destination_id = models.ForeignKey(city,related_name='+',verbose_name ="目的地"); #models.CharField(max_length=4, choices=CITY_CHOICE,verbose_name ="到达城市")
    company_id = models.ForeignKey(company,related_name='+',verbose_name ="航空公司")
    
    none_stop = models.BooleanField(verbose_name ="直飞")

    plane_type = models.CharField(max_length=1, choices=FLIGHT_CHOICES,verbose_name ="舱位等级")
    
    price = models.FloatField(verbose_name ="价格")
    leave_date = models.DateField(verbose_name ="出发日期")
    leave_time = models.TimeField(verbose_name ="出发时间")
    arrive_date = models.DateField(verbose_name ="到达日期")
    arrive_time = models.TimeField(verbose_name ="到达时间")
    leave_number = models.IntegerField(verbose_name ="剩余票数")
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        f_type = FLIGHT_CHOICES[int(self.plane_type)-1][1]
        return u'{} {}->{} {} {} {}->{} {} {}:￥{} {}个座位'\
            .format(self.company_id, self.starting_id,self.destination_id,u'直飞' if self.none_stop else u'中转',self.leave_date,\
            self.leave_time,self.arrive_date,self.arrive_time,f_type,self.price,self.leave_number)


    
STAR_CHOICES = (
        ('2','<=2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5','5 stars'),
    )
ROOM_CHOICES = (
        ('1', 'standard'),
        ('2', 'big'),
    )
class hotel(models.Model):
    '''
    @note this is the hotel infomation object.
    '''
    name = models.CharField(max_length=256)

    hotel_star = models.CharField(max_length=1, choices=STAR_CHOICES)
    img_url = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    city_id = models.ForeignKey(city,related_name='+')
    
    price = models.FloatField()

    room_type = models.CharField(max_length=1, choices=ROOM_CHOICES)
    hot_level = models.IntegerField(default=0)
    commented_num = models.IntegerField(default=0)
    scores = models.IntegerField(default=-1)
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        r_type = ROOM_CHOICES[int(self.room_type)-1][1]
        h_type = STAR_CHOICES[int(self.hotel_star)-2][1]
        return u'{} {} {} {} {}: ￥{} 热度:{} 评分:{}' \
            .format(self.city_id, self.name,h_type,self.phone_number,r_type,self.price,self.hot_level,'not comented yet!' if self.scores==-1 else str(self.scores))

class room_num(models.Model):
    '''
    @note this is the hotel room infomation object.
    '''
    hotel_id = models.ForeignKey(hotel,related_name='+')
    room_number = models.IntegerField()
    date = models.DateField()
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return u'{} {} 剩余{}个房间' .format(self.hotel_id,self.date,self.room_number)
class flight_discount(models.Model):
    '''
    @note this is the flight discount infomation object.
    '''
    flight_id  = models.ForeignKey(flight,related_name='+')
    discount = models.FloatField()
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return u'{}-{}' .format(self.flight_id,self.discount)
class room_discount(models.Model):
    '''
    @note this is the room discount infomation object.
    '''
    hotel_id  = models.ForeignKey(hotel,related_name='+')
    discount = models.FloatField()
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return u'{}-{}' .format(self.hotel_id,self.discount)
class hotel_record(models.Model):
    '''
    @note this is the hotel room booking record infomation object.
    '''
    user_id = models.ForeignKey(User,related_name='+')
    hotel_id = models.ForeignKey(hotel,related_name='+')
    comment = models.CharField(max_length=512,default='')
    scores = models.IntegerField(default=-1)
    checkin_date = models.DateField()
    last = models.IntegerField()
    num = models.IntegerField()
    book_date = models.DateField()
    book_time = models.TimeField()
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return u'{}-{}' .format(self.user_id,self.hotel_id)
class flight_record(models.Model):
    '''
    @note this is the hotel flight booking record infomation object.
    '''
    user_id = models.ForeignKey(User,related_name='+')
    flight_id = models.ForeignKey(flight,related_name='+')

    comment = models.CharField(max_length=512,default='')
    scores = models.IntegerField(default=-1)
    num = models.IntegerField()
    book_date = models.DateField()
    book_time = models.TimeField()
    def __unicode__(self):
        '''
        @return: returns how the object will be printed
        '''
        return u'{}-{}' .format(self.user_id,self.flight_id)