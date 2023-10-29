#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 17:58
Author  : ren
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,DeclarativeBase

from config import config

engine = create_engine(
    config.db_url, echo=True, echo_pool="debug"
)

session = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)

Base = declarative_base()


def init(drop=False):
    from internal.db import models  # noqa
    if drop:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    #
    tmp = models.DigitalTemplate()
    tmp.id = -1
    tmp.name = 'test_tmp'
    with session() as s:
        s.add(tmp)
        s.commit()
