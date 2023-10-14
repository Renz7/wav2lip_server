#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:49
Author  : ren
"""

from fastapi.routing import APIRouter
from starlette.requests import Request

from ext.weixin.app import wx_login
from schema.common import res_ok, res_err
from schema.user import UserLoginReq

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(login_req: UserLoginReq, request: Request):
    if not login_req.code:
        return res_err(-1, err="code required")
    session_info = wx_login(login_req.code)
    request.session.setdefault("wx_info", session_info)
    return res_ok(None)
