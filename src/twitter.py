import tweepy

from datetime import datetime as dt
from src import config, app_logger

log = app_logger.get_logger(__name__)


def get_api():
    """ Returns Twitter API object. """

    auth = tweepy.OAuthHandler(
        config.TWITTER_CONSUMER_KEY,
        config.TWITTER_CONSUMER_SECRET
    )
    auth.set_access_token(
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET
    )
    return tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )


def search_tweets(api, target):
    """ Returns a collection of relevant Tweets matching a specified query.

    Attributes:
        :api (Obj): Tweepy API client object.
        :target (str):      A UTF-8, URL-encoded search query of 500 characters
                            max including  operators. Queries  may additionally
                            be limited by complexity.
        :since_id (int):    Returns results  with an ID  greater than (that is,
                            more  recent  than)  the  specified  ID.  There are
                            limits  to  the  number  of  Tweets  which  can  be
                            accessed  through the API.  If the limit  of Tweets
                            has  occured since the  since_id, the since_id will
                            be forced to the oldest ID available.
    """

    log.info(f'Looking for tweets with target "{target}".')

    # Doc: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets  # noqa: E501
    for tweet in tweepy.Cursor(
        api.search,
        q=target,
        lang='en',
        result_type='recent',
        include_entities=False
    ).items(1):
        id = tweet._json['id']
        created_at = tweet._json['created_at']
        epoch = int(
            dt.strptime(
                created_at, '%a %b %d %H:%M:%S +0000 %Y'
            ).timestamp()
        )

        print(f'id: {id}, created_at: {created_at}, epoch: {epoch}')


def get_user_timeline(api, sender_twitter_user, count):
    """ This function prints the N (defined by count attribute) last retweets
    from a specific user timeline.

    Attributes:
        :api (Obj): Tweepy API client object.
        :sender_twitter_user (str): Sender twitter account name, without @.
        :count (int):               Number of recent retweets  to search hidden
                                    information.
    """

    log.debug(
        f'Looking for retweets in "{sender_twitter_user}" user timeline.'
    )
    retweets = api.user_timeline(sender_twitter_user, count=count)

    return reversed(retweets)


def retweet(api, id_or_status):
    """ Just retweet a tweet by ID or status (both are valid).

    Attributes:
        :api (Obj):             Tweepy API client object.
        :id_or_status (str):    ID from tweet to retweet.
    """

    api.retweet(id_or_status)
