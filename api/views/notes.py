import json

from django.db import transaction
from django.db.models import Q, Subquery, OuterRef
from django.contrib.auth.models import User
from rest_framework.request import Request

import strings
from api.views.base import (
    CustomAPIView,
    CustomGenericAPIView,
    CustomListModelMixin,
    CustomCreateModelMixin,
    CustomRetrieveModelMixin,
    CustomUpdateModelMixin,
)
from api.serializers import NoteSerializer, VersionHistorySerializer
from api.models import Note, VersionHistory
from api.utils import success_response, error_response


class NoteBaseView(CustomGenericAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(owner_id=self.request.user.id) | 
            Q(shared_with__id=self.request.user.id)
        )


class NoteList(NoteBaseView, CustomListModelMixin, CustomCreateModelMixin):
    def get_queryset(self):
        # Fetch latest note log and associate with each note record respectively
        note_logs = VersionHistory.objects.only("old_description").filter(note_id=OuterRef("id")).order_by("-created_at")
        return super().get_queryset().annotate(old_description=Subquery(note_logs.values("old_description")[:1]))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetail(NoteBaseView, CustomRetrieveModelMixin, CustomUpdateModelMixin):
    # permission_classes = (CanReadOrUpdateNote,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
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


class VersionHisotryList(CustomGenericAPIView, CustomListModelMixin):
    queryset = VersionHistory.objects.select_related("user", "note")
    serializer_class = VersionHistorySerializer

    def get_queryset(self):
        # Filter the version hisotry records based on the given note_id
        return super().get_queryset().filter(
            Q(note__owner_id=self.request.user.id) | 
            Q(note__shared_with__id=self.request.user.id),
            note_id=self.kwargs["note_id"]
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
