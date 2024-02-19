import uuid

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Note, VersionHistory


class NoteCreateTests(APITestCase):
    url = reverse("create-note")

    def setUp(self) -> None:
        User.objects.create_user(username="test_user", password="1234")
        self.client.login(username="test_user", password="1234")

    def tearDown(self) -> None:
        self.client.logout()

        User.objects.all().delete()
        Note.objects.all().delete()
    
    def test_create_note(self):
        data = {"description": "Lorem Ipsum"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg="Check response status code. Should be equal to 201"
        )

    def test_description_limit(self):
        data = {"description": "Lorem Ipsum" * 2000}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            msg="Check response status code. Should be equal to 400, Since the description length is more than 2000"
        )


class NoteDetailTests(APITestCase):
    url = None
    note = None

    def setUp(self) -> None:
        user = User.objects.create_user(username="test_user", password="1234")

        self.note = Note.objects.create(owner=user, description="Lorem Ipsum")
        self.client.login(username="test_user", password="1234")
        self.url = reverse("note-detail", kwargs={"pk": str(self.note.id)})

    def tearDown(self) -> None:
        self.client.logout()

        User.objects.all().delete()
        Note.objects.all().delete()

    def test_note_retrive(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200"
        )

    def test_note_retrive_invalid_id(self):
        response = self.client.get(
            reverse("note-detail", kwargs={"pk": str(uuid.uuid4())}),
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            msg="Check response status code. Should be equal to 400, Since we are intentially passing an invalid ID"
        )

    def test_note_update(self):
        data = {"description": "Lorem Ipsum 1"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200"
        )

        # refresh note object
        self.note.refresh_from_db()

        self.assertEqual(
            self.note.description,
            "Lorem Ipsum 1",
            msg="Check if description is updated in DB"
        )

    def test_note_version_history_creation(self):
        data = {"description": "Lorem Ipsum 2"}
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200"
        )

        self.assertTrue(
            VersionHistory.objects.filter(note_id=response.data["data"]["id"]).exists(),
            msg="Check is version hisotry record is created related to the given note object"
        )


class ShareNoteTests(APITestCase):
    url = reverse("share-note")
    note = None

    def setUp(self) -> None:
        user1 = User.objects.create_user(username="test_user", password="1234")

        self.note = Note.objects.create(owner=user1, description="Lorem Ipsum")
        self.client.login(username="test_user", password="1234")

    def tearDown(self) -> None:
        self.client.logout()

        User.objects.all().delete()
        Note.objects.all().delete()

    def test_share_note(self):
        # Create a different user to share the note with
        user = User.objects.create_user(username="another_user", password="1234")

        data = {"note_id": str(self.note.id), "usernames": '["another_user"]'}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200."
        )

        self.assertTrue(
            self.note.shared_with.filter(id=user.id).exists(),
            msg="Check shared user is associated with the note object in DB"
        )

        # Logout previous user
        self.client.logout()

        # Login shared user
        self.client.login(username="another_user", password="1234")

        note_detail_url = reverse("note-detail", kwargs={"pk": str(self.note.id)})

        # Check if the shared user has access to the note or not
        response = self.client.get(note_detail_url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200."
        )

        # Check if the shared user can update the note
        response = self.client.put(note_detail_url, {"description": "Lorem Ipsum 3"}, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg="Check response status code. Should be equal to 200."
        )

        # Refresh the note object
        self.note.refresh_from_db()

        self.assertEqual(
            self.note.description,
            "Lorem Ipsum 3",
            msg="Check if description is updated in DB"
        )

    def test_note_accessiblity_without_share(self):
        # Logout the previous user
        self.client.logout()

        # Create a different user
        User.objects.create_user(username="some_other_user1", password="1234")

        # Login the other user
        self.client.login(username="some_other_user1", password="1234")
        
        note_detail_url = reverse("note-detail", kwargs={"pk": str(self.note.id)})
        response = self.client.get(note_detail_url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg="Check response status code. Should be equal to 403, Since we are using a different user (which does not have the access) to retrive the note"
        )
    
    def test_note_update_without_share(self):
        # Logout the previous user
        self.client.logout()

        # Create a different user
        User.objects.create_user(username="some_other_user2", password="1234")

        # Login the other user
        self.client.login(username="some_other_user2", password="1234")

        note_detail_url = reverse("note-detail", kwargs={"pk": str(self.note.id)})
        response = self.client.put(note_detail_url, {"description": "I can update anything!"} , format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg="Check response status code. Should be equal to 403, Since we are using a different user (which does not have the access) to update the note"
        )
