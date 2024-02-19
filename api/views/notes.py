import json

from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.permissions import AllowAny

import strings
from api.views.base import (
    CustomAPIView,
    CustomGenericAPIView,
    CustomCreateModelMixin,
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
)
from api.serializers import NoteSerializer
from api.models import Note
from api.utils import success_response, error_response


class CreateNote(CustomGenericAPIView, CustomCreateModelMixin):
    serializer_class = NoteSerializer

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetail(CustomGenericAPIView, CustomRetrieveModelMixin, CustomUpdateModelMixin):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @transaction.atomic
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ShareNote(CustomAPIView):
    @transaction.atomic
    def post(self, request: Request):
        # Fetch the note object with the given ID
        note = Note.objects.filter(owner_id=request.user.id, id=request.data["note_id"]).first()
        if not note:
            return error_response(message=strings.INVALID_NOTE_ID)

        # Parse the usernames array
        usernames: list[str] = json.loads(request.data["usernames"])
        users = User.objects.filter(username__in=usernames)

        # Check if current user username is preasent in the usernames array
        if str(request.user.username) in usernames:
            return error_response(message=strings.CURRENT_USERNAME_ERROR)

        # Check if user exist w.r.t to each username that is passed
        if len(usernames) != users.count():
            return error_response(message=strings.INVALID_USER_IDS)

        # Associate given users with the note
        note.shared_with.add(*users)

        return success_response(data=usernames, message=strings.SHARE_NOTE_SUCCESS)
