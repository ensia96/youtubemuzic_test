import os

from django.http import StreamingHttpResponse
from django.views import View

from pydub import AudioSegment


class StreamView(View):
    MILISECOND_TO_SECOND = 1000

    def iteration(self, file, bytes_per_sec):
        while True:
            c = file.read(bytes_per_sec)
            if c:
                yield c
            else:
                break

    def get(self, request):
        audio = AudioSegment.from_mp3('roses.mp3')
        playtime = len(audio) / self.MILISECOND_TO_SECOND
        size = os.path.getsize('roses.mp3')
        bytes_per_sec = int(size / playtime)

        resp = StreamingHttpResponse(self.iteration(open('roses.mp3', 'rb+'), bytes_per_sec),
                                     status=200, content_type='audio/mp3')

        return resp
