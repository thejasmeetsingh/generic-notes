from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

import strings
from api.views.base import CustomAPIView
from api.utils import get_auth_token, error_response, success_response


class Singup(CustomAPIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request: Request):
        # Check if user with the given username already exists or not
        if User.objects.filter(username__exact=request.data["username"]).exists():
            return error_response(message=strings.USERNAME_ALREADY_EXISTS)

        # Create user object
        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data["password"]
        )

        # Generate JWT tokens for the user
        data = get_auth_token(user=user)

        return success_response(
            data=data, 
            message=strings.CREATE_SUCCESS.format("Account "),
            status_code=status.HTTP_201_CREATED,
        )


class Login(CustomAPIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request: Request):
        # Authenticate the user with the given credentials
        user = authenticate(request, username=request.data["username"], password=request.data["password"])
        
        if not user:
            return error_response(
                message=strings.INVALID_LOGIN_CREDENTIALS,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # Update the last login timestamp in user object
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Generate JWT tokens for the user
        data = get_auth_token(user=user)

        return success_response(data=data, message=strings.LOGIN_SUCCESS)


class RefreshToken(CustomAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request):
        # Pass request data to the serializer and check if token is valid or not
        serializer = self.serializer_class(data={"refresh": request.data["refresh"]})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return error_response(message=str(e))

        return success_response(data=serializer.validated_data, message=strings.TOKEN_REFRESH_SUCCESS)