#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 23:52
Author  : ren
"""
from urllib import parse

from fastapi import File,UploadFile

from config import config


def parse_oss_url(url):
    """
    parse full oss path
    :param url: base path in db
    :return:
    """
    return parse.urljoin(config.oss_base, url)


async def upload_oss(file: UploadFile, path) -> str:
    # todo 上传文件返回地址
    file.filename
    return ""
