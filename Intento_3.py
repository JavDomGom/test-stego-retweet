import json
from datetime import datetime as dt
from src import app_logger, twitter, codes

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    """
    1. Creamos una lista de 100 tweets que contengan el target "food", en
    inglés (en) y que sean hasta el año 2015.
    """
    tweets = twitter.get_tweets_list('food', 'en', '2015', 100)

    """
    2. Por cada tweet comprobamos si contiene imágenes o no y si es un retweet
    o no.
    """

    for tw in tweets:
        photos = len(tw.photos)  # El valor es una lista, y puede estar vacía.
        retweet = tw.retweet  # Bool
        tweet = tw.tweet
        print(f'photos: {photos}, retweet: {retweet}, tweet: {tweet}')
        input('\nPress any key...\n')


log.info('Finishing program.')


if __name__ == '__main__':
    main()
