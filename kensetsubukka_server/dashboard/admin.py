from django.contrib import admin

# Register your models here.
from .models import Request, User_dashboard

admin.site.register(Request)
admin.site.register(User_dashboard)