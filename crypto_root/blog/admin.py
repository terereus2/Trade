from django.contrib import admin
from django.contrib.auth.models import User

from .models import Blog,Article,Comment,UserVote
# Register your models here.
admin.site.register(Blog)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserVote)