from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'LandingPage.views.homepage',name='homepage'),
    url(r'^pricing-plans/$', 'LandingPage.views.plans',name='plans'),
    url(r'^signup/(\d{1})/$', 'LandingPage.views.signup',name='signup'),
    url(r'^thanks/$', 'LandingPage.views.thanks',name='thanks'),
    # url(r'^$', 'Bondiz.views.home', name='home'),
    # url(r'^Bondiz/', include('Bondiz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()