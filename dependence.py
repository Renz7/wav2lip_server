#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:26
Author  : ren
"""
import threading
from contextlib import contextmanager
from typing import Type

import oss2
from fastapi import Depends
from oss2 import Bucket
from oss2.credentials import StaticCredentialsProvider
from sqlalchemy.orm import Session
from starlette.requests import Request

from config import oss_config as config
from internal.db.database import session
from repositories import BaseRepository


# db
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


#  oss
bucket = None
lock = threading.Lock()


def init_bucket() -> Bucket:
    global bucket
    if not bucket:
        with lock:
            auth = oss2.ProviderAuth(
                StaticCredentialsProvider(access_key_id=config.access_key_id,
                                          access_key_secret=config.access_key_secret))
            bucket = oss2.Bucket(auth, endpoint=config.endpoint, bucket_name=config.bucket)
    return bucket


def oss():
    return init_bucket()


def get_user(request: Request):
    return request.session.get("wx_id")
