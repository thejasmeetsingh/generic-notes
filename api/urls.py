from django.urls import path

from api.views import auth, notes


urlpatterns = [
    # Auth API Endpoints
    path("singup/", auth.Singup.as_view()),
    path("login/", auth.Login.as_view()),
    path("refresh-token/", auth.RefreshToken.as_view()),
    path("user/", auth.UserList.as_view()),

    # Note API Endpoints
    path("notes/create/", notes.CreateNote.as_view()),
    path("notes/share/", notes.ShareNote.as_view()),
    path("notes/version-history/<str:note_id>/", notes.VersionHisotryList.as_view()),
    path("notes/<str:pk>/", notes.NoteDetail.as_view()),
]