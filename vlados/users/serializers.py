from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


from .validators import validate_username

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.USERNAME_LENGTH,
                                     validators=[validate_username])
    password = serializers.CharField(max_length=settings.PASSWORD_LENGTH)
    email = serializers.CharField(max_length=settings.USERNAME_LENGTH)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.USERNAME_LENGTH)
    password = serializers.CharField(max_length=settings.PASSWORD_LENGTH)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
