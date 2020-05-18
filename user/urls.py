from django.urls import path

from .views import (
    GoogleSignInView,
    StorageView
)

urlpatterns = [
    path('/signin', GoogleSignInView.as_view()),
    path('/storage', StorageView.as_view())
]
