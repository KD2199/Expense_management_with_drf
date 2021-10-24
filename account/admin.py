from rest_framework.authtoken.admin import TokenAdmin
from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    list_filter = ['email']


TokenAdmin.raw_id_fields = ['user']
