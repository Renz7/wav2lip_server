#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:34
Author  : ren
"""
from pydantic import BaseModel


class UserLoginReq(BaseModel):
    code: str
