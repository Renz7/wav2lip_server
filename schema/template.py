#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 23:49
Author  : ren
"""
from pydantic import BaseModel

import utils
from internal.db.models import DigitalTemplate


class Template(BaseModel):
    id: int
    name: str
    oss_url: str

    @staticmethod
    def from_db(db_model: DigitalTemplate):
        return Template(
            id=db_model.id,
            name=db_model.name,
            oss_url=utils.parse_oss_url(db_model.template_oss)
        )
