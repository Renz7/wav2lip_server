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
    def __init__(self, db):
        self.db: Session = db
        self.model_clz: typing.Type[Base] = self.get_model_clz()

    def get_model_clz(self) -> typing.Type[Base]:
        return object.__class__

    async def get_by_id(self, _id: int) -> Base:
        return self.db.query(self.model_clz).get(_id)
