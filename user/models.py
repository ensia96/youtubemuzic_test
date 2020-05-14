from django.db import models
from music.models import (
    Playlist,
    Media,
    Artist
)


class User(models.Model):
    google_id = models.CharField(max_length=50)

    class Meta:
        db_tables = 'users'


class ListStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)


class MediaStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    media = models.ForeignKey(Media, on_delete=models.PROTECT)


class RecentPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)


class RecentMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)


class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    media = models.ForeignKey(Media, on_delete=models.PROTECT)
    like_unlike = models.BooleanField()


class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)


