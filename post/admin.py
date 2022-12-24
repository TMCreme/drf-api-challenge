"""
Admin setup for post
"""
from django.contrib import admin

from .models import Post


admin.site.register(Post)

# Register your models here.
