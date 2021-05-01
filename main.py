from datetime import datetime as dt
from src import app_logger, twitter, codes

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    api = twitter.get_api()

    # Así retuiteas usando el ID del mensaje original.
    # twitter.retweet(api, '550441077241430016')
    # twitter.retweet(api, '550440733417959424')
    # twitter.retweet(api, '550440426457796608')
    # twitter.retweet(api, '550439176462942210')

    # Y así te traes los retweets de un usuario, por ejemplo los 10 últimos.
    tweets = twitter.get_user_timeline(api, 'WatchMeNow', 10)

    now_epoch = int(dt.now().timestamp())
    code = codes.Code(now_epoch)

    for tw in tweets:
        id = tw._json['id']
        created_at = tw._json['created_at']
        tw_epoch = int(
            dt.strptime(
                created_at, '%a %b %d %H:%M:%S +0000 %Y'
            ).timestamp()
        )
        print(f'id: {id}, created_at: {created_at}, tw_epoch: {tw_epoch}')

        num_enc = code.encode('Hola')
        print(code.decode(num_enc))

    log.info('Finishing program.')


if __name__ == '__main__':
    main()
