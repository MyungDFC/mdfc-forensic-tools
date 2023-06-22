import os


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '40C8B34337CADF05A2CC16A41A68C115')


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
