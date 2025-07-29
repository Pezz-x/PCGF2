from django.contrib import admin
from .models import Post
#from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):

    list_display = ('author', 'title', 'slug', 'time_created')
    search_fields = ['author', 'title', 'body']
    list_filter = ('author', 'time_created')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('body',)
