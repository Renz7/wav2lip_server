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

    def page_by_status(self, status, page, size):
        """
        根据项目编辑状态分页
        :param status:
        :param page:
        :param size:
        :return:
        """
        query = self.db.query(self.__clz__).filter(Project.task_status == status)

        return query.offset((page - 1) * size).limit(
            size).all(), query.count()
