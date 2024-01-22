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
        query = self.db.query(self.__clz__).filter(Project.task_status == status, Project.deleted == False)

        return query.offset((page - 1) * size).limit(
            size).all(), query.count()

    def delete(self, id):
        """
        删除项目
        :param id:
        :return:
        """
        self.db.query(self.__clz__).filter(Project.id == id).update({Project.deleted: True})
        self.db.commit()

    def update_name(self, id, name):
        self.db.query(self.__clz__).filter(Project.id == id).update({
            Project.name: name
        })
        self.db.commit()

    def update(self, project):
        self.db.query(self.__clz__).filter(Project.id == project.id).update({Project.name: project.name})
        self.db.commit()
