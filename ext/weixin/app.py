#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 12:58
Author  : ren
"""

from weixin.client import WxAppCloudAPI

from config import config

wx_app = WxAppCloudAPI(appid=config.weixin.appid, app_secret=config.weixin.app_secret)


def wx_login(code: str = None, encrypted_data=None, iv=None) -> dict:
    if not code:
        return None
    return wx_app.exchange_code_for_session_key(code)
