from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import UserProfile

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"New password": "The new password must meet the password requirements."})
        return value

    def validate_old_password(self, value):
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError("Invalid context. User object not found.")

        # check if old password matches current password
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password does not match.")
        return value

    def validate(self, data):
        old_password = data.get("old_password", None)
        new_password = data.get("new_password", None)

        if old_password and new_password and old_password == new_password:
            raise serializers.ValidationError(
                "New password cannot be the same as the old password."
            )

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_verified == False:
            raise serializers.ValidationError({"error": "Email is not verified."})

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_verified": user.is_verified,
        }

        # Create a refresh token and add it to the response data
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Include the user data in the response
        data.update(user_data)

        return data


class ConfirmEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ["token", "uidb64"]


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with email already exists")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=validated_data["password"],
                is_active=True,
                is_staff=False,
                is_verified=False,
            )
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_verified",
            "created_at",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ["user"]


class RetrieveUserSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_verified",
            "created_at",
            "user_profile",
        ]

    def get_user_profile(self, obj):
        try:
            profile = obj.userprofile
            return UserProfileSerializer(profile).data
        except UserProfile.DoesNotExist:
            return None
