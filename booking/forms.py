# -*- coding:utf-8 -*-  
from django import forms
import datetime
from booking.data import COMPANY_CHOICES
#这是航班搜索的表单
class flightForm(forms.Form):
    start = forms.CharField(label='start city',initial='阿克苏')
    des = forms.CharField(label='destination city',initial='安庆')
    date = forms.DateField(label='leave date',initial=datetime.date(2013, 6, 1))
    company = forms.ChoiceField(label='company',choices=COMPANY_CHOICES)
    NoneStop=(
              ('0','unlimit'),
              ('1','true'),
              ('2','false'),
              )
    non_stop = forms.ChoiceField(label='nonstop',choices=NoneStop)
    FLIGHT_CHOICES = (
        ('0','unlimit'),
        ('1','economy'),
        ('2','business'),
        ('3','first class'),
    )
    level = forms.ChoiceField(label='class',choices=FLIGHT_CHOICES)
    I_or_D_CHOICES = (
                      ('0',u'unsort'),
                      ('1',u'increase'),
                      ('2',u'decrease'),
                      )
                      
    I_or_D = forms.ChoiceField(label='how to sort',choices=I_or_D_CHOICES)
    SORT_BY = (
               ('0','unsort'),
               ('price','price'),
               ('company_id','company'),
               ('none_stop','none_stop'),
               ('leave_time','leave_time'),
               )
    sort_by = forms.ChoiceField(label='sort by',choices=SORT_BY)
#这是酒店搜索的表单
class hotelForm(forms.Form):
    city = forms.CharField(label='city',initial='北京')
    start = forms.DateField(label='check in date',initial=datetime.date(2013, 6, 1))
    last = forms.IntegerField(label='days to live in',initial=1)
    STAR_CHOICES = (
        ('0', 'unlimit'),
        ('2','<=2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5','5 stars'),
    )
    star = forms.ChoiceField(label='star level',choices=STAR_CHOICES)
    ROOM_CHOICES = (
        ('0', 'unlimit'),
        ('1', 'standard'),
        ('2', 'big'),
    )
    room_type =forms.ChoiceField(label='room type',choices=ROOM_CHOICES)
    keyword = forms.CharField(label='keyword',required=False)#keyword可以不填
    I_or_D_CHOICES = (
                      ('0',u'unsort'),
                      ('1',u'increase'),
                      ('2',u'decrease'),
                      )
                      
    I_or_D = forms.ChoiceField(label='how to sort',choices=I_or_D_CHOICES)
    SORT_BY = (
               ('0','unsort'),
               ('price','price'),
               ('hotel_star','hotel star'),
               ('scores','scores'),
               ('hot_level','hot level'),
               )
    sort_by = forms.ChoiceField(label='sort by',choices=SORT_BY)
        
        