import jwt

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from youtubemuzic_test.settings import SECRET_KEY
from .models import User


def login_required(func):
    def login_wrapper(self, request, *args, **kwargs):
        try:
            print("headers=",end=""),print(request.headers)
            print(args)
            print(kwargs)
            token = request.headers['token']
            user_id = jwt.decode(token, SECRET_KEY, algorithms='HS256')['id']
            user = get_object_or_404(User, id=user_id)
            return func(self, request, user)

        except KeyError:
            print('loginerror')
            return HttpResponse(status=400)

    return login_wrapper
