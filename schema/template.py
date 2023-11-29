#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 23:49
Author  : ren
"""
from typing import Optional

from pydantic import BaseModel

from internal.db.models import DigitalTemplate


class Template(BaseModel):
    id: int
    name: str
    oss_url: Optional[str]
    pic_url: Optional[str]

    @staticmethod
    def from_db(db_model: DigitalTemplate):
        return Template(
            id=db_model.id,
            name=db_model.name,
            oss_url=db_model.template_oss,
            pic_url=db_model.preview_pic
        )
