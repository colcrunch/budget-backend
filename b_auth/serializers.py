from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(allow_blank=False, read_only=True)

    def validate(self, data):
        try:
            user = User.objects.filter(username=data.get('username'))
            if len(user) > 0:
                raise serializers.ValidationError(_("Username already exists"))
        except User.DoesNotExist:
            pass

        if not data.get('first_name'):
            raise serializers.ValidationError(_("First Name Error: This field may not be blank"))

        if not data.get('last_name'):
            raise serializers.ValidationError(_("Last Name Error: This field may not be blank"))
        
        if not data.get('email'):
            raise serializers.ValidationError(_("Email Error: This field may not be blank"))
        
        if not data.get('password') or not self.initial_data.get('confirm_password'):
            raise serializers.ValidationError(_("Password Error: This field may not be blank"))

        if data.get('password') != self.initial_data.get('confirm_password'):
            raise serializers.ValidationError(_("Passwords do not match"))

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_active=validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password', 'email', 'is_active')
        extra_kwargs = {'confirm_password': {'read_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'sfin_token']