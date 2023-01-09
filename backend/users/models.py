from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = [("Admin", "Admin"), ("Staff", "Staff"), ("User", "User")]


class User(AbstractUser):
    avatar = models.ImageField(
        upload_to="users/avatars/%Y/%m/%d/", default="users/avatars/default.jpg"
    )
    bio = models.TextField(max_length=500, null=True)
    joined_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=40, choices=USER_ROLES, default="User")

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
