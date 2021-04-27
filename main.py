from datetime import datetime as dt
from src import app_logger, config

log = app_logger.get_logger(__name__)


def main():
    log.info('Starting program.')

    oauth = config.get_token()

    # users = config.get_users(
    #     oauth,
    #     ['TwitterDev', 'TwitterAPI'],
    #     ['created_at', 'name', 'description']
    # )

    tweets = config.get_tweets(
        oauth,
        ['1386398089108344832',
         '1386398088365953026',
         '1386398087904591873',
         '1386398085929070594',
         '1386398085077782532',
         '1386398084603662336'],
        ['created_at', 'text']
    )

    for tweet in tweets:
        created_at_epoch = dt.strptime(
            tweet["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        print(
            f'id: {tweet["id"]}\tcreated_at: {tweet["created_at"]} ({created_at_epoch.timestamp()})'  # noqa: E501
        )
        # print(f'text: {tweet["text"]}')

    log.info('Finishing program.')


if __name__ == '__main__':
    main()
