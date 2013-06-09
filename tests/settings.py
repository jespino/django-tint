import os

SECRET_KEY = "123"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

INSTALLED_APPS = [
    'tint'
]

MEDIA_URL = "/media/"
ROOT_URLCONF = "tests.urls"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

TINT_TRANSFORMATIONS = {
  'test1': [
      {
          "action": 'fit',
          "width": 1024,
          "height": 768,
          "align": 'center',
          "valign": 'middle',
      },
  ],
}

TINT_KEEP_IMAGES = False
TINT_KEEP_THUMBNAILS = False

ALLOWED_HOSTS = ["testserver"]
