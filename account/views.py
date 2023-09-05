from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import smart_str
from django.http import Http404
from common.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, generics, status, permissions
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from common.pagination import CustomPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    RegistrationSerializer,
    RetrieveUserSerializer,
)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = get_user_model()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)

        old_password = request.data.get("old_password")
        if not request.user.check_password(old_password):
            return Response(
                {"error": "Password change failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_password = request.data.get("new_password")
        request.user.set_password(new_password)
        request.user.save()

        return Response({"message": "Password changed successfully"},status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairViewSet(TokenObtainPairView):

    """
    View to obtain an access token and refresh token using a custom serializer.
    """

    serializer_class = CustomTokenObtainPairSerializer


class ConfirmEmailView(APIView):

    """
    View for confirming a user's email address.
    Accepts a POST request with 'uidb64' and 'token' parameters in the URL.
    If the provided token is valid, sets the user's email as verified and active.
    Returns a success message or an error message if the token is invalid.
    """

    permission_classes = []

    def post(self, request, uidb64, token):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise Http404("User not found")

        if default_token_generator.check_token(user, token):
            # Wrap the user update operations in a transaction for safety
            with transaction.atomic():
                user.is_active = True
                user.is_verified = True
                user.save()
            return Response(
                {"message": "Email confirmation successful"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationView(generics.CreateAPIView):
    """
    View for user registration.
    Accepts a POST request with user registration data in the request body.
    Uses the RegistrationSerializer to create a new user account.
    """

    serializer_class = RegistrationSerializer


class UserListView(generics.ListAPIView):
    serializer_class = RetrieveUserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = CustomPagination
    search_fields = ["first_name", "last_name", "email"]

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RetrieveUserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a user profile.
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return self.queryset.get(user=self.request.user)
