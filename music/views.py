import os

from django.http import StreamingHttpResponse
from django.views import View

from pydub import AudioSegment


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize, length = 0):
        self.filelike = filelike
        self.blksize = blksize
        self.remaining = length

    def __close__(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


class StreamView(View):
    MILISECOND_TO_SECOND = 1000

    def get(self, request):
        audio = AudioSegment.from_mp3('roses.mp3')
        playtime = len(audio) / self.MILISECOND_TO_SECOND
        size = os.path.getsize('roses.mp3')
        bytes_per_sec = int(size / playtime)

        resp = StreamingHttpResponse(RangeFileWrapper(open('roses.mp3', 'rb+'), bytes_per_sec, size),
                                     status=200, content_type='audio/mp3')

        return resp