from django.conf import settings
from django.template import RequestContext, Template
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from wedding.models import Invitation

def home(request):
	return render_to_response('home.html',{'nbar':'home'}, RequestContext(request))

def ceremony(request):
	return render_to_response('ceremony.html',{'nbar':'ceremony'}, RequestContext(request))

def reception(request):
	return render_to_response('reception.html',{'nbar':'reception'}, RequestContext(request))

def wv_reception(request):
	return render_to_response('wv_reception.html',{'nbar':'wv_reception'}, RequestContext(request))

def rsvp(request, code=None):
	if not code and "code" in request.POST:
		code = request.POST.get("code")

	invitation = Invitation.objects.by_code(code)
	if not invitation:
		print code
		if code:
			messages.add_message(request, messages.ERROR, 'Invalid invitation code.')
		return render_to_response('rsvp_form.html',{'nbar':'rsvp'}, RequestContext(request))
	
	if not request.user.is_staff:
		invitation.last_viewed = timezone.localtime(timezone.now())
		invitation.save()
	return render_to_response('rsvp.html',{'nbar':'rsvp', 'invitation':invitation}, RequestContext(request))

