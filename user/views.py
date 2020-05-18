import json
import requests
import jwt

from django.http import HttpResponse, JsonResponse
from django.views import View

from youtubemuzic_test.settings import SECRET_KEY
from music.models import (
    Media,
    Playlist
)
from .models import (
    User,
    RecentMedia,
    RecentPlaylist
)
from .utils import login_required


class GoogleSignInView(View):
    GOOGLE_AUTH_URL = 'https://oauth2.googleapis.com/tokeninfo?id_token='
    CORRECT_ISS_LIST = ['accounts.google.com', 'https://accounts.google.com']

    def post(self, request):
        try:
            data = json.loads(request.body)
            google_id = data['id']
            google_token = data['token']
            token_data = json.loads(requests.get(self.GOOGLE_AUTH_URL + google_token).text)

            if (token_data['iss'] not in self.CORRECT_ISS_LIST) or (
                    token_data['sub'] != google_id):
                return JsonResponse({'message': 'MODIFIED_TOKEN'}, status=401)

            user, created = User.objects.get_or_create(google_id=google_id)
            token = jwt.encode(
                {'id': user.id}, SECRET_KEY, 'HS256'
            ).decode('utf-8')
            # print(google_token)
            # print(token)
            return JsonResponse({'token': token}, status=200)

        except KeyError:
            return HttpResponse(status=400)


class StorageView(View):
    @login_required
    def get(self, request, user):
        print(user.id)
        return HttpResponse(status=200)


class RecentMediaView(View):
    @login_required
    def post(self, request, user):
        try:
            media_id = json.loads(request.body)['media_id']
            print(media_id)
            media = Media.objects.get(id=media_id)
            recent_media, created = RecentMedia.objects.get_or_create(user=user, media=media)
            if not created:
                recent_media.save()

            return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)
        except Media.DoesNotExist:
            return HttpResponse(status=404)


class RecentPlaylistView(View):
    @login_required
    def post(self, request, user):
        try:
            playlist_id = json.loads(request.body)['playlist_id']
            playlist = Playlist.objects.get(id=playlist_id)
            recent_playlist, created = RecentPlaylist.objects.get_or_create(user=user, playlist=playlist)
            if not created:
                recent_playlist.save()

            return HttpResponse(status=200)

        except KeyError:
            print('keyerror')
            return HttpResponse(status=400)
        except Media.DoesNotExist:
            return HttpResponse(status=404)

    # @login_required
    # def get(self, request, user):

