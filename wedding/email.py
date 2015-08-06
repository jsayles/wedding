import json
import requests
import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core import urlresolvers
from django.views.decorators.csrf import csrf_exempt
from django.template import Template, TemplateDoesNotExist, Context
from django.template.loader import get_template
from django.utils import timezone

from wedding.models import Invitation

logger = logging.getLogger(__name__)

class MailgunException(Exception):
	pass

def get_admin_emails():
	emails = []
	for name, email in settings.ADMINS:
		emails.append(email)
	return emails

def send_code_request(email):
	sent = False
	invite = Invitation.objects.by_email(email)
	if invite and invite.sent_ts:
		sent = send_invitation(invite)

	subject = "[Wedding] Code Request - %s" % (email)
	text_content = "Invitation Code Request\n===================\n\nEmail: %s\nSent: %s" % (email, sent)
	text_content += "\n\n" + settings.SITE_URL + urlresolvers.reverse('admin:index', args=[])
	mailgun_data =  {"from": settings.EMAIL_ADDRESS,
		"to": [get_admin_emails() ],
		"subject": subject,
		"text": text_content,
	}
	mailgun_send_raw(mailgun_data)
	
def send_guestbook_entry(guest_note):
	subject = "[Wedding] Guestbook - %s" % (guest_note.from_name)
	text_content = "New Guestbook Entry\n=================\n\nFrom: %s\nNote: %s" % (guest_note.from_name, guest_note.note)
	text_content += "\n\n" + settings.SITE_URL + urlresolvers.reverse('admin:wedding_guestnote_change', args=[guest_note.id])
	mailgun_data =  {"from": settings.EMAIL_ADDRESS,
		"to": [get_admin_emails() ],
		"subject": subject,
		"text": text_content,
	}
	return mailgun_send_raw(mailgun_data)

def send_question(from_name, note):
	subject = "[Wedding] Question - %s" % (from_name)
	text_content = "New Question\n=================\n\nFrom: %s\nNote: %s" % (from_name, note)
	text_content += "\n\n" + settings.SITE_URL + urlresolvers.reverse('admin:index', args=[])
	mailgun_data =  {"from": settings.EMAIL_ADDRESS,
		"to": [get_admin_emails() ],
		"subject": subject,
		"text": text_content,
	}
	return mailgun_send_raw(mailgun_data)

def send_new_rsvp(invitation):
	subject = "[Wedding] RSVP - %s" % (invitation.recipient)
	text_content = "New RSVP\n========\n\nRecipient: %s\nCeremony: %s\nReception: %s\nWV: %s" % (invitation.recipient, invitation.rsvp_ceremony, invitation.rsvp_reception, invitation.rsvp_wv)
	text_content += "\n\n" + settings.SITE_URL + urlresolvers.reverse('admin:wedding_invitation_change', args=[invitation.id])
	mailgun_data =  {"from": settings.EMAIL_ADDRESS,
		"to": [get_admin_emails() ],
		"subject": subject,
		"text": text_content,
	}
	return mailgun_send_raw(mailgun_data)

def send_invitation(invitation, safe=False):
	if not invitation.email1:
		raise MailgunException("Invitation does not have a valid email address!")

	# Render the content
	context = Context({
		'today': timezone.localtime(timezone.now()), 
		'invitation': invitation,
		'site_url': settings.SITE_URL,
		'safe': safe,
		}) 
	text_template = get_template("email_invite.txt")
	text_content = text_template.render(context)
	html_template = get_template("email_invite.html")
	html_content = html_template.render(context)

	# Send the email
	mailgun_data = {"from": settings.EMAIL_ADDRESS,
		"to": [invitation.email1,],
		"subject": "Jacob and Katie get Married!",
		"text": text_content,
		"html": html_content,
	}
	if invitation.email2:
		mailgun_data["to"].append(invitation.email2)
	mailgun_send_raw(mailgun_data)
	
	invitation.sent_ts = timezone.localtime(timezone.now())
	invitation.save()
	return True

def mailgun_send(mailgun_data, files_dict=None):
	#logger.debug("Mailgun send: %s" % mailgun_data)
	#logger.debug("Mailgun files: %s" % files_dict)

	# Make sure we have what we need
	from_name, from_address = email.utils.parseaddr(mailgun_data["from"])
	to_name, to_address = email.utils.parseaddr(mailgun_data["to"][0])
	subject = mailgun_data["subject"]
	if not from_address or not to_address or not subject:
		raise MailgunException("Mailgun data missing FROM, TO, or SUBJECT!")
	logger.debug("from: %s, to: %s, subject: %s" % (from_address, to_address, subject))

	# Clean up our bcc list
	if "bcc" in mailgun_data:
		bcc_list = mailgun_data["bcc"]
		if from_address in bcc_list:
			bcc_list.remove(from_address)
		if to_address in bcc_list:
			bcc_list.remove(to_address)
		mailgun_data["bcc"] = list(set(bcc_list))
		logger.debug("bcc: %s" % mailgun_data["bcc"])

	# Attach some headers: LIST-ID, REPLY-TO, Precedence...
	# Reply-To: list email apparently has some religious debates
	# (http://www.gnu.org/software/mailman/mailman-admin/node11.html) 
	# Precedence: list - helps some out of office auto responders know not to send their auto-replies. 
	mailgun_data["h:List-Id"] = to_address
	mailgun_data["h:Reply-To"] = to_address
	mailgun_data["h:Precedence"] = "list"

	# Fire in the hole!
	return mailgun_send_raw(mailgun_data, files_dict)

def mailgun_send_raw(mailgun_data, files_dict=None):
	# Make sure nothing goes out if the system is in debug mode
	if settings.DEBUG:
		# If we are in DEBUG mode override the TO address
		mailgun_data["to"] = [get_admin_emails() ]
		if not hasattr(settings, 'MAILGUN_DEBUG') or settings.MAILGUN_DEBUG:
			# We will see this message in the mailgun logs but nothing will actually be delivered
			logger.debug("mailgun_send: setting testmode=yes")
			mailgun_data["o:testmode"] = "yes"

	resp = requests.post("https://api.mailgun.net/v2/%s/messages" % settings.MAILGUN_DOMAIN,
		auth=("api", settings.MAILGUN_API_KEY),
		data=mailgun_data, 
		files=files_dict
	)
	logger.debug("Mailgun response: %s" % resp.text)
	return HttpResponse(status=200)

def get_logs(email):
	return requests.get("https://api.mailgun.net/v2/%s/messages" % settings.MAILGUN_DOMAIN,
		auth=("api", settings.MAILGUN_API_KEY),
		params={"ascending"   : "yes",
					"limit"       :  25,
					"pretty"      : "yes",
					"recipient" : email})
