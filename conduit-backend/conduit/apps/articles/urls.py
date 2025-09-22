# conduit/apps/articles/urls.py   (NEU)

from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet,
    ArticlesFavoriteAPIView,
    ArticlesFeedAPIView,
    CommentsListCreateAPIView,
    CommentsDestroyAPIView,
    TagListAPIView,
)

app_name = "articles"                     # wichtig für namespace="articles"

router = DefaultRouter(trailing_slash=False)
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    # Router-Routen ( /api/articles , /api/articles/<slug> … )
    path("", include(router.urls)),

    # Feed (kein Regex nötig → path)
    path("articles/feed/", ArticlesFeedAPIView.as_view()),

    # Regex-Routen → re_path
    re_path(
        r"^articles/(?P<article_slug>[-\w]+)/favorite/?$",
        ArticlesFavoriteAPIView.as_view(),
    ),
    re_path(
        r"^articles/(?P<article_slug>[-\w]+)/comments/?$",
        CommentsListCreateAPIView.as_view(),
    ),
    re_path(
        r"^articles/(?P<article_slug>[-\w]+)/comments/(?P<comment_pk>\d+)/?$",
        CommentsDestroyAPIView.as_view(),
    ),

    # Tag-Liste
    path("tags/", TagListAPIView.as_view()),
]
