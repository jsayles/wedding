from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save

STATE_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))

class UserProfile(models.Model):
	user = models.OneToOneField(User)

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

class InvitationGroup(models.Model):
	name = models.CharField(max_length=32)

	def __unicode__(self):
		return (self.name)

class Invitation(models.Model):
	recipient = models.CharField("Recipient", max_length = 64)
	address_line1 = models.CharField("Address line 1", max_length = 64, blank = True)
	address_line2 = models.CharField("Address line 2", max_length = 64, blank = True)
	city = models.CharField("City", max_length = 64, blank = True)
	state = models.CharField("State", choices=STATE_CHOICES, max_length=2, blank = True)
	zip_code = models.CharField("Zip Code", max_length = 10, blank=True)
	email1 = models.EmailField("Primary Email", blank=True, null=True)
	email2 = models.EmailField("Alternate Email", blank=True, null=True)
	rsvp_ceremony = models.PositiveSmallIntegerField("Confirmed Ceremony", blank=True, null=True)
	rsvp_reception = models.PositiveSmallIntegerField("Confirmed Reception", blank=True, null=True)
	rsvp_wv = models.PositiveSmallIntegerField("Confirmed West Virginia Reception", blank=True, null=True)
	estimated_ceremony = models.PositiveSmallIntegerField("Estimated Ceremony", default=0)
	estimated_reception = models.PositiveSmallIntegerField("Estimated Reception", default=0)
	estimated_wv = models.PositiveSmallIntegerField("Estimated West Virginia Reception", default=0)
	gift = models.CharField("Gift", max_length = 64, blank = True)
	thank_you_sent = models.BooleanField(default=False)
	notes = models.TextField(blank=True, null=True)
	groups = models.ManyToManyField(InvitationGroup, blank=True)

	def __unicode__(self):
		return (self.recipient)