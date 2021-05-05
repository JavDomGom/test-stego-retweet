from datetime import datetime as dt
from src import app_logger, twitter, codes

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    words = twitter.load_words('db/words.txt')

    """
    1. Creamos una lista de 1000 tweets que contengan el target "food", en
    inglés (en) y que sean hasta el año 2015.
    """
    tweets = twitter.get_tweets_list('food', 'en', '2015', 100)

    """
    2. Retweeteamos cada uno de los tweets de la lista especificando su ID.
    """
    api = twitter.get_api()

    for tw in tweets[:5]:  # Para pruebas rápidas solo los 5 primeros tweets.
        twitter.retweet(api, tw.id)

    """
    3. Te traes los retweets de un usuario, con un límite de hasta 10 (si los
    hubiera).
    """
    tweets = twitter.get_user_timeline(api, 'WatchMeNow', 10)

    """
    4. Ahora puedes hacer lo que quieras con cada retweet, por ejemplo sacar el
    epoch de cuando fue retweeteado e imrprimir alguna info. Ojo, los IDs de
    estos retweets no son los IDs de los tweets originales (los de 2015).
    """
    for tw in tweets:
        id = tw._json['id']
        created_at = tw._json['created_at']
        tw_epoch = int(
            dt.strptime(
                created_at, '%a %b %d %H:%M:%S +0000 %Y'
            ).timestamp()
        )
        print(f'id: {id}, created_at: {created_at}, tw_epoch: {tw_epoch}')

    # Probando encode/decode.
    now_epoch = int(dt.now().timestamp())
    code = codes.Code(now_epoch)

    num_enc = code.encode('Hola')
    print(code.decode(num_enc))


log.info('Finishing program.')


if __name__ == '__main__':
    main()
