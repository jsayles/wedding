from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Q

from wedding.models import UserProfile, InvitationGroup, Invitation

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
admin.site.register(InvitationGroup, InvitationGroupAdmin)

class AddressFilter(admin.SimpleListFilter):
	title = "address"
	parameter_name = "address"

	def lookups(self, request, model_admin):
		return (
			('True', 'True'),
			('False', 'False'),
		)

	def queryset(self, request, queryset):
		if self.value() == 'True':
			return queryset.exclude(address_line1__exact='').exclude(city__exact='').exclude(state__exact='').exclude(zip_code__exact='')
		if self.value() == 'False':
			return queryset.filter(Q(address_line1="") | Q(city="") | Q(state="") | Q(zip_code=""))

class InvitationAdmin(admin.ModelAdmin):
	def address(self):
		if self.address_line1 and self.city and self.state and self.zip_code:
			return True
		return False;

	model = Invitation
	list_display=("recipient", address, "email1")
	list_filter=("groups", AddressFilter)
	search_fields = ('recipient', 'email1')

admin.site.register(Invitation, InvitationAdmin)