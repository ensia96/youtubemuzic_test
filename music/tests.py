from django.test import TestCase, Client


class StreamViewTest(TestCase):
    def test_get_success(self):
        client = Client()
        response = client.get('/music')

        self.assertEqual(response.status_code, 200)
