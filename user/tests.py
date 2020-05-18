import json
import time

from django.test import TestCase, Client

from music.models import (
    Artist,
    Thumbnail,
    Type,
    Collection,
    Playlist,
    Media
)


class SignInViewTest(TestCase):
    maxDiff = None
    right_id = "110722951437071906833"
    wrong_id = "121432853094875398693"
    right_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk2MGE3ZThlODM0MWVkNzUyZjEyYjE4NmZhMTI5NzMxZmUwYjA0YzAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzIyOTUxNDM3MDcxOTA2ODMzIiwiZW1haWwiOiJhc3hkMTUzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiaVpWVGNiMXJ3MjkyX0JiQWJyUjYtQSIsIm5hbWUiOiLstZzspIDsmIEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2hTUlJDcVRGdnhVQ3VJbUNnMjZxalp1cjBUVzlZRlk4M1BpMFB3Vmc9czk2LWMiLCJnaXZlbl9uYW1lIjoi7KSA7JiBIiwiZmFtaWx5X25hbWUiOiLstZwiLCJsb2NhbGUiOiJrbyIsImlhdCI6MTU4OTc2OTM5NywiZXhwIjoxNTg5NzcyOTk3LCJqdGkiOiI4OTI4MDNkOTMxOTg0NTFlMjIxNTI5NDhlZDNmMDQ1ZjcxZTA0NTBmIn0.PtD1vHAMUy1u8xXC8lb474zdQbysm5DrNGHOBjaDedQ7_S9wuzHf1gAm_wJ2swwEfg6yioQveYiI2_2_c1Vvy9wM8VqWqeGIzgyUf-jCxDFLmMsLnSSV5zYS1qQYM3x9BriVU7abQ1tqAkcKtDZqUT-plKqjpFY2ElNaxoknGDXaoLqpkjWkeFnIu46uwqTg-a-dzm5zJf8Bmg5Fs5sxV9rTyTJsqroq98Cr6anTBdY6oKtkR6sg-cTM281K8Mhc1EnmpE4cNSYlgld4qVGELrGO3YJ4r8swYhgo8Mf_oETfZ7aXwhovvNBraz3gD7Mp8Vh7X4opLNVU1cBDU_15qw"
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjExMDcyMjk1MTQzNzA3MTkwNjgzMyJ9.fSlWgrLldmNSnJAAjQbzYwJDlesKkbC4fPmmcOdGO1I"

    def setUp(self):
        thumbnail = Thumbnail.objects.create(
            url='test_url'
        )

        artist = Artist.objects.create(
            name='test_artist',
            url='test_url',
            thumbnail=thumbnail,
        )

        type = Type.objects.create(
            name='test_type'
        )

        collection = Collection.objects.create(
            name='test_collection',
            thumbnail=thumbnail,
            type=type
        )

        playlist = Playlist.objects.create(
            name='test_playlist',
            artist=artist,
            thumbnail=thumbnail,
            type=type,
            collection=collection
        )

        Media(
            name='ra-mu-ne',
            length=time(minute=5, second=12),
            views=8320,
            url='roses.mp3',
            artist=artist,
            thumbnail=thumbnail,
            type=type,
            collection=collection,
            playlist=playlist
        ).save()

    def test_sign_in_success(self):
        client = Client()
        data = {"id": self.right_id, "token": self.right_token}
        response = client.post('/user/signin', json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['token'], self.jwt_token)

    def test_sign_in_wrong_id_token(self):
        client = Client()
        data = {"id": self.wrong_id, "token": self.right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_sign_in_with_wrong_key(self):
        client = Client()
        data = {"if": self.wrong_id, "tooken": self.right_token}
        response = client.post('/user/signin', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media(self):
        client = Client()
        data = {
            "media_id": 1
        }
        response = client.post('recent/media', data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)