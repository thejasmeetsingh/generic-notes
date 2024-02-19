from django.urls import path

from api.views import auth, notes


urlpatterns = [
    # Auth API Endpoints
    path("singup/", auth.Singup.as_view(), name="singup"),
    path("login/", auth.Login.as_view(), name="login"),
    path("refresh-token/", auth.RefreshToken.as_view(), name="refresh-token"),
    path("user/", auth.UserList.as_view(), name="user-list"),

    # Note API Endpoints
    path("notes/create/", notes.CreateNote.as_view(), name="create-note"),
    path("notes/share/", notes.ShareNote.as_view(), name="share-note"),
    path("notes/version-history/<str:note_id>/", notes.VersionHisotryList.as_view(), name="note-version-history"),
    path("notes/<str:pk>/", notes.NoteDetail.as_view(), name="note-detail"),
]