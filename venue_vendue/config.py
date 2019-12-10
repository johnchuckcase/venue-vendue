import logging
import os
import sys
from dotenv import load_dotenv
load_dotenv()

env = os.environ.get('ENV', 'default')

if 'pytest' in sys.modules or 'py.test' in sys.modules:
    env = 'test'


def get_postgres_vars(service='VENUE-VENDUE', testing=False):
    host = os.environ.get(f'{service}_HOST', 'localhost')
    port = os.environ.get(f'{service}_PORT', '1234')
    user = os.environ.get(f'{service}_USER', 'test_user')
    password = os.environ.get(f'{service}_PASSWORD', 'test_password')
    db_name_key = f'{service}_TEST_DATABASE' if testing else f'{service}_DATABASE'
    db_name = os.environ.get(db_name_key, f'test_venue_vendue' if testing else 'venue_vendue')
    return host, port, user, password, db_name


def get_postgres_url(service='VENUE-VENDUE', testing=False):
    host, port, user, password, db_name = get_postgres_vars(service, testing)
    return f'postgresql://{user}:{password}@{host}:{port}/{db_name}'


class BaseConfig:
    DEBUG = False
    ENV = env
    SQLALCHEMY_DATABASE_URI = get_postgres_url()


class DevConfig(BaseConfig):
    LOGGING_LEVEL = logging.DEBUG


class ProdConfig(BaseConfig):
    SHOULD_ALERT = True


class SandboxConfig(BaseConfig):
    DEBUG = True
    SHOULD_ALERT = True


class StageConfig(BaseConfig):
    SHOULD_ALERT = True


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = get_postgres_url(testing=True)
    TESTING = True


configs = {
    'default': DevConfig,
    'dev': DevConfig,
    'prod': ProdConfig,
    'sandbox': SandboxConfig,
    'stage': StageConfig,
    'test': TestConfig
}


settings = configs[env]
