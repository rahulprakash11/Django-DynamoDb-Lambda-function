import os
import environ
from pathlib import Path
from corsheaders.defaults import default_methods
from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    "my-custom-header",
]


BASE_DIR = Path(__file__).resolve(strict=True).parent
env = environ.Env()
ENVIRONMENT = os.environ.get('ENV')
print("ENVIRONMENT :", ENVIRONMENT)
if ENVIRONMENT == 'local':
    env.read_env(str(BASE_DIR / '.env.local'))
    print("Inside local env")
    STATIC1_URL = 'static/' # if not local
    CORS_ALLOW_METHODS = list(default_methods)
    CORS_ALLOW_HEADERS = list(default_headers) + [
        "range",
    ]
    CORS_EXPOSE_HEADERS = ["Content-Range"]
    AWS_ACCESS_KEY_ID = env.str("AWS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET")

elif ENVIRONMENT == 'dev':
    print("Inside dev env")
    env.read_env(str(BASE_DIR / '.env.dev'))
    STATIC1_URL = '../static/' # if not local

elif ENVIRONMENT == 'prod':
    print("Inside prod env")
    env.read_env(str(BASE_DIR / '.env.production'))
    STATIC1_URL = '../static/' # if not local


DB_HOST = env.str('DB_HOST')
DB_REGION = env.str('DB_REGION')
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.str('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CORS_ALLOWED_URL = env.list('CORS_ALLOWED_ORIGINS')

# LOGGING_LEVEL = DJANGO_LOG_LEVEL
LOGGING_HANDLERS = env.list('LOGGING_HANDLERS')
DJANGO_LOG_LEVEL = env.str('DJANGO_LOG_LEVEL', 'INFO')
DJANGO_LOG_FILE = env.str('DJANGO_LOG_FILE')


if ENVIRONMENT == 'local':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': DJANGO_LOG_FILE,
                'formatter': 'verbose'
            },
            'console': {
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django': {
                'handlers': LOGGING_HANDLERS,
                'propagate': False,
                'level': DJANGO_LOG_LEVEL,
            },
            'app.products': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'app.productionLine': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'app.contactUs': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    }