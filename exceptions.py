#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/29 04:04
Author  : ren
"""
import typing


class InternalException(Exception):

    def __init__(self, code: int = -1, err: typing.Any = None, status_code=500):
        self.code = code
        self.err = err
        self.status = status_code


# 10xx data error
class RecordNotFound(InternalException):
    def __init__(self, msg=''):
        super().__init__(code=1001, err="record not found" if not msg else msg)


# 11xx args validate
class InvalidParam(InternalException):
    def __init__(self, fname=None):
        super().__init__(1101, f"invalid field[{fname}]")


# 12xx runtime error
class OSSError(InternalException):
    def __init__(self, msg="error during oss operating"):
        super().__init__(1201, msg)
