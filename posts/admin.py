from django.contrib import admin
from .models import Post, Comment, Share #import model ที่สร้างขึ้น

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Share)
