from django.test import TestCase, Client

class StreamViewTest(TestCase):
    def test_get_success(self):
        client = Client()
        response = client.get('/music/1')

        self.assertEqual(response.status_code, 200)

    def test_get_404(self):
        client = Client()
        response = client.get('/muzic/')

        self.assertEqual(response.status_code, 404)
