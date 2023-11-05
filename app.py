#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 17:14
Author  : ren
"""
import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from api import user_api, template_api, project_api, ffmpeg_api
from config import config
from exceptions import InternalException
from schema.common import res_err


def register_router(app: FastAPI):
    app.include_router(user_api.router)
    app.include_router(template_api.router)
    app.include_router(project_api.router)
    app.include_router(ffmpeg_api.router)


def setup_middlewares(app: FastAPI):
    """
    登陆检查
    :param app:
    :return:
    """

    async def check_login(request: Request, call_next):
        if not request.session.values():
            return res_err(-1, "login required", 401)
        else:
            logger.debug(f"session {request.session}")
            return await call_next(request)

    async def mock_session(reqeust: Request, call_next):
        reqeust.session.setdefault("wx_id", "wx_id-xxxxxx")
        return await call_next(reqeust)

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=check_login
    )
    if app.debug:
        logger.warning("setup mock login user middle")
        app.add_middleware(BaseHTTPMiddleware, dispatch=mock_session)  # todo del me in prod
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.secret_key,
        max_age=3 * 24 * 60 * 60,  # 3 days
    )


def init_logger():
    LOG_FORMAT = "{time} | {level} | {file}:{line} | {process}-{thread} | {message}"

    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level="DEBUG"
    )


def init_app(app: FastAPI):
    setup_middlewares(app)

    @app.exception_handler(InternalException)
    async def handle_common_err(request: Request, ex: InternalException):
        return res_err(code=ex.code, err=ex.err, status_code=ex.status)

    @app.exception_handler(500)
    async def handel_500(request: Request, ex):
        return res_err(code=-1, err=f"{ex}")


def create_app(debug: bool) -> FastAPI:
    app = FastAPI(debug=debug)
    init_app(app)
    register_router(app)
    return app


init_logger()

app = create_app(config.debug)
