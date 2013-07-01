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
    url(r'^$','adminInfo.views.index'),
    url(r'^(?P<what>\w+)/$','adminInfo.views.show'),
    url(r'^(?P<what>\w+)/(?P<pk_id>\d+)/$','adminInfo.views.edit'),
    url(r'^(?P<what>\w+)/(?P<pk_id>\d+)/delete/$','adminInfo.views.delete'),
    url(r'^(?P<what>\w+)/load/$','adminInfo.views.load'),
    url(r'^(?P<what>\w+)/add/','adminInfo.views.add'),
    
)