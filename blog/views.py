from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Blog, BlogSharing
from .serializers import (
    BlogEditSerializer,
    BlogSerializer,
    BlogSharingSerializer,
    AuthorsWithAccessSerializer,
)
from common.permissions import IsBlogOwnerOrReadOnly, IsBlogOwnerOrSharedWith
from common.pagination import CustomPagination
from drf_yasg.utils import swagger_auto_schema

class BlogViewset(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title",
        "content",
        "blog_author.fullname",
        "author__first_name",
        "author__last_name",
    ]  # Fields to search
    ordering_fields = ["title", "created_at", "updated_at"]  # Fields to order by

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        
        # Filter based on the author's (user's) is_active field
        return super().get_queryset().filter(author__is_active=True)
    
    # Override the perform_create method to set the author field
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return BlogEditSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [ permissions.IsAuthenticated(), IsBlogOwnerOrReadOnly()]
        return super().get_permissions()


class BlogSharingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=BlogSharingSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BlogSharingSerializer(data=request.data)
        if serializer.is_valid():
            # Set the owner of the shared blog post to the currently authenticated user
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter the BlogSharing objects to get authors with access to each blog
        return BlogSharing.objects.filter(owner=self.request.user)
