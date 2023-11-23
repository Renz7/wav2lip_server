#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 23:49
Author  : ren
"""
from typing import Optional

from pydantic import BaseModel

import utils
from internal.db.models import DigitalTemplate


class Template(BaseModel):
    id: int
    name: str
    oss_url: Optional[str]

    @staticmethod
    def from_db(db_model: DigitalTemplate):
        return Template(
            id=db_model.id,
            name=db_model.name,
            oss_url= utils.get_oss_url(db_model.template_oss)
        )
