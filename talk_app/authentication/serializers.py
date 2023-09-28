from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from authentication.models import CustomUser


class EmailLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UsernameRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    # def validate_username(self, username):
    #     if CustomUser.objects.filter(username=username).exists():
    #         raise serializers.ValidationError("A user with this username already exists.")
    #     return username
    #
    # def validate_email(self, email):
    #     if CustomUser.objects.filter(email=email).exists():
    #         raise serializers.ValidationError("A user with this email already exists.")
    #     return email

