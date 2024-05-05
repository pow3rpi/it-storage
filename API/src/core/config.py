# Validation settings
MIN_USERNAME_LENGTH: int = 3
MAX_USERNAME_LENGTH: int = 16
MIN_PWD_LENGTH: int = 8
MAX_PWD_LENGTH: int = 20
MIN_TITLE_LENGTH: int = 2
MAX_TITLE_LENGTH: int = 64
MIN_TAG_LENGTH: int = 2
MAX_TAG_LENGTH: int = 25
MAX_ANNOTATION_LENGTH: int = 250
USERNAME_ALLOWED_CHARS: str = '-_'
TAG_ALLOWED_CHARS: str = '-_.+#'
MAX_NAME_LENGTH: int = 20
MAX_TUTORIAL_SIZE: int = 1024 * 64
MAX_N_TAGS: int = 5

# Url settings
SIGN_UP_REDIRECT_URL: str = 'http://127.0.0.1:3000'

# Cookie settings
cookie_options = {
    'expires': 864000,  # 10 days (in sec)
    'httponly': True,
    'secure': True,
    'samesite': 'none'
}

# Search settings
MAX_SUGGESTED_TAGS: int = 80
MAX_POSTS_PER_PAGE: int = 20
MIN_SIMILARITY_SCORE: float = 0.25

# Logging settings
LOG_PATH = 'logs/'
LOG_SIZE_IN_BYTES = 15360  # 15 KB
N_LOGS = 9  # max number of log files
