from rest_framework import serializers
from .models import Blog, BlogSharing
from account.models import User


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["title", "content"]


class BlogSharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSharing
        fields = ["owner", "shared_with", "blog"]


class AuthorsWithAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
