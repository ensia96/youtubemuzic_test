from django.db import models


class Collection(models.Model):
    name      = models.CharField(max_length=50)
    thumbnail = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)
    type      = models.ForeignKey('Type', on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'collections'


class Playlist(models.Model):
    name        = models.CharField(max_length=40)
    description = models.CharField(max_length=100)
    year        = models.IntegerField()
    artist      = models.ForeignKey('Artist', on_delete=models.PROTECT)
    thumbnail   = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)
    type        = models.ForeignKey('Type', on_delete=models.PROTECT)
    collection  = models.ForeignKey('Collection', on_delete=models.PROTECT)

    class Meta:
        db_table = 'playlists'


class Media(models.Model):
    name       = models.CharField(max_length=100)
    length     = models.TimeField()
    views      = models.IntegerField()
    url        = models.CharField(max_length=300)
    artist     = models.ForeignKey('Artist', on_delete=models.PROTECT)
    thumbnail  = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)
    collection = models.ForeignKey('Collection', on_delete=models.SET_NULL, null=True)
    playlist   = models.ForeignKey('Playlist', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'medias'


class Artist(models.Model):
    name        = models.CharField(max_length=200)
    description = models.CharField(max_length=300, null=True)
    url         = models.CharField(max_length=300)
    thumbnail   = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)

    class Meta:
        db_table = 'artists'


class Type(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'types'


class Thumbnail(models.Model):
    url = models.CharField(max_length=2000)

    class Meta:
        db_table = 'thumbnails'


class Hotlist(models.Model):
    title       = models.CharField(max_length=50)
    thumbnail   = models.ForeignKey('Thumbnail', on_delete=models.PROTECT)
    artist      = models.CharField(max_length=50)
    views       = models.CharField(max_length=10)
