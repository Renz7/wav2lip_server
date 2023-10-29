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

    async def get_by_id(self, _id: int) -> Base:
        return self.db.query(self.__clz__).get(_id)

    async def create(self, instance: Base):
        with self.db as db:
            db.add(instance)
            db.commit()
        return instance

    async def update_by_id(self, id: int, update_state):
        with self.db as db:
            db.query(self.__clz__).filter(self.__clz__.id == id).update(update_state)
            db.commit()
