# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = 'http://localhost/static/acubor/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/html/static/acubor/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://localhost/static/acubor/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'acubor',
        'USER': 'acubor',
        'PASSWORD': 'acubor',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
