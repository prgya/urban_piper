from django.contrib import admin

# Register your models here.

from .models import hackernews

admin.site.register(hackernews)
