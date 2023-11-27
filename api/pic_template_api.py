#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/26 13:41
Author  : ren
"""
from fastapi import APIRouter, Depends, UploadFile
from oss2 import Bucket

import utils
from dependence import get_repository, get_oss
from internal.db.models import BackgroundPic
from repositories.backendground_pic_repo import BackedgroundPicRepo
from schema.common import res_ok

router = APIRouter(prefix="/pic")


@router.get("/")
async def get_pic(
        page: int = 0, size: int = 10,
        repo: BackedgroundPicRepo = Depends(get_repository(BackedgroundPicRepo))):
    data, total = repo.page(page, size)

    return res_ok(
        {
            "data": data,
            "total": total
        }
    )

@router.get("/upload")
async def upload_pic(pic: UploadFile,
                     name: str = None,
                     oss: Bucket = Depends(get_oss),
                     repo: BackedgroundPicRepo = Depends(get_repository(BackedgroundPicRepo))):
    if len(pic.filename.split(".")) < 2:
        raise Exception("file type error")
    file_type = pic.filename.split(".")[-1]
    path = utils.gen_oss_path(file_type)
    oss.put_object(path, await pic.read())
    backend = BackgroundPic()
    backend.name = name
    backend.background_oss = path
    return repo.create(backend)
