from django.urls import path, include
from django.contrib import admin
from .views import *
from rest_framework_simplejwt import views as jwt_views
admin.autodiscover()


urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserRegister.as_view()),
    # path('user/activate/', UserActivate.as_view()),
    path('user/<int:user_id>/', UserDetail.as_view()),
    path('user/me/', UserDetail.as_view()),
    path('user/profile/', UserProfile.as_view()),
]