from d51.django.apps.twitter import utils
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import simplejson

def create(request, id=None, twitter=None, format='json'):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST', ])

    twitter = twitter if twitter else utils.get_twitter(token=request.user.twitter.get_oauth_token())
    if id:
        result = getattr(twitter.friendships.create, id).POST()
    else:
        get_params = {}
        user_id = request.GET.get('user_id')
        if user_id:
            get_params['user_id'] = user_id
        screen_name = request.GET.get('screen_name')
        if screen_name:
            get_params['screen_name'] = screen_name
        result = twitter.friendships.create.POST(**get_params)

    # TODO: add support for serializing to XML
    return HttpResponse(simplejson.dumps(result))

