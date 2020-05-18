from django.urls import path

from .views import (
    GoogleSignInView,
    StorageView,
    RecentMedia
)

urlpatterns = [
    path('/signin', GoogleSignInView.as_view()),
    path('/storage', StorageView.as_view()),
    path('/recent/media', RecentMedia.as_view())
]
