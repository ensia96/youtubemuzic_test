import json

from django.test import TestCase, Client


class SignInViewTest(TestCase):
    maxDiff = None
    right_id = "110722951437071906833"
    wrong_id = "121432853094875398693"
    right_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImMxNzcxODE0YmE2YTcwNjkzZmI5NDEyZGEzYzZlOTBjMmJmNWI5MjciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzIyOTUxNDM3MDcxOTA2ODMzIiwiZW1haWwiOiJhc3hkMTUzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiMGlCSmdqR0ZadFljSFowcDVQdDYyUSIsIm5hbWUiOiLstZzspIDsmIEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy05SS10Vll0SDF0NC9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BTVp1dWNtNkZUTHZhdGVTcGRBdE5IamxXcVptMHJyVFRRL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiLspIDsmIEiLCJmYW1pbHlfbmFtZSI6Iuy1nCIsImxvY2FsZSI6ImtvIiwiaWF0IjoxNTg5NTM4MDExLCJleHAiOjE1ODk1NDE2MTEsImp0aSI6IjRkMGY5YTljNDM3MmNlZWQxZGE0YWIwODA3ZGMxOWMzM2Q4N2RiNGUifQ.nTw_XKwmAZoXBevNGCBTOU7GAiGm4zerVncpo_DY0X3m21sZQmW7EbxxBTOyhjKQ0iYP-Jty5cTdxqte45h1orTSPD4_Zrq9JXmcl7UCw9jNi6cXpGrIX7qlRjcNCqwxqQf3suYFgaXxHiqYN5NxVzsAszHKmcibxYNfD8-13zSJfrYAsM9GjCH5ObljqlF7chuE_P1dFgEiLxSSghtNlWmKPN_GEQnk5mBVj9KZxw0q933UZLecaZueB6OtW5yv_gOIS8UiMthdq9sQrEkyAHb4jCNutxJzFgs4PPohOqTBitBEvf0C4uIK_rinX4Zf2ScEv8PxDXFSnwVDaqyOJg"
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Mn0.uX_L1x4fkgETPa-D3Wr-TrPgzkw1XAvjVQPsCNHcXP8"

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
