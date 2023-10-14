#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 17:24
Author  : ren
"""
from pydantic_settings import BaseSettings as DanticBaseSettings, SettingsConfigDict


class BaseSettings(DanticBaseSettings):
    model_config = SettingsConfigDict(_case_sensitive=False, env_file=".env", extra="ignore")


class WeixinConfig(BaseSettings):
    appid: str = "xx"
    app_secret: str = "xxx"


class Config(BaseSettings):
    db_url: str = "mysql+pymysql://root:1233@localhost/wav2lip"
    weixin: WeixinConfig = WeixinConfig()
    secret_key: str = "xxx"

    oss_base: str = "http://"


config = Config()


class CeleryConfig(BaseSettings):
    broker: str = "redis://localhost/0"
    backend: str = "redis://localhost/0"


celery_config = CeleryConfig()

print(celery_config, config)
