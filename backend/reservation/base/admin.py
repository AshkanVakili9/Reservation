from django.contrib import admin
from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    
    readonly_fields = ['date_joined']
    list_display = ['full_name','phone']

    search_fields = ['full_name', 'phone']
    
    list_filter = ['is_staff', 'is_active', 'date_joined']


admin.site.register(User, UserAdmin)
admin.site.register(Sms)
