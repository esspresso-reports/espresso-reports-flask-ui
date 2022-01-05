import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'espresso.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ESPRESSO_BACKEND_BASE_URL = os.getenv('ESPRESSO_API_BASE_URL', 'http://localhost:5000')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('ESPRESSO_DATABASE_URL')


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
