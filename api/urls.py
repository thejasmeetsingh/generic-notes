from django.urls import path

from api.views import auth, notes


urlpatterns = [
    # Auth API Endpoints
    path("singup/", auth.Singup.as_view()),
    path("login/", auth.Login.as_view()),
    path("refresh-token/", auth.RefreshToken.as_view()),
]