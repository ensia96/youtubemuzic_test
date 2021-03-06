import os
import json
import random

from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.db.models import F
from pydub import AudioSegment

from .models import Collection, Playlist, Media, Artist, Type, Thumbnail, Hotlist


class RangeFileWrapper(object):

    def __init__(self, filelike, blksize, length=0):

        self.filelike = filelike
        self.blksize = blksize
        self.remaining = length

    def __iter__(self):

        return self

    def __next__(self):

        if self.remaining is None:

            data = self.filelike.read(self.blksize)

            if data:
                return data

            raise StopIteration()

        else:

            if self.remaining <= 0:
                raise StopIteration()

            data = self.filelike.read(min(self.remaining, self.blksize))

            if not data:
                raise StopIteration()

            self.remaining -= len(data)

            return data


class StreamView(View):
    MILISECOND_TO_SECOND = 1000

    def get(self, request, media_id):
        if not Media.objects.filter(id=media_id).exists():
            return HttpResponse(status=404)

        audio_source = 'roses.mp3'
        audio = AudioSegment.from_mp3(audio_source)
        playtime = len(audio) / self.MILISECOND_TO_SECOND
        size = os.path.getsize(audio_source)
        bytes_per_sec = int(size / playtime)

        resp = StreamingHttpResponse(
            RangeFileWrapper(
                open(
                    audio_source,
                    'rb+'
                ),
                bytes_per_sec * 10,
                size
            ),
            status=200,
            content_type='audio/mp3'
        )

        resp['Cache-Control'] = 'no-cache'

        return resp


class MainView(View):

    def get(self, request):

        range_list = [1, 7, 13]

        #        if user exists range_list=[1,6,2]

        if request.GET :
            range_list = request.GET.getlist('collection_id')

        collection = Collection.objects.prefetch_related('playlist_set')

        payload = {
            'contents':
                [
                    {
                        'collection': collection.filter(id=i).values('name').first()['name'],
                        'elements':
                            list(
                                collection.filter(id=i).annotate(
                                    list_id=F('playlist__id'),
                                    list_name=F('playlist__name'),
                                    list_thumb=F('playlist__thumbnail_id__url'),
                                    list_type=F('playlist__type_id__name'),
                                    list_artist=F('playlist__artist')
                                ).values(
                                    'list_id',
                                    'list_name',
                                    'list_thumb',
                                    'list_type',
                                    'list_artist'
                                )
                            )
                    }
                    for i in range_list
                ]
        }

        if not request.GET:
            payload[
                'main_thumb'
            ] = collection.filter(
                name=payload[
                    'contents'
                ][0][
                    'collection'
                ]
            ).values(
                'thumbnail_id__url'
            ).first()[
                'thumbnail_id__url'
            ]
            payload[
                'range_list'
            ]=random.sample(
                [3,4,8,10,12,15,16],
                6
            )

        return JsonResponse(
            payload,
            status=200
        )


class ListView(View):

    def get(self, request, list_id):
        playlist = Playlist.objects.filter(id=list_id).prefetch_related('media_set')

        return JsonResponse(
            {
                'list_meta': playlist.annotate(
                    list_name=F('name'),
                    list_desc=F('description'),
                    list_artist=F('artist'),
                    list_year=F('year'),
                    list_thumb=F('thumbnail_id__url'),
                    list_type=F('type_id__name')
                ).values(
                    'list_name',
                    'list_desc',
                    'list_artist',
                    'list_year',
                    'list_thumb',
                    'list_type'
                ).first(),
                'elements': list(
                    playlist.annotate(
                        item_id=F('media__id'),
                        item_thumb=F('media__thumbnail_id__url'),
                        item_name=F('media__name'),
                        item_artist=F('media__artist_id__name'),
                        item_album=F('media__album'),
                        item_length=F('media__length'),
                    ).values(
                        'item_id',
                        'item_thumb',
                        'item_name',
                        'item_artist',
                        'item_album',
                        'item_length',
                    )
                )
            },
            status=200
        )


class HotListView(View):

    def get(self, request):
        return JsonResponse(
            {
                'element': list(
                    Hotlist.objects.annotate(
                        thumb=F('thumbnail_id__url')
                    ).values(
                        'title',
                        'thumb',
                        'artist',
                        'views',
                    )
                )
            }
            , status=200
        )
