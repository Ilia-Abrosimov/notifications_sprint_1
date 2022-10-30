"""Settings."""

import os

from dotenv import load_dotenv
from split_settings.tools import include, optional

load_dotenv()
ENV = os.environ.get('DJANGO_ENV', 'development')

base_settings = [
    'components/database.py',
    'components/base.py',
    f'environments/{ENV}.py',
    optional('environments/local.py'),
]

include(*base_settings)
