from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'collections'


class Type(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'types'


class Playlist(models.Model):
    name = models.CharField(max_length=40)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    thumbnail = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)
    artist = models.ForeignKey('Artist', on_delete=models.PROTECT)

    class Meta:
        db_table = 'playlists'


class Thumbnail(models.Model):
    url = models.CharField(max_length=300)

    class Meta:
        db_table = 'thumbnails'


class Artist(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=300)
    thumbnail = models.ForeignKey(Thumbnail, on_delete=models.PROTECT)

    class Meta:
        db_table = 'artists'


class Song(models.Model):
    name = models.CharField(max_length=100)
    play_time = models.TimeField()
    url = models.CharField(max_length=300)
    thumbnail = models.ForeignKey(Thumbnail, on_delete=models.PROTECT)
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)

    class Meta:
        db_table = 'songs'


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.PROTECT)
    song = models.ForeignKey(Song, on_delete=models.PROTECT)

    class Meta:
        db_table = 'playlist_songs'


class Attribute(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'attributes'


class SongAttribute(models.Model):
    song = models.ForeignKey(Song, on_delete=models.PROTECT)
    attribute = models.ForeignKey(Attribute, on_delete=models.PROTECT)

    class Meta:
        db_table = 'song_attributes'
