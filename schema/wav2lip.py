#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:39
Author  : ren
"""
import dataclasses

from pydantic import BaseModel


class GenWav2LipTask(BaseModel):
    template_oss: str
    wav_oss: str
