#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:49
Author  : ren
"""

from fastapi import UploadFile, Form, Depends
from fastapi.routing import APIRouter
from loguru import logger
from sqlalchemy.orm import Session
from starlette.requests import Request

from dependence import get_user, db_dep
from ext.weixin.app import wx_login
from internal.db.models import User
from schema.common import res_ok, res_err

router = APIRouter(prefix="/user")


@router.post("/login")
async def login(code: str, request: Request, db: Session = Depends(db_dep)):
    if not code:
        return res_err(-1, err="code required")
    session_info = wx_login(code)
    wx_id = session_info['openid']
    request.session.setdefault("wx_id", wx_id)
    if not db.query(User).filter(User.wx_id == session_info["openid"]).first():
        user = User()
        user.wx_id = wx_id
        db.add(user)
        db.commit()
        logger.info(f"create user {wx_id}")
    return res_ok('ok')


@router.post("/user_info")
async def create_user_info(
        avatar: UploadFile,
        nick: str = Form(),
        user: str = Depends(get_user),
        db: Session = Depends(db_dep)
):
    """
    用户信息
    :param db:
    :param user:
    :param avatar:
    :param nick:
    :return:
    """
    if not user:
        return res_err(401, "login required", status_code=401)
    else:
        content = await avatar.read()
        db.query(User).filter(User.wx_id == user).update(
            {"avatar": content, "nickname": nick})
        db.commit()
        return res_ok("ok")


@router.get("/user_info")
async def get_user_info(user: str = Depends(get_user), db: Session = Depends(db_dep)):
    """
    获取用户信息
    :param db:
    :param user:
    :return:
    """
    if not user:
        return res_err(401, "login required", status_code=401)
    else:
        user_info = db.query(User).filter(User.wx_id == user).first()
        if not user_info:
            return res_err(404, "user not found", status_code=404)
        else:
            return res_ok(user_info)
