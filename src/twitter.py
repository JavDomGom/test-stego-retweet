import tweepy

from src import config, app_logger

log = app_logger.get_logger(__name__)


def _get_api():
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


def get_searched_tweets(target, since_id):
    """ Returns a collection of relevant Tweets matching a specified query.

    Attributes:
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
    return [
        tweet for tweet in tweepy.Cursor(
            _get_api().search,
            q=target,
            lang='en',
            result_type='popular',
            since_id=since_id,
            include_entities=False
        ).items()
    ]
