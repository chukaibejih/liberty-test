from rest_framework import viewsets, generics, permissions, filters
from .models import Blog, BlogSharing
from .serializers import (
    BlogEditSerializer,
    BlogSerializer,
    BlogSharingSerializer,
    AuthorsWithAccessSerializer,
)
from common.permissions import IsOwnerOrReadOnly, IsBlogOwnerOrSharedWith
from common.pagination import CustomPagination


class BlogViewset(viewsets.ModelViewSet):
    queryset = Blog
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title",
        "content",
        "blog_author.fullname",
    ]  # Fields to search
    ordering_fields = ["title", "created_at", "updated_at"]  # Fields to order by

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(blog_author__is_active=True)

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return BlogEditSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [
                permissions.IsAuthenticated(),
                IsOwnerOrReadOnly(),
            ]
        return super().get_permissions()


class BlogSharingView(generics.CreateAPIView):
    queryset = BlogSharing.objects.all()
    serializer_class = BlogSharingSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Ensure the user is authenticated

    def perform_create(self, serializer):
        # Set the owner of the shared blog post to the currently authenticated user
        serializer.save(owner=self.request.user)


class SharedBlogsListView(generics.ListAPIView):
    queryset = BlogSharing.objects.all()
    serializer_class = BlogSharingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBlogOwnerOrSharedWith]

    def get_queryset(self):
        # Filter blogs shared with the currently authenticated author
        return BlogSharing.objects.filter(shared_with=self.request.user)


class AuthorsWithAccessView(generics.ListAPIView):
    queryset = BlogSharing.objects.all()
    serializer_class = AuthorsWithAccessSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Ensure the user is authenticated

    def get_queryset(self):
        # Filter the BlogSharing objects to get authors with access to each blog
        return BlogSharing.objects.filter(blog__author=self.request.user)
