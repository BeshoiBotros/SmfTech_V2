from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # tokens urls
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    
    # registeration url
    path('register/', views.RegisterView.as_view()),

    # profiles urls
    path('profile/', views.ProfileView.as_view()),
    path('profile/<int:pk>/', views.ProfileView.as_view()),
    path('profile/user/<int:user_pk>/', views.ProfileView.as_view()),

    # users urls
    path('users/', views.UserView.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
    path('users/change-password/', views.ChangePasswordView.as_view()),
    path('users/reset-password/', views.ResetPasswordView.as_view()),
    path('users/reset-password/confirm/<str:token>/', views.ConfirmResetPassword.as_view()),
]