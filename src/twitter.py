import tweepy
import twint

from src import config, app_logger

log = app_logger.get_logger(__name__)


def get_tweets_list(target, lang, year, limit):
    """ Returns a list of tweets according to the search parameters.

    Attributes:
        :target (str):  Search terms.
        :lang (str):    Compatible language codes: https://github.com/twintproject/twint/wiki/Langauge-codes  # noqa: E501
        :year (str):    Filter Tweets before the specified year.
        :limit (int):   Number of Tweets to pull (Increments of 100).
    """

    log.info(f'Looking for {limit} tweets with target "{target}", lang "{lang}" and before "{year}".')  # noqa: E501

    c = twint.Config()
    c.Search = target
    c.Lang = lang
    c.Year = year
    c.Limit = limit
    c.Hide_output = True
    c.Store_object = True

    twint.run.Search(c)

    return twint.output.tweets_list


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


def retweet(api, id):
    """ Just retweet a tweet by ID.

    Attributes:
        :api (Obj): Tweepy API client object.
        :id (str):  ID from tweet to retweet.
    """

    try:
        api.retweet(id)
        log.info(f'Tweet with id "{id}" successfully retweeted!')
    except Exception as e:
        log.warning(e)


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
