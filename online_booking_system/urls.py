from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'online_booking_system.views.home', name='home'),
    # url(r'^online_booking_system/', include('online_booking_system.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$','booking.views.index'),
    
    
    url(r'^sys/',include('adminInfo.urls')),
    
    url(r'^booking/',include('booking.urls')),
    
    url(r'^accounts/login/$','userInfo.views.login_view'),
    
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login'}),
    url(r'^accounts/reg/$','userInfo.views.register'),
)
