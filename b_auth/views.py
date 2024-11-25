from django.shortcuts import render
from django.db import transaction
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserSerializer, UserProfileSerializer


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = User.objects.get(username=request.data.get('username'))
        if not user.is_active:
            return Response(data={"error": 'Please activate your account before attempting to log in.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

class UserRegister(APIView):
    """
    API Endpoint to register users.
    METHODS: POST
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if request.auth is None:
            data = request.data
            data['is_active'] = False if settings.REGISTRATION_VERIFY_EMAILS else True
            serializer = UserRegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                    
                        # TODO: Implement email verification/account activation.
                        # subject = f"Activate your {settings.SERVICE_NAME} account."
                        # message = render_to_string('acc_active_email.html', {
                        #     'user': user,
                        #     'domain': request.META['HTTP_ORIGIN'],
                        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        #     'token': account_activation_token.make_token(user)
                        # })
                        
                        # send_confirmation_email(user.email, subject, message)

                        serialized_user = UserSerializer(user)
                        refresh = RefreshToken.for_user(user)
                        data = {'user':serialized_user.data,'refresh':str(refresh), 'access':str(refresh.access_token)}
                        return Response(data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserDetail(APIView):
    """
    API Endpoint to get the details for a user.
    METHODS: GET
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id='me', format=None):
        try:
            if user_id == 'me':
                user_id = request.user.pk
            user = User.objects.get(pk=user_id)
        except Exception as e:
            return Response({"error": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfile(APIView):
    """
    API Endpoint to get the a user's profile.

    METHODS: GET
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)