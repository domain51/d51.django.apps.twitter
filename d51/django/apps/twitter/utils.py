from django.conf import settings as django_settings
from dolt.apis.twitter import Twitter
import oauth2

def get_key_and_secret(settings=django_settings):
    return (
        settings.D51_DJANGO['APPS']['TWITTER']['CONSUMER_KEY'],
        settings.D51_DJANGO['APPS']['TWITTER']['CONSUMER_SECRET'],
    )

def get_configured_consumer(settings=django_settings):
    return oauth2.Consumer(*get_key_and_secret(settings=settings))

def get_http_client(consumer=None, token=None, settings=django_settings):
    consumer = consumer if consumer else get_configured_consumer(settings=settings)
    return oauth2.Client(consumer, token)

def get_twitter(settings=django_settings, token=None):
    http = get_http_client(settings=settings, token=token)
    return Twitter(http=http)
