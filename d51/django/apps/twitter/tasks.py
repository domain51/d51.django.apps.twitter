from celery.decorators import task
from celery.task import Task
from d51.django.apps.twitter.models import TwitterUser, get_twitter

@task
def sync_user(twitter_id, source=None, crawl_mode=False):
    logger = Task.get_logger()
    logger.info("[sync_user] starting sync_user(%s)" % twitter_id)
    try:
        user = TwitterUser.objects.get(id__exact=str(twitter_id))
    except TwitterUser.DoesNotExist:
        user = TwitterUser(id=twitter_id)
    user.update_from_twitter()
    user.save()
    if source:
        user.follow(source)

    if crawl_mode and user.screen_name:
        crawl.delay(screen_name=user.screen_name)
    else:
        logger.info("[sync_user] got a user with an empty name")
    return user

@task
def crawl(id=None, screen_name=None, cursor=-1, crawl_mode=False):
    logger = Task.get_logger()
    logger.info('[crawl] starting crawl(id=%s, screen_name=%s, cursor=%s)' % (id, screen_name, cursor))
    twitter = get_twitter()
    params = {
        "cursor": cursor
    }
    if id:
        params['user_id'] = id
    elif screen_name:
        params['screen_name'] = screen_name
    result = twitter.followers.ids(**params)

    # block while we grab the current user's info
    del params['cursor']
    source_id = twitter.users.show(**params)['id']
    source = sync_user(source_id)

    for id in result['ids']:
        sync_user.delay(id, source=source, crawl_mode=crawl_mode)

    if result['next_cursor']:
        logger.info("[crawl] continuing at next_cursor=%s" % result['next_cursor'])
        crawl.delay(twitter_id, cursor=result['next_cursor'], crawl_mode=crawl_mode)



