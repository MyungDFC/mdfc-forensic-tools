import os

youtube_api_key = "AIzaSyArJw90BhvdgM5fWF1GTdvs7nm0QMUsdpQ"

youtube_channel_id = "UC7P1LyBxStJkKxAb_yx5DKw"
youtube_playlist_id_digital_forensics = "PLQQ1DxVUSynHVkxkV3CYrl3F5qsZjw89E"
youtube_playlist_id_media_series = "PLQQ1DxVUSynHc6OEEK1T_RHmUfXHb_6FA"
youtube_playlist_id_myungtv_special = "PLQQ1DxVUSynEzV-aXRGe33hfsDxDAGvOn"
youtube_playlist_id_office_life_episode = "PLQQ1DxVUSynHdEnI8-yTepu52NeyjPjME"
youtube_playlist_id_it_information = "PLQQ1DxVUSynERq7dryeGeBKfvl-wCFs8j"
youtube_playlist_id_all = "PLQQ1DxVUSynEX6k953Mo-V711SOynaug"

tistory_api_token = "da5bb94f06d2b241c9b8d7f47f4df03e_caa447be52e5fbc5bf498e082bd18e91"

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', '40C8B34337CADF05A2CC16A41A68C115')
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass