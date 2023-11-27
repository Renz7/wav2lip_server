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
from schema.common import Paginate

router = APIRouter(prefix="/template")


@router.get("/")
async def get_templates(paginate: Paginate = Paginate.default(),
                        repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo))):
    return repo.get_templates(paginate.page, paginate.page_size)


@router.post("/create")
async def upload_template(template_file: UploadFile,
                          template_name: str = Form(),
                          repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo)),
                          oss: Bucket = Depends(get_oss)):
    oss_path = utils.gen_oss_path(suffix="mp4")
    url = utils.get_oss_url(oss_path)
    oss.put_object(oss_path,
                   await template_file.read())  # 可能存在性能问题
    template = DigitalTemplate()

    template.name = template_name,
    template.template_oss = oss_path
    repo.create_template(template)
    return template.id
