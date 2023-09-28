from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authentication.models import CustomUser


class PhotoProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ['profile_photo']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_photo']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.profile_photo = validated_data.get('profile_photo',
                                                    instance.profile_photo)
        instance.save()
        return instance


class ChangePasswordAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['old_password', 'password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username"]

    def validate_username(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This user already in use."})
        return value

    def update(self, instance, validated_data):
        instance.username = validated_data["username"]
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']  #