SECRET = {
    'secret': '8u*t9%4qqq@*7a4dxqi4jw-_xj)=b#&fp-@6&$ne)xi_%53lt#'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'youtubemuzic_test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci'
        }
    }
}
