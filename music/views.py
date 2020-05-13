import os

from django.http import HttpResponse, StreamingHttpResponse
from django.views import View

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
