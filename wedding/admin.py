from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from wedding.models import UserProfile, Invitation

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

class InvitationAdmin(admin.ModelAdmin):
	pass
admin.site.register(Invitation, InvitationAdmin)
