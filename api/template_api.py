#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 21:51
Author  : ren
"""

from fastapi import APIRouter, Depends, UploadFile, Form
from oss2 import Bucket

import utils
from dependence import get_repository, get_oss
from internal.db.models import DigitalTemplate
from repositories.digital_template_repo import DigitalTemplateRepo
from schema.common import Paginate, res_ok

router = APIRouter(prefix="/template")


@router.get("/")
async def get_templates(paginate: Paginate = Paginate.default(),
                        repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo))):
    data = repo.get_templates(paginate.page, paginate.page_size)
    return res_ok(data)


@router.post("/create")
async def upload_template(template_file: UploadFile,
                          template_preview_pic: UploadFile,
                          template_name: str = Form(),
                          repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo)),
                          oss: Bucket = Depends(get_oss)):
    oss_path = utils.gen_oss_path(suffix="mp4")
    oss.put_object(oss_path,
                   await template_file.read())  # 可能存在性能问题
    pic_path = utils.gen_oss_path(suffix=utils.get_file_suffix(template_preview_pic.filename))
    oss.put_object(pic_path,
                   await template_preview_pic.read())
    template = DigitalTemplate()

    template.name = template_name,
    template.template_oss = oss_path
    template.preview_pic = pic_path
    repo.create_template(template)
    return res_ok(template)
