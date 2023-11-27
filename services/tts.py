#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/26 14:58
Author  : ren
"""
import urllib.parse

from config import tts_config


def tts(text: str, out: str = None):
    """
    调用tts接口
    :param text:
    :param out:
    :return:
    """
    url = urllib.parse.urljoin(tts_config.tts_url, "/voice_clone")
    data = {
        "prompt_audio": text,
        "prompt_text": out
    }
