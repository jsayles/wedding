import csv
from datetime import date, datetime

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
	invitation= session_invitation(request)
	return render_to_response('home.html',{'invitation':invitation}, RequestContext(request))

def ceremony(request):
	invitation= session_invitation(request)
	return render_to_response('ceremony.html',{'invitation':invitation}, RequestContext(request))

def reception(request):
	invitation= session_invitation(request)
	return render_to_response('reception.html',{'invitation':invitation}, RequestContext(request))

def wv_reception(request):
	invitation= session_invitation(request)
	return render_to_response('wv_reception.html',{'invitation':invitation}, RequestContext(request))

def registry(request):
	invitation= session_invitation(request)
	return render_to_response('registry.html',{'invitation':invitation}, RequestContext(request))

def hotels(request):
	invitation= session_invitation(request)
	return render_to_response('hotels.html',{'invitation':invitation}, RequestContext(request))

def view_invite_email(request):
	invitation = Invitation.objects.get(pk=1)
	context = RequestContext(request)
	safe = "safe" in request.GET
	args = {'invitation':invitation, 'site_url':settings.SITE_URL, 'safe':safe}
	if "text" in request.GET:
		return render_to_response('email_invite.txt', args, context, content_type="text/plain")
	return render_to_response('email_invite.html', args, context)

@staff_member_required
def totals(request):
	all_invitations = Invitation.objects.all()
	
	total_est_ceremony = 0
	total_conf_ceremony = 0
	total_est_wv = 0
	total_conf_wv = 0
	invites = []
	for tier_id, tier in TIER_CHOICES:
		invitations = Invitation.objects.filter(tier=tier_id)
		est_ceremony = 0
		conf_ceremony = 0
		est_wv = 0
		conf_wv = 0
		viewed = 0
		unviewed = 0
		sent = 0
		unsent = 0
		for i in invitations:
			est_ceremony = est_ceremony + i.estimated_ceremony
			est_wv = est_ceremony + i.estimated_wv
			if i.rsvp_ceremony:
				conf_ceremony = conf_ceremony + i.rsvp_ceremony
			if i.rsvp_wv:
				conf_wv = conf_wv + i.rsvp_wv
			if i.last_viewed:
				viewed = viewed + 1
			else:
				unviewed = unviewed + 1
			if i.sent_ts:
				sent = sent + 1
			else:
				unsent = unsent + 1
		invites.append({'tier': tier, 'invitations':invitations, 'est_ceremony':est_ceremony, 'conf_ceremony':conf_ceremony, 'est_wv':est_wv, 'conf_wv':conf_wv, 
			'viewed':viewed, 'unviewed':unviewed, 'sent':sent, 'unsent':unsent})
		total_est_ceremony = total_est_ceremony + est_ceremony
		total_conf_ceremony = total_conf_ceremony + conf_ceremony
		total_est_wv = total_est_wv + est_wv
		total_conf_wv = total_conf_wv + conf_wv
	return render_to_response('totals.html', {'tiers':TIER_CHOICES, 'invites': invites, 'total_est_ceremony':total_est_ceremony, 'total_conf_ceremony':total_conf_ceremony, 
		'total_est_wv':total_est_wv, 'total_conf_wv':total_conf_wv}, RequestContext(request))

@staff_member_required
def gifts(request):
	if "invite_id" in request.POST:
		invite_id = int(request.POST['invite_id'])
		invite = Invitation.objects.get(id=invite_id)
		if "gift" in request.POST:
			invite.gift = request.POST['gift'].strip()
		else:
			invite.thank_you_sent = True
		invite.save()
	no_gift = Invitation.objects.no_gift()
	has_gift = Invitation.objects.has_gift()
	need_thanks = has_gift.filter(thank_you_sent=False)
	return render_to_response('gifts.html',{'no_gift':no_gift, 'has_gift':has_gift, 'need_thanks':need_thanks}, RequestContext(request))

@staff_member_required
def export(request):
	invites = Invitation.objects.all()
	header = ['recipient', 'address_line1', 'address_line2', 'city', 'state', 'zip_code',
		'have_address', 'thank_you_sent', 'mail_invitation', 'check_spelling', 'is_viewed', 'is_sent', 'have_rsvp',
		'email1', 'email2', 'code', 'tier', 'last_viewed', 'sent_ts', 'notes']

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="invitations-%s.csv"' % date.today().isoformat()
	writer = csv.writer(response)

	# Write out the header
	writer.writerow(header)

	# Write out the fields
	for invite in invites:
		row = []
		row.append(invite.recipient)
		row.append(invite.address_line1)
		row.append(invite.address_line2)
		row.append(invite.city)
		row.append(invite.state)
		row.append(invite.zip_code)
		row.append(invite.have_address())
		row.append(invite.thank_you_sent)
		row.append(invite.mail_invitation)
		row.append(invite.check_spelling)
		row.append(invite.is_viewed())
		row.append(invite.is_sent())
		row.append(invite.have_rsvp())
		row.append(invite.email1)
		row.append(invite.email2)
		row.append(invite.get_code())
		row.append(invite.tier)
		if invite.last_viewed:
			row.append(invite.last_viewed.isoformat())
		else:
			row.append("")
		if invite.sent_ts:
			row.append(invite.sent_ts.isoformat())
		else:
			row.append("")
		row.append(invite.notes)
		writer.writerow(row)

	return response

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
	return render_to_response('guestbook.html',{'guest_notes':guest_notes, 'new_note':new_note, 'invitation':invitation}, RequestContext(request))

def contact(request):
	new_note = False
	if "from" in request.POST and "note" in request.POST:
		from_name = request.POST['from'].strip()
		note = request.POST['note'].strip()
		email.send_question(from_name, note)
		new_note = True
		
	invitation = session_invitation(request)
	return render_to_response('contact.html',{'new_note':new_note, 'invitation':invitation}, RequestContext(request))

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
	return HttpResponseRedirect(reverse('rsvp'))

def rsvp(request, code=None):
	if "email" in request.POST:
		email.send_code_request(request.POST.get("email"))
		msg = "Invitation code sent.  If you can't find it, search for 'jacobandkatiegetmarried' and look in your spam folder."
		messages.add_message(request, messages.INFO, msg)
		
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

	# If given a return, go there
	if "return" in request.POST:
		return_location = request.POST.get("return")
		return HttpResponseRedirect(reverse(return_location))

	return render_to_response('rsvp.html', {'invitation':invitation}, RequestContext(request))

def register_open(request, code):
	try:
		invitation = Invitation.objects.by_code(code)
		if invitation:
			invitation.last_viewed = timezone.localtime(timezone.now())
			invitation.save()
	except:
		pass
	TRANSPARENT_1_PIXEL_GIF = "\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
	return HttpResponse(TRANSPARENT_1_PIXEL_GIF, content_type='image/gif')
