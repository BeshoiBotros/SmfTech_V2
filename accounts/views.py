from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models, serializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
from SmfTech.shortcuts import send_reset_password_email
from SmfTech.settings import FRONTEND_URL, SECRET_KEY
import jwt
import uuid
from django.contrib.auth.hashers import check_password

class RegisterView(APIView):
    
    def post(self, request):
        
        user_serializer = serializers.UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, user_pk=None):
        
        if pk:
            instance = get_object_or_404(models.Profile, id=pk)
            profile_serializer = serializers.ProfileSerializer(instance=instance)
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        
        if user_pk:
            user_instance = get_object_or_404(models.User, id=user_pk)
            profile_instance = get_object_or_404(models.Profile, user=user_instance)
            profile_serializer = serializers.ProfileSerializer(profile_instance)
            return Response(profile_serializer.data, status=status.HTTP_200_OK)

        queryset = models.Profile.objects.all()

        profile_serializer = serializers.ProfileSerializer(queryset, many=True)

        return Response(profile_serializer.data, status=status.HTTP_200_OK)


   
    def patch(self, request):
        
        user_instance = get_object_or_404(models.User, id=request.user.pk)
        profile_instance = get_object_or_404(models.Profile, user=user_instance)

        profile_serializer = serializers.ProfileSerializer(instance=profile_instance, data=request.data, partial=True)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        
        if pk:
            user_instance = get_object_or_404(models.User, id=pk)
            user_serializer = serializers.UserSerializer(user_instance)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        queryset = models.User.objects.all()
        users_serializer = serializers.UserSerializer(queryset, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        
        user_serializer = serializers.UserSerializer(request.user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    
    def post(self, request):
        reset_password_serializer = serializers.ResetPasswordSerializer(data=request.data)

        if reset_password_serializer.is_valid():
            email = reset_password_serializer.validated_data['email']
            user = get_object_or_404(models.User, email=email)
            user: models.User|object = get_object_or_404(models.User, email=email)
            paylod = {
                'user' : user.pk,
                'uuid'  : str(uuid.uuid4())
            }
            token = jwt.encode(paylod, key=SECRET_KEY, algorithm='HS256')
            reset_password_url = f"{FRONTEND_URL}accounts/users/reset-password/confirm/{token}/"
            send_reset_password_email(reset_link=reset_password_url, user_email=email)
            
            return Response({'detail' : 'You will receive a password reset link in your email within 5 minutes.'}, status=status.HTTP_200_OK)

        return Response(reset_password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmResetPassword(APIView):
    
    def post(self, request, token):

        if models.ResetPasswordToken.objects.filter(token=token).exists():
            return Response({'detail' : 'That link already used, try again.'})
        
        paylod = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        user = get_object_or_404(models.User, id=paylod['user'])

        serializer = serializers.ResetPasswordConfirmation(data=request.data)

        if serializer.is_valid():
            if check_password(serializer.validated_data['new_password'], user.password):
                return Response({'detail' : 'Password cannot be the same as the previous password'})
            models.ResetPasswordToken.objects.create(token=token)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail' : 'password reseted successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ChangePasswordView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request: HttpRequest):
        
        user = request.user
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'detail' : 'old password is invalid'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail' : 'password has been changed successfully'}, status=status.HTTP_200_OK)    
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)