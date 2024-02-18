import uuid

from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Note(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    shared_with = models.ManyToManyField(User, related_name="shared_notes")

    class Meta:
        ordering = ("-created_at",)


class VersionHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    old_description = models.TextField(max_length=2000)
    new_description = models.TextField(max_length=2000)

    class Meta:
        ordering = ("-created_at",)
