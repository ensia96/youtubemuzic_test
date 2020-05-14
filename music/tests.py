from datetime import time

from django.test import TestCase, Client

from .models import Media


class StreamViewTest(TestCase):
    def setUp(self):
        Media(
            name='ra-mu-ne',
            length=time(minute=5, second=12),
            views=8320,
            url='roses.mp3'
        ).save()

    def tearDown(self):
        Media.objects.all().delete()

    def test_get_success(self):
        client = Client()
        response = client.get('/music/1')

        self.assertEqual(response.status_code, 200)

    def test_get_404(self):
        client = Client()
        response = client.get('music/56473')

        self.assertEqual(response.status_code, 404)