import os

youtube_api_key = "AIzaSyAyqF2hV2gyegSCqCK4sTPMKcAnJRNZIu8"
youtube_channel_id = "UC7P1LyBxStJkKxAb_yx5DKw"

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '40C8B34337CADF05A2CC16A41A68C115')
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass