import time

from django.conf.urls import patterns, include, url
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
	url(r'^cache\.manifest$', lambda r: HttpResponse("CACHE MANIFEST\n#Time: %s\nCACHE:\nFALLBACK:\nNETWORK:\n*" % time.time(), content_type="text/plain")),

	url(r'^$', 'wedding.views.home', name='home'),
	url(r'^ceremony/', 'wedding.views.ceremony', name='ceremony'),
	url(r'^wa_reception/', 'wedding.views.reception', name='reception'),
	url(r'^wv_reception/', 'wedding.views.wv_reception', name='wv_reception'),
	url(r'^whoami/', 'wedding.views.whoami', name='whoami'),
	url(r'^registry/', 'wedding.views.registry', name='registry'),
	url(r'^hotels/', 'wedding.views.hotels', name='hotels'),
	url(r'^guestbook/', 'wedding.views.guestbook', name='guestbook'),
	url(r'^contact/', 'wedding.views.contact', name='contact'),
	url(r'^totals/', 'wedding.views.totals', name='totals'),
	url(r'^gifts/', 'wedding.views.gifts', name='gifts'),
	url(r'^export/', 'wedding.views.export', name='export'),
	url(r'^rsvp/(?P<code>[0-9a-z]+)$', 'wedding.views.rsvp', name='rsvp'),
	url(r'^rsvp/', 'wedding.views.rsvp', name='rsvp'),
	url(r'^save/', 'wedding.views.rsvp_save', name='rsvp_save'),
	url(r'^email/', 'wedding.views.view_invite_email', name='email'),
	url(r'^plan/', 'wedding.views.wedding_plan', name='plan'),
	url(r'^photos/', 'wedding.views.photos', name='photos'),
	url(r'^register_open/(?P<code>[0-9a-z]+)/', 'wedding.views.register_open', name='register_open'),

	url(r'^admin/', include(admin.site.urls)),
)