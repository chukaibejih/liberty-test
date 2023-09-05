from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests (read-only) for any user
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Allow PUT, PATCH, DELETE requests only if the user is the owner of the blog
        return obj.id == request.user.id



class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsBlogOwnerOrSharedWith(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the shared blog or the shared_with author
        return obj.owner == request.user or obj.shared_with == request.user
