import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from .manager import UserManager


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True
        return super().save(*args, **kwargs)

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    GENDER = (
        ("male", "Male"),
        ("female", "Female"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER)
    published_posts = models.IntegerField(default=0)
