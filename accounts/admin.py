from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'no_hp', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'no_hp')

# Register your models here.
