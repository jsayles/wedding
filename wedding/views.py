from django.conf import settings
from django.template import RequestContext, Template
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from wedding import email
from wedding.models import *

def home(request):
	return render_to_response('home.html',{'nbar':'home'}, RequestContext(request))

def ceremony(request):
	return render_to_response('ceremony.html',{'nbar':'ceremony'}, RequestContext(request))

def reception(request):
	return render_to_response('reception.html',{'nbar':'reception'}, RequestContext(request))

def wv_reception(request):
	return render_to_response('wv_reception.html',{'nbar':'wv_reception'}, RequestContext(request))

def registry(request):
	return render_to_response('registry.html',{'nbar':'registry'}, RequestContext(request))

def totals(request):
	all_invitations = Invitation.objects.all()
	
	total_est = 0
	total_conf = 0
	invites = []
	for tier_id, tier in TIER_CHOICES:
		invitations = Invitation.objects.filter(tier=tier_id)
		est_count = 0
		conf_count = 0
		viewed = 0
		unviewed = 0
		sent = 0
		unsent = 0
		for i in invitations:
			est_count = est_count + i.estimated_ceremony
			if i.rsvp_ceremony:
				conf_count += conf_count + i.rsvp_ceremony
			if i.last_viewed:
				viewed = viewed + 1
			else:
				unviewed = unviewed + 1
			if i.sent_ts:
				sent = sent + 1
			else:
				unsent = unsent + 1
		invites.append({'tier': tier, 'invitations':invitations, 'est_count':est_count, 'conf_count':conf_count, 'viewed':viewed, 'unviewed':unviewed, 'sent':sent, 'unsent':unsent})
		total_est = total_est + est_count
		total_conf = total_conf + conf_count
	return render_to_response('totals.html', {'tiers':TIER_CHOICES, 'invites': invites, 'total_est':total_est, 'total_conf':total_conf}, RequestContext(request))

def session_invitation(request):
	invitation = None
	if request.session.get('invitation_id', False):
		invitation_id = request.session['invitation_id']
		invitation = Invitation.objects.filter(pk=invitation_id).first()
	return invitation
	
def whoami(request):
	if "clear" in request.GET:
		request.session['invitation_id'] = None
		return HttpResponse("Cleared")
		
	invitation= session_invitation(request)
	if invitation:
		return HttpResponse(invitation.recipient)
	return HttpResponse("Unknown")

def guestbook(request):
	new_note = None
	if "from" in request.POST and "note" in request.POST:
		from_name = request.POST['from'].strip()
		note = request.POST['note'].strip()
		new_note = GuestNote.objects.create(from_name=from_name, note=note)
		# Send an email to announce the new entry
		email.send_guestbook_entry(new_note)
		
	invitation = session_invitation(request)
	guest_notes = GuestNote.objects.filter(approved=True).order_by('-created')
	return render_to_response('guestbook.html',{'nbar':'guestbook', 'guest_notes':guest_notes, 'new_note':new_note, 'invitation':invitation}, RequestContext(request))

def rsvp_save(request):
	invitation = session_invitation(request)
	try:
		invitation.rsvp_ceremony = request.POST.get("rsvp_ceremony")
		invitation.rsvp_reception = request.POST.get("rsvp_reception")
		invitation.rsvp_wv = request.POST.get("rsvp_wv")
		invitation.address_line1 = request.POST.get("address_line1")
		invitation.address_line2 = request.POST.get("address_line2")
		invitation.city = request.POST.get("city")
		invitation.state = request.POST.get("state")
		invitation.zip_code = request.POST.get("zip_code")
		invitation.email1 = request.POST.get("email1")
		invitation.email2 = request.POST.get("email2")
		invitation.save()
		messages.add_message(request, messages.ERROR, "Information saved")
	except Exception as e:
		messages.add_message(request, messages.ERROR, "Error saving: (%s)" % e)
	# Let the team know we have new information
	email.send_new_rsvp(invitation)
	return HttpResponseRedirect(reverse('wedding.views.rsvp'))

def rsvp(request, code=None):
	if not code and "code" in request.POST:
		code = request.POST.get("code")

	if code:
		# Pull it from the database
		invitation = Invitation.objects.by_code(code)
	else:
		# No Code - Check session
		invitation = session_invitation(request)

	if invitation:
		if not request.user.is_staff:
			invitation.last_viewed = timezone.localtime(timezone.now())
			invitation.save()

		request.session['invitation_id'] = invitation.id
	else:
		if code:
			# If we have code but could not find an invitation it's a bad code
			messages.add_message(request, messages.ERROR, 'Invalid invitation code.')
		return render_to_response('rsvp_form.html',{'nbar':'rsvp'}, RequestContext(request))
	

	return render_to_response('rsvp.html',{'nbar':'rsvp', 'invitation':invitation}, RequestContext(request))

