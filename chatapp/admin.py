from django.contrib import admin

# Register your models here.
from .models import Client, Project

admin.site.register(Client)
admin.site.register(Project)
