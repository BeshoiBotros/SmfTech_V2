from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    
    email    = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True) 

    class Meta:
        
        model  = User
        fields = ['id','username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def validate_password(self, value):
        # Example validation: password must be at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Example validation: password must contain at least one digit
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        
        # Example validation: password must contain at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        # Example validation: password must contain at least one special character
        if not re.search(r'[!@#$%^&*(),.?_":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        
        return value
    
    def validate_email(self, value):

        # check if user email already exist or not
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        from .models import Profile
        model  = Profile
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({'new password': 'new password can not be the same old password'})
        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordConfirmation(serializers.Serializer):
    new_password = new_password = serializers.CharField(write_only = True, validators=[validate_password])

