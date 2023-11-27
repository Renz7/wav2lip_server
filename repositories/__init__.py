#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 00:18
Author  : ren
"""
import typing

from sqlalchemy.orm import Session

from internal.db.database import Base


class BaseRepository:
    __clz__: typing.Type[Base] = None

    def __init__(self, db):
        self.db: Session = db

    def page(self, page: int, size: int) -> object:
        count = self.db.query(self.__clz__).count()
        return self.db.query(self.__clz__).order_by(self.__clz__.id).offset((page - 1) * size).limit(size).all(), count

    def get_by_id(self, _id: int) -> Base:
        return self.db.query(self.__clz__).get(_id)

    def create(self, instance: Base):
        with self.db as db:
            db.add(instance)
            db.commit()
        return instance

    def update_by_id(self, id: int, update_state):
        with self.db as db:
            db.query(self.__clz__).order_by(self.__clz__.id).filter(self.__clz__.id == id).update(update_state)
            db.commit()
