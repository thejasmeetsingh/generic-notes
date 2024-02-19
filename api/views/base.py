from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response

import strings
from api.utils import success_response


class CustomAPIView(APIView):
    def handle_exception(self, exc):
        if isinstance(exc, KeyError):
            exc = serializers.ValidationError(detail={"message": f"{exc.args[0]} field is required"})
        return super().handle_exception(exc)


class CustomGenericAPIView(GenericAPIView):
    def handle_exception(self, exc):
        if isinstance(exc, KeyError):
            exc = serializers.ValidationError(detail={"message": f"{exc.args[0]} field is required"})
        return super().handle_exception(exc)


class CustomListAPIView(ListModelMixin):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {"status_code": status.HTTP_200_OK}

        if "results" in response.data:
            data.update(response.data)
        else:
            data["results"] = response.data

        data["message"] = kwargs.get("message")
        return Response(data)


class CustomCreateAPIView(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return success_response(
            data=response.data,
            message=kwargs.get("message", strings.CREATE_SUCCESS),
            status_code=status.HTTP_201_CREATED,
        )


class CustomRetrieveAPIView(RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(data=response.data, message=kwargs.get("message"))


class CustomUpdateAPIView(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return success_response(data=response.data, message=kwargs.get("message", strings.UPDATE_SUCESS))

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return success_response(data=response.data, message=kwargs.get("message", strings.UPDATE_SUCESS))


class CustomDeleteAPIView(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return success_response(data=response.data, message=kwargs.get("message", strings.DELETE_SUCCESS))
