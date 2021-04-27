import sys

from requests_oauthlib import OAuth1Session

from src import config, app_logger

log = app_logger.get_logger(__name__)


def get_token():
    consumer_key = config.TWITTER_CONSUMER_KEY
    consumer_secret = config.TWITTER_CONSUMER_SECRET
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        print(
            'There may have been an issue with the consumer_key or consumer_secret you entered.'  # noqa: E501
        )

    log.info('Looking for access token.')
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    print(f'Got OAuth token: {resource_owner_key}')

    log.info('Request authorization.')
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    print(f'Please go here and authorize: {authorization_url}')
    verifier = input('Paste the PIN here: ')

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    log.info('Got access token!')

    return OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_tokens['oauth_token'],
        resource_owner_secret=oauth_tokens['oauth_token_secret'],
    )


def get_users(oauth, usernames, user_fields):
    """ Return a list of users.

    Attributes:
        :oauth (Object):    OAuth1Session object with access token.
        :usernames (lst):   List of users to get.
        :user_fields (lst): List of  user fields to include in response. Values
                            can  be:  created_at,  description,  entities,  id,
                            location, name, pinned_tweet_id, profile_image_url,
                            protected, public_metrics, url, username, verified,
                            and withheld.
    """

    params = {
        'usernames': ','.join(usernames),
        'user.fields': ','.join(user_fields)
    }

    response = oauth.get(
        'https://api.twitter.com/2/users/by',
        params=params
    )

    if response.status_code != 200:
        error = f'Error: {response.status_code} {response.text}'
        log.error(error)
        raise Exception(error)

    log.info(f'Response code: {response.status_code}')

    if 'data' in response.json():
        return response.json()['data']
    else:
        log.error(response.json())
        print(response.json())
        sys.exit(1)


def get_tweets(oauth, ids, tweet_fields):
    """ Return a list of users.

    Attributes:
        :oauth (Object):        OAuth1Session object with access token.
        :ids (lst):             List of tweets IDs.
        :tweet_fields (lst):    List  of tweet fields  to include  in response.
                                Values can be: attachments, author_id, geo, id,
                                context_annotations, conversation_id, entities,
                                created_at,  in_reply_to_user_id,  text,  lang,
                                non_public_metrics,  referenced_tweets, source,
                                organic_metrics,  possibly_sensitive, withheld,
                                promoted_metrics and public_metrics.
    """

    params = {
        'ids': ','.join(ids),
        'tweet.fields': ','.join(tweet_fields)
    }

    response = oauth.get(
        'https://api.twitter.com/2/tweets',
        params=params
    )

    if response.status_code != 200:
        error = f'Error: {response.status_code} {response.text}'
        log.error(error)
        raise Exception(error)

    log.info(f'Response code: {response.status_code}')

    if 'data' in response.json():
        return response.json()['data']
    else:
        log.error(response.json())
        print(response.json())
        sys.exit(1)
