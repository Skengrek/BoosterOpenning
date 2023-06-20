from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

USER_ROLES = [("Admin", "Admin"), ("Staff", "Staff"), ("User", "User")]


class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        if not username:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.username = username
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="users/avatars/%Y/%m/%d/", default="users/avatars/default.jpg"
    )
    joined_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=40, choices=USER_ROLES, default="User")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
