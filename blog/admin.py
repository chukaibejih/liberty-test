from django.contrib import admin
from .models import Blog, BlogSharing

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('author',)
    search_fields = ('title', 'content', 'author__email')


@admin.register(BlogSharing)
class BlogSharingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'shared_with', 'blog')
    list_filter = ('owner', 'shared_with')
    search_fields = ('owner__email', 'shared_with__email', 'blog__title')
