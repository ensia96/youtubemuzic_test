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
    path('/recent/media/<int:media_id>', RecentMediaView.as_view()),
    path('/recent/playlist/<int:playlist_id>', RecentPlaylistView.as_view())
]
