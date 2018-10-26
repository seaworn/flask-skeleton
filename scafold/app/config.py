import os


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = os.environ.get('APP_NAME', 'App')
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a really hard to guess string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEVEL_URL', 'sqlite:///database-devel.sqlite3')


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'sqlite:///database-test.sqlite3')


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PRO_URL', 'sqlite:///database.sqlite3')
    WTF_CSRF_ENABLED = True
