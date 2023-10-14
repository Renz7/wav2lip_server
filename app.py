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

from api import user_api, template_api, project_api
from config import config
from schema.common import res_err, InternalException


def register_router(app: FastAPI):
    app.include_router(user_api.router)
    app.include_router(template_api.router)
    app.include_router(project_api.router)


def init_session(app):
    async def check_login(request: Request, call_next):
        if not request.session.values():
            return res_err(-1, "login required", 401)
        else:
            logger.debug(f"session {request.session}")
            return await call_next(request)

    async def mock_session(reqeust: Request, call_next):
        reqeust.session.setdefault("1", 1)
        return await call_next(reqeust)

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=check_login
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=mock_session)
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.secret_key
    )


def init_logger():
    LOG_FORMAT = "{time} | {level} | {file}:{line} | {process}-{thread} | {message}"

    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level="DEBUG"
    )


def init_app(app: FastAPI):
    init_session(app)

    @app.exception_handler(InternalException)
    async def handle_common_err(request: Request, ex: InternalException):
        return res_err(code=ex.code, err=ex.err, status_code=ex.status)

    @app.exception_handler(500)
    async def handel_500(request: Request, ex):
        return res_err(code=-1, err=f"unknown error {ex}")


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    init_app(app)
    register_router(app)
    return app


init_logger()

app = create_app()
