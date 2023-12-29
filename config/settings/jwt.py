import datetime
from datetime import timedelta
from config.env import env

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days = 1)
}
