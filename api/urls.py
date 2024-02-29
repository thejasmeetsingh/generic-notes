from django.urls import path

from api.views import auth, notes


urlpatterns = [
    # Auth API Endpoints
    path("singup/", auth.Singup.as_view(), name="singup"),
    path("login/", auth.Login.as_view(), name="login"),
    path("refresh-token/", auth.RefreshToken.as_view(), name="refresh-token"),
    path("user/", auth.UserList.as_view(), name="user-list"),

    # Note API Endpoints
    path("note/", notes.NoteList.as_view(), name="note-list"),
    path("note/share/", notes.ShareNote.as_view(), name="share-note"),
    path("note/version-history/<str:note_id>/", notes.VersionHisotryList.as_view(), name="note-version-history"),
    path("note/<str:pk>/", notes.NoteDetail.as_view(), name="note-detail"),
]