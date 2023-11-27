#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/26 14:02
Author  : ren
"""
from enum import IntEnum

from pydantic import BaseModel


class DRIVEN_MODE(IntEnum):
    UNDEFINED = -1
    TEXT = 0
    VOICE = 1


class CreateProject(BaseModel):
    # --- 模板部分 ---
    # 数字人模板
    digital_template_id: int
    # 背景选择
    background_id: int

    # --- 语音部分 ---
    # 驱动模式
    driven_mode: DRIVEN_MODE = DRIVEN_MODE.UNDEFINED
    # 文本
