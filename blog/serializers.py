from rest_framework import serializers
from .models import Blog, BlogSharing
from account.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    class Meta:
        model = Blog
        fields = ["id", "title", "content", "author"]


class BlogEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["id", "title", "content"]


class BlogSharingSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    class Meta:
        model = BlogSharing
        fields = ["owner", "shared_with", "blog"]


class AuthorsWithAccessSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    shared_with = UserSerializer()
    blog = BlogSerializer()

    class Meta:
        model = BlogSharing
        fields = ["owner", "shared_with", "blog"]
