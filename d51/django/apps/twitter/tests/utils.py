from d51.django.apps.twitter import utils
from d51.django.apps.twitter.tests.test import TestCase
from django.conf import settings
from dolt.apis import twitter as dolt
import oauth2
import random

class TestOfGetTwitterFunction(TestCase):
    def setUp(self):
        self.orig_settings = settings
        self.orig_settings.D51_DJANGO = {
            "APPS": {
                "TWITTER": {
                    "CONSUMER_KEY": "foobar",
                    "CONSUMER_SECRET": "barfoo",
                },
            },
        }

    def tearDown(self):
        settings = self.orig_settings

    def test_uses_provided_settings(self):
        random_key = "some random key %d" % random.randint(100, 200)
        random_secret = "ssh, some random secret %d" % random.randint(100, 200)

        my_settings = settings
        my_settings.D51_DJANGO['APPS']['TWITTER']['CONSUMER_KEY'] = random_key
        my_settings.D51_DJANGO['APPS']['TWITTER']['CONSUMER_SECRET'] = random_secret

        twitter = utils.get_twitter(my_settings)
        self.assertTrue(isinstance(twitter, dolt.Twitter), "sanity check")
        self.assertTrue(isinstance(twitter._http, oauth2.Client))

        self.assertEqual(random_key, twitter._http.consumer.key)
        self.assertEqual(random_secret, twitter._http.consumer.secret)

    def test_uses_default_credentials_when_none_are_provided(self):
        twitter = utils.get_twitter()
        self.assertEqual("foobar", twitter._http.consumer.key)
        self.assertEqual("barfoo", twitter._http.consumer.secret)
