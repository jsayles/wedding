from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings

from wedding.models import *

def gen_message(queryset, noun, pl_noun, suffix):
	if len(queryset) == 1:
		prefix = "1 %s was" % noun
	else:
		prefix = "%d %s were" % (len(queryset), pl_noun)
	msg = prefix + " " + suffix + "."
	return msg

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class InvitationGroupAdmin(admin.ModelAdmin):
	pass

class AddressFilter(admin.SimpleListFilter):
	title = "address"
	parameter_name = "address"

	def lookups(self, request, model_admin):
		return (
			('Yes', 'Yes'),
			('No', 'No'),
		)

	def queryset(self, request, queryset):
		if self.value() == 'Yes':
			return queryset.exclude(address_line1__exact='').exclude(city__exact='').exclude(state__exact='').exclude(zip_code__exact='')
		if self.value() == 'No':
			return queryset.filter(Q(address_line1="") | Q(city="") | Q(state="") | Q(zip_code=""))

class InvitationAdmin(admin.ModelAdmin):
	def address(self):
		if self.address_line1 and self.city and self.state and self.zip_code:
			return "Yes"
		return "No";
	
	def estimated(self):
		return self.estimated_ceremony
		
	def confirmed(self):
		if not self.rsvp_ceremony:
			return ""
		return self.rsvp_ceremony
	
	def group(self):
		if not self.groups or self.groups.count() == 0:
			return "None"
		elif self.groups.count() > 1:
			return "Multiple"
		return self.groups.first().name

	def code(self):
		code = self.get_code()
		url = self.get_url()
		return '<a href="%s">%s</a>' % (url, code)
	code.allow_tags = True

	model = Invitation
	list_display=("recipient", address, "email1", estimated, confirmed, group, "tier", "last_viewed", code)
	list_filter=("groups", "tier", AddressFilter, "thank_you_sent", "mail_invitation", "check_spelling")
	search_fields = ("recipient", "email1", "email2")

class GuestNoteAdmin(admin.ModelAdmin):
	def approve(self, request, queryset):
		for note in queryset:
			note.approve()
		msg = gen_message(queryset, "GuestNote", "GuestNotes", "approved")
		self.message_user(request, msg)

	model = GuestNote
	list_display=("created", "from_name", "approved")
	list_filter=("approved",)
	search_fields = ("from_name",)
	actions= ["approve", ]

# Register all our new admin models
admin.site.register(InvitationGroup, InvitationGroupAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(GuestNote, GuestNoteAdmin)
