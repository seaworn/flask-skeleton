import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""

    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a really hard to guess string')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    @staticmethod
    def configure():
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVEL_DATABASE_URL', 'sqlite:///' + os.path.join(base_dir, 'database-devel.sqlite3'))


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 'sqlite:///' + os.path.join(base_dir, 'database-test.sqlite3'))


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + os.path.join(base_dir, 'database.sqlite3'))
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig)
