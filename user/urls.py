from django.urls import path

from .views import (
    GoogleSignInView,
    StorageView,
    RecentMediaView,
    RecentPlaylistView
)

urlpatterns = [
    path('/signin', GoogleSignInView.as_view()),
    path('/storage', StorageView.as_view()),
    path('/recent/media', RecentMediaView.as_view()),
    path('/recent/playlist', RecentPlaylistView.as_view())
]
