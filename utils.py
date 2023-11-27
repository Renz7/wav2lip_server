#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 23:52
Author  : ren
"""
import urllib.parse
import uuid

from config import oss_config


def gen_oss_path(suffix: object = "mp4") -> object:
    """生产oss文件路径
    :rtype: object
    """
    suffix = suffix if suffix.startswith(".") else "." + suffix
    return f"sd-files/{uuid.uuid4().hex}{suffix}"


def get_file_suffix(fname: str):
    sp = fname.split(".")
    if len(sp) <= 1:
        return None
    else:
        return sp[-1]


def get_oss_url(fp):
    return urllib.parse.urljoin(oss_config.url_prefix, fp)
