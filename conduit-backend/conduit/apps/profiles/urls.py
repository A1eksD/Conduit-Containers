from django.urls import re_path                # path reicht hier nicht wegen Regex
from .views import ProfileRetrieveAPIView, ProfileFollowAPIView

app_name = "profiles"                          # namespace = "profiles"

urlpatterns = [
    # Username wird per Regex abgefangen
    re_path(r"^profiles/(?P<username>\w+)/?$", ProfileRetrieveAPIView.as_view()),
    re_path(r"^profiles/(?P<username>\w+)/follow/?$", ProfileFollowAPIView.as_view()),
]
