import json

from django.test import TestCase, Client


class SignInViewTest(TestCase):
    maxDiff = None
    right_id = "110722951437071906833"
    wrong_id = "121432853094875398693"
    right_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImMxNzcxODE0YmE2YTcwNjkzZmI5NDEyZGEzYzZlOTBjMmJmNWI5MjciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNTYzODgyMTA5MDUxLTF2bTZudmF1NzQ4c28zNmdkbXBram0wMjhoMjI0N2FzLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwNzIyOTUxNDM3MDcxOTA2ODMzIiwiZW1haWwiOiJhc3hkMTUzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiazVPMnRPbUQ3R0JuWGFpYnE0VFYzQSIsIm5hbWUiOiLstZzspIDsmIEiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDUuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy05SS10Vll0SDF0NC9BQUFBQUFBQUFBSS9BQUFBQUFBQUFBQS9BTVp1dWNtNkZUTHZhdGVTcGRBdE5IamxXcVptMHJyVFRRL3M5Ni1jL3Bob3RvLmpwZyIsImdpdmVuX25hbWUiOiLspIDsmIEiLCJmYW1pbHlfbmFtZSI6Iuy1nCIsImxvY2FsZSI6ImtvIiwiaWF0IjoxNTg5NTI1MDE0LCJleHAiOjE1ODk1Mjg2MTQsImp0aSI6IjEwNWY4MGE0M2Q3MDQ1YWNmYWQwZmRkY2RmNGE3YWNkMWYwYmI0OGMifQ.K9gTgFTTqU2BDhWVAuYGpr4hF2-9vTySj7K9I7cTZo2NLqleTmQR87lvM5SSLtbWuv3GX7eHNgrw_JBSubJYQjsiXYsvsO8ZVNmKlhPMvDFbuyMKL1dm1-ZxWtjukX7KLlyCEd5GDHrz4AU_BcaqU_NZGYop85rpk4K0yvOpIqXZ1oj1xq5XdU82baWSk0QQ2EpHok0XazzgDe7KxqsPuaIVFI3nb-l5mfwtg6bENsFORTMplq2bMOBZTjkD8FJ1nXzvHArEu6ngQTAtcNDW5xE--UyOYk6Vp4nhNiEOh60l_ib8NwRFbtBRVS-KPBagHuPQO--QI0PNpK6ombbF7w'
    jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjExMDcyMjk1MTQzNzA3MTkwNjgzMyJ9.fSlWgrLldmNSnJAAjQbzYwJDlesKkbC4fPmmcOdGO1I"

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
