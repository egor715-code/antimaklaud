from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'team')
    list_display = ('username', 'email', 'role', 'team', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'chevron_photo', 'team')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(BanReason)
admin.site.register(BanTeam)
