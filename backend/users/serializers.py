from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User

User = get_user_model()

# override djoser's user registration serializer
class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "avatar",
            "role",
            "password",
        )


# override user details serializer
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "avatar",
            "role",
            "is_active",
        )
