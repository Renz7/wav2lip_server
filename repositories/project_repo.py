#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/29 00:53
Author  : ren
"""

from internal.db.models import Project
from repositories import BaseRepository


class ProjectRepository(BaseRepository):
    __clz__ = Project
