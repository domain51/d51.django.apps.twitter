from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'd51.django.apps.twitter.api',
    url(r'friendships/create(/(?P<id>.*))?(\.(?P<format>xml|json))?$', 'friendships.create', name='twitter_friendships_create'),
)
