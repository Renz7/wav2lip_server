#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:26
Author  : ren
"""
from contextlib import contextmanager
from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from internal.db.database import session
from repositories import BaseRepository


@contextmanager
def get_db() -> Session:
    """
    db dependence
    :return:
    """
    db = session()
    try:
        yield db
    finally:
        db.close()


async def db_dep() -> Session:
    with get_db() as db:
        yield db


def get_repository(repo_type: Type[BaseRepository]):
    def get_repo(db=Depends(db_dep)) -> BaseRepository:
        return repo_type(db)

    return get_repo
