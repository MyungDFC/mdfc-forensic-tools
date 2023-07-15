import os

youtube_api_key = "AIzaSyAyqF2hV2gyegSCqCK4sTPMKcAnJRNZIu8"
youtube_channel_id = "UC7P1LyBxStJkKxAb_yx5DKw"
youtube_playlist_id_digital_forensics = "PLQQ1DxVUSynHVkxkV3CYrl3F5qsZjw89E"
youtube_playlist_id_all = "PLQQ1DxVUSynEX6k953Mo-V711SOyndaug"

naver_api_key = "YYMHwn7FkrCqVUPMGU4H"
naver_api_secret = "JAW_Yuw8_z"

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '40C8B34337CADF05A2CC16A41A68C115')
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass