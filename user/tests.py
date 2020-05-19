import json
import time

from django.test import TestCase, Client

from user.models import User


class SignInViewTest(TestCase):
    maxDiff = None
    right_id = "110722951437071906833"
    wrong_id = "121432853094875398693"
    right_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk2MGE3ZThlODM0MWVkNzUyZjEyYjE4NmZhMTI5NzMxZmUwYjA0YzAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzIyOTUxNDM3MDcxOTA2ODMzIiwiZW1haWwiOiJhc3hkMTUzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoia2EzYjUwS2dkMUdFVzVIeGZlUDVYZyIsIm5hbWUiOiLstZzspIDsmIEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2hTUlJDcVRGdnhVQ3VJbUNnMjZxalp1cjBUVzlZRlk4M1BpMFB3Vmc9czk2LWMiLCJnaXZlbl9uYW1lIjoi7KSA7JiBIiwiZmFtaWx5X25hbWUiOiLstZwiLCJsb2NhbGUiOiJrbyIsImlhdCI6MTU4OTc4ODg1MiwiZXhwIjoxNTg5NzkyNDUyLCJqdGkiOiJmN2I1N2QyMThjZTY0OTcwYjlhNmFhNjU1OWYyMDdiMjg2NDkyMzNkIn0.fIESOiCvAzKBdrK3S051yrOvP0QqbS9l2BfrH4v9c1zRarUBMH_tpeEiBJtJVJgdFWIGHz-Nr-T7f1J-H0oocIEghfFT-7gtdgHjjJ0s7uyRtQW0NROSmYDgzlwSY4nzUouwwTfL8wmYW7OlCQkXxZoNwUUyFq4ALMABVwdgNhhKHaR8UEN_D6iYrKYiJ4xswdQg37RRy897PMc3YOoi39UvKsF_z4t3WJ7aVjwWGvqUpcc9wIsJvke21E5IyHZKuO42Dneh80y31nWUt8tHEGvOtVJ32PvlrclCevDL8LsI5zgw73D96b_ntAd5r6uUh7IwMuKOqfK_4nmWs8XemA"
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjV9.3QK2UMqDzxSwXReg0IbjeBiuoLVQsG57Tw818QlesSI"

    def setUp(self):
        User(
            google_id='2314324'
        ).save()

    def tearDown(self):
        User.objects.get(google_id='2314324').delete()

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


class RecentViewTest(TestCase):
    right_id = "110722951437071906833"
    wrong_id = "121432853094875398693"
    right_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk2MGE3ZThlODM0MWVkNzUyZjEyYjE4NmZhMTI5NzMxZmUwYjA0YzAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzIyOTUxNDM3MDcxOTA2ODMzIiwiZW1haWwiOiJhc3hkMTUzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoia2EzYjUwS2dkMUdFVzVIeGZlUDVYZyIsIm5hbWUiOiLstZzspIDsmIEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2hTUlJDcVRGdnhVQ3VJbUNnMjZxalp1cjBUVzlZRlk4M1BpMFB3Vmc9czk2LWMiLCJnaXZlbl9uYW1lIjoi7KSA7JiBIiwiZmFtaWx5X25hbWUiOiLstZwiLCJsb2NhbGUiOiJrbyIsImlhdCI6MTU4OTc4ODg1MiwiZXhwIjoxNTg5NzkyNDUyLCJqdGkiOiJmN2I1N2QyMThjZTY0OTcwYjlhNmFhNjU1OWYyMDdiMjg2NDkyMzNkIn0.fIESOiCvAzKBdrK3S051yrOvP0QqbS9l2BfrH4v9c1zRarUBMH_tpeEiBJtJVJgdFWIGHz-Nr-T7f1J-H0oocIEghfFT-7gtdgHjjJ0s7uyRtQW0NROSmYDgzlwSY4nzUouwwTfL8wmYW7OlCQkXxZoNwUUyFq4ALMABVwdgNhhKHaR8UEN_D6iYrKYiJ4xswdQg37RRy897PMc3YOoi39UvKsF_z4t3WJ7aVjwWGvqUpcc9wIsJvke21E5IyHZKuO42Dneh80y31nWUt8tHEGvOtVJ32PvlrclCevDL8LsI5zgw73D96b_ntAd5r6uUh7IwMuKOqfK_4nmWs8XemA"
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjV9.3QK2UMqDzxSwXReg0IbjeBiuoLVQsG57Tw818QlesSI"

    def setUp(self):
        User(
            google_id='2314324'
        ).save()

    def tearDown(self):
        User.objects.get(google_id='2314324').delete()

    def test_post_recent_media_success(self):
        client = Client()
        data = {
            "media_id": 2
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)

    def test_post_recent_playlist_success(self):
        client = Client()
        data = {
            "playlist_id": 2
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)

    def test_post_recent_media_login_failure(self):
        client = Client()
        data = {
            "media_id": 2
        }
        header = {'HTTP_authorization': 'dfgdsfg'}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_login_failure(self):
        client = Client()
        data = {
            "media_id": 5
        }
        header = {'HTTP_authorization': 'sdfgdfgs'}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_key_error(self):
        client = Client()
        data = {
            "media": 2
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_key_error(self):
        client = Client()
        data = {
            "list_id": 2
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_value_error(self):
        client = Client()
        data = {
            "media": 'dsfsd'
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_playlist_value_error(self):
        client = Client()
        data = {
            "media": '43534'
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 400)

    def test_post_recent_media_does_not_exist(self):
        client = Client()
        data = {
            "media_id": 1275417598
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/media', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 404)

    def test_post_recent_playlist_does_not_exist(self):
        client = Client()
        data = {
            "playlist_id": 59432708942
        }
        header = {'HTTP_authorization': self.jwt_token}
        response = client.post('/user/recent/playlist', data=data, content_type='application/json', **header)

        self.assertEqual(response.status_code, 404)