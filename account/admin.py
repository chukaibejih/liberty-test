from django.contrib import admin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name"]
    list_filter = ["created_at", "is_verified", "is_active", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__first_name", "user__last_name"]
    list_filter = ["user__created_at"]
