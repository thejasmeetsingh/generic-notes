from rest_framework.permissions import BasePermission

import strings


class CanReadOrUpdateNote(BasePermission):
    message = strings.NOTE_PERMISSION_ERROR

    def has_object_permission(self, request, _, obj):
        """
        Return True if current user is either the owner of the note or have access to the note via note share,
        Else return False.
        """

        return obj.owner_id == request.user.id or obj.shared_with.filter(id=request.user.id).exists()
