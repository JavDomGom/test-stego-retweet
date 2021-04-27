import os

TRACE_LEVEL = os.getenv('TRACE_LEVEL', 'INFO')
LOG_PATH = os.getenv('LOG_PATH', 'log')
LOG_MAX_MEGABYTES = int(os.getenv('LOG_MAX_BYTES', 5))
LOG_MAX_FILES = int(os.getenv('LOG_MAX_FILES', 3))
LOG_FORMATTER = os.getenv(
    'LOG_FORMATTER',
    '%(asctime)-15s [%(levelname)s] %(funcName)s() %(message)s'
)

# Set your credentials:
TWITTER_CONSUMER_KEY = 'XXX'
TWITTER_CONSUMER_SECRET = 'XXX'
TWITTER_TOKEN = 'XXX'
TWITTER_TOKEN_SECRET = 'XXX'
