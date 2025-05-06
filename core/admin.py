from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dark_mode']
    search_fields = ['user__username', 'user__email']

admin.site.register(UserProfile, UserProfileAdmin)