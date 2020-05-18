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
            token = data['token']

            token_data = json.loads(requests.get(self.GOOGLE_AUTH_URL + token).text)

            if (token_data['iss'] not in self.CORRECT_ISS_LIST) or (
                    token_data['sub'] != google_id):
                return JsonResponse({'message': 'MODIFIED_TOKEN'}, status=401)

            user = User.objects.get_or_create(google_id=google_id)
            token = jwt.encode(
                {'id': user[0].id}, SECRET_KEY, 'HS256'
            ).decode('utf-8')
            print(token)

            return JsonResponse({'token': token}, status=200)

        except KeyError:
            return HttpResponse(status=400)


class StorageView(View):
    @login_required
    def get(self, request, user):
        print(user.id)
        return HttpResponse(status=200)


class RecentMedia(View):
    @login_required
    def post(self, request, user):
        try:
            media_id = request.body['media_id']
            media = Media.object.get(id=media_id)
            recent_media, created = RecentMedia.object.get_or_create(user=user, media=media)
            recent_media.save()
            print(recent_media.user.id)
            print(recent_media.media.id)
            return HttpResponse(status=200)

        except KeyError:
            return HttpResponse(status=400)
        except Media.DoesNotExist:
            return HttpResponse(status=404)

    @login_required
    def get(self, request, user):
        user.recent_media_set.all()

