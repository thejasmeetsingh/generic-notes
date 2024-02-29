from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Note, VersionHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "date_joined")


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("id", "description", "created_at", "modified_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Check if latest field preasent in the instance.
        # Add the old description value into the serialized data.
        data.update({"old_description": getattr(instance, "old_description", None)})
        return data

    def create(self, validated_data: dict):
        validated_data.update({"owner": self.context["request"].user})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        old_description = instance.description
        new_description = validated_data["description"]

        instance = super().update(instance, validated_data)

        # Create the version history record, Whenever any update action is performed on the note
        VersionHistory.objects.create(
            user=self.context["request"].user,
            note=instance,
            old_description=old_description,
            new_description=new_description,
        )

        return instance


class VersionHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = VersionHistory
        fields = (
            "id",
            "old_description",
            "new_description",
            "user",
            "note",
            "created_at",
        )
