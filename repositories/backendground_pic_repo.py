#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/26 13:45
Author  : ren
"""
from internal.db.models import BackgroundPic
from . import BaseRepository


class BackedgroundPicRepo(BaseRepository):
    __clz__ = BackgroundPic
