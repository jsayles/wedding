from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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

class InvitationAdmin(admin.ModelAdmin):
	model = Invitation
	list_display=("recipient", )
	list_filter=("groups", )
	search_fields = ('recipient', 'email1')

admin.site.register(Invitation, InvitationAdmin)
