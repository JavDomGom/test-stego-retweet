import json
from datetime import datetime as dt
from src import app_logger, twitter, codes

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    # Transformo la lista de palabras a un conjunto (set), que es más rápido.
    words = set(twitter.load_words('db/words.txt'))

    """
    1. Creamos una lista de 100 tweets que contengan el target "food", en
    inglés (en) y que sean hasta el año 2015.
    """
    tweets = twitter.get_tweets_list('food', 'en', '2015', 100)

    """
    2. Por cada tweet comprobamos si contiene una o dos palabras, pero no más,
    de nuestro set de palabras.
    """

    for tw in tweets:
        match = 0
        tweet = tw.tweet.lower()
        for w in set(tweet.split()):
            if w.isalpha() and len(w) >= 4 and len(w) <= 18 and w in words:
                match += 1
            if match == 3:
                break

        if match in {1, 2}:
            print(
                {
                    'match': match,
                    'tweet': tweet
                }
            )
            log.info(f'Tweet with ID "{tw.id}" optimal to work.')
            input('\nPress any key...\n')


log.info('Finishing program.')


if __name__ == '__main__':
    main()
