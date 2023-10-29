#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 00:38
Author  : ren
"""

import typing

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Paginate(BaseModel):
    page: int = 0
    page_size: int = 10

    @staticmethod
    def default():
        return Paginate(page=0, page_size=10)


class DataResponse(BaseModel):
    data: typing.Any = ""
    code: int = 0
    err_msg: str = ""


def res_ok(data=None):
    return DataResponse(data=jsonable_encoder(data))


def res_err(code, err, status_code=500):
    return JSONResponse(
        content=DataResponse(code=code, err_msg=err).model_dump(), status_code=status_code
    )


class InternalException(Exception):

    def __init__(self, code: int = -1, err: typing.Any = None, status_code=500):
        self.code = code
        self.err = err
        self.status = status_code
