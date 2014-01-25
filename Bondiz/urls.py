from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # url(r'^accounts/', include('allauth.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/homepage/'}),
    #url(r'^$', 'LandingPage.views.homepage',name='homepage'),
    # url(r'^signup/$', 'LandingPage.views.signup',name='signup'),
    # url(r'^thanks/$', 'LandingPage.views.thanks',name='thanks'),
    # url(r'^$', 'Bondiz.views.home', name='home'),
    # url(r'^Bondiz/', include('Bondiz.foo.urls')),
    
    url(r'^$', 'BondizApp.views.home',name='home'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^paypal/create/$', 'BondizApp.views.paypal_create',name='paypal_create'),
    url(r'^paypal/execute/$', 'BondizApp.views.paypal_execute',name='paypal_execute'),
)

urlpatterns += staticfiles_urlpatterns()