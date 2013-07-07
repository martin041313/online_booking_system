'''
@version: v2.0
'''
from django.conf.urls import patterns, include, url

from Order import views

urlpatterns = patterns('',
    url(r'^$', views.viewMyOrder),
    url(r'^json/$', views.viewAllOrderJSON),
    #url(r'^check/$', views.viewCheckUser),
    url(r'^comment/(?P<orderId>\d+)/$', views.viewComment),
    url(r'^json/(?P<orderId>\d+)/$', views.viewOneOrderJSON),
    url(r'^create/$', views.viewCreateOrder),
    url(r'^cancel/(?P<orderId>\d+)/$', views.viewCancel),
    url(r'^pay/(?P<orderId>\d+)/$', views.viewPay),
    url(r'^ship/(?P<orderId>\d+)/$', views.viewShip),
    url(r'^arrive/(?P<orderId>\d+)/$', views.viewArrive),
    url(r'^refund/(?P<orderId>\d+)/$', views.viewRefund),
    url(r'^complete/(?P<orderId>\d+)/$', views.viewComplete),
    url(r'^close/(?P<orderId>\d+)/$', views.viewClose),
)
