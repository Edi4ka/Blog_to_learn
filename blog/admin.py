from django.contrib import admin
from .models import Post, Comment, RatingComment, RatingPost


class AdminPost(admin.ModelAdmin):
    fields = ('title', 'text', 'author', 'tags', 'approved')
    list_display = ('title', 'time_published', 'time_edited')
    list_filter = ('approved', 'time_published')


admin.site.register(Post, AdminPost)
admin.site.register(Comment,)
admin.site.register(RatingComment)
admin.site.register(RatingPost)
