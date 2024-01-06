SECRET_KEY = 'django-insecure-u8u+3!$!jgw%!r9&g35%_3!=n%rv82d+4(b-wt*2=+b(!1um9g'

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistematestes',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
