from datetime import datetime as dt
from src import app_logger, twitter, codes

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    tweets = twitter.get_searched_tweets(
        target='food',
        since_id=12345678
    )
    now_epoch = int(dt.now().timestamp())
    code = codes.Code(now_epoch)

    for tweet in tweets:
        id = tweet._json['id']
        created_at = tweet._json['created_at']
        epoch = int(
            dt.strptime(
                created_at, '%a %b %d %H:%M:%S +0000 %Y'
            ).timestamp()
        )

        print(f'id: {id}, created_at: {created_at}, epoch: {epoch}')

        code.encode('Hola')
        print(code.decode(epoch))

    log.info('Finishing program.')


if __name__ == '__main__':
    main()
