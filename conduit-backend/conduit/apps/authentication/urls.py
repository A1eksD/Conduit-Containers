from django.urls import path, re_path          # NEU
from .views import (
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,
)

app_name = "authentication"                   # damit namespace = "authentication"

urlpatterns = [
    # einfache Pfade → path()
    path("user/",  UserRetrieveUpdateAPIView.as_view()),
    path("users/", RegistrationAPIView.as_view()),

    # Regex-Suffix optional? Dann re_path:
    re_path(r"^users/login/?$", LoginAPIView.as_view()),
]
