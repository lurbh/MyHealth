from django.contrib import admin
from .models import *

# Register your models here.
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['id','email']

admin.site.register(Subscriber, SubscriberAdmin)