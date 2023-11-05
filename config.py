#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 17:24
Author  : ren
"""
from pydantic_settings import BaseSettings as DanticBaseSettings, SettingsConfigDict


class BaseSettings(DanticBaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env", extra="ignore")


class WeixinConfig(BaseSettings):
    appid: str = "xx"
    app_secret: str = "xxx"


class OSSConfig(BaseSettings):
    access_key_id: str
    access_key_secret: str
    endpoint: str
    bucket: str
    url_prefix: str


class Config(BaseSettings):
    debug: bool = False
    db_url: str = "mysql+pymysql://root:1233@localhost/wav2lip"

    weixin: WeixinConfig = WeixinConfig()
    secret_key: str = "xxx"

    wav2lip_fn_index: int = 314


class CeleryConfig(BaseSettings):
    broker: str = "redis://localhost/0"
    backend: str = "redis://localhost/0"


class WebuiConfig(BaseSettings):
    enable: bool = False
    webui_url: str = "http://127.0.0.1:7860/"
    webui_output_dir: str = "./output"


config = Config()
celery_config = CeleryConfig()
oss_config = OSSConfig()

webui_config = WebuiConfig()
