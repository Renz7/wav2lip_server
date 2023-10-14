#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/13 21:51
Author  : ren
"""

from fastapi import APIRouter, Depends

from dependence import get_repository
from repositories.digital_template_repo import DigitalTemplateRepo
from schema.common import Paginate

router = APIRouter(prefix="/template")


@router.get("/")
async def get_templates(paginate: Paginate = Paginate.default(),
                        repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo))):
    return await repo.get_templates(paginate.page, paginate.page_size)


@router.post("/")
async def upload_template():
    pass
