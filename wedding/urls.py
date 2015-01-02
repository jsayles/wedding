from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', 'wedding.views.home', name='home'),
	url(r'^ceremony/', 'wedding.views.ceremony', name='ceremony'),
	url(r'^wa_reception/', 'wedding.views.reception', name='reception'),
	url(r'^wv_reception/', 'wedding.views.wv_reception', name='wv_reception'),
	url(r'^rsvp/', 'wedding.views.rsvp', name='rsvp'),
	url(r'^admin/', include(admin.site.urls)),
)
