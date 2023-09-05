from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairViewSet.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "confirm_email/<str:uidb64>/<str:token>/",
        ConfirmEmailView.as_view(),
        name="confirm-email",
    ),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),

    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user-profile/<str:pk>/', UserProfileRetrieveUpdateView.as_view(), name='user-profile'),
]
