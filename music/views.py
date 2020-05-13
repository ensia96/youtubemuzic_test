import os

from django.http import StreamingHttpResponse
from django.views import View

<<<<<<< HEAD
#from pydub import AudioSegment
#
#
#class StreamView(View):
#    def iteration(self, source, times):
#        f = open(source, 'rb+')
#        f.seek(int(times))
#        while True:
#            c = f.read(512)
#            if c:
#                yield c
#            else:
#                break
#
#    def get(self, request):
#        audio = AudioSegment.from_file('roses.mp3')
#        durations = int(len(audio) / 1000)
#        size = os.path.getsize('roses.mp3')
#        size_per_sec = size / durations
#
#        seconds = 0
#        resp = StreamingHttpResponse(self.iteration('roses.mp3', size_per_sec * seconds), status=200,
#                                     content_type='audio/mp3')
#        resp['Cache-Control'] = 'no-cache'
#        resp['Accept-Ranges'] = 'bytes'
#
#        return resp
=======
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
>>>>>>> 28eecb65380ad467bb4f41f1eda919d009472a35
