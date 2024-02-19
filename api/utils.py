from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_auth_token(user: User):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def success_response(data: dict, message: str | None = None, status_code: int = status.HTTP_200_OK):
    return Response({"message": message, "data": data}, status=status_code)


def error_response(message: str, errors: dict | None = None, status_code: int = status.HTTP_400_BAD_REQUEST):
    return Response({"message": message, "errors": errors}, status=status_code)
