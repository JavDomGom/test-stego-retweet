from src import app_logger, twitter

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    api = twitter.get_api()

    # Así te traes los retweets de un usuario, por ejemplo los 10 últimos.
    twitter.get_user_timeline(api, 'WatchMeNow', 10)

    # Y así retuiteas usando el status, no el ID.
    twitter.retweet(api, '16846')
    twitter.retweet(api, '993643')
    twitter.retweet(api, '540600022')
    twitter.retweet(api, '153263220755402754')
    twitter.retweet(api, '164497520108646401')

    log.info('Finishing program.')


if __name__ == '__main__':
    main()
