from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have email')
        if not password:
            raise ValueError('User must have password')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.is_ambassador = False
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('User must have email')
        if not password:
            raise ValueError('User must have password')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.is_ambassador = False
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_ambassador = models.BooleanField(default=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
