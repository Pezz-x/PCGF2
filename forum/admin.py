from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('author', 'title', 'time_created')
    search_fields = ('author', 'title')
    list_filter = ('author', 'title')
    prepopulated_fields = {'slug':('title',)}
    summernote_fields = ('body',)

admin.site.register(Comment)
