#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:03
Author  : ren
"""

from fastapi import APIRouter, UploadFile, Depends, Form

import utils
from dependence import get_repository
from internal.celery.tasks import gen_wav2lip
from repositories.digital_template_repo import DigitalTemplateRepo
from schema.common import res_err, InternalException
from schema.wav2lip import GenWav2LipTask

router = APIRouter(prefix="/project")


def submit_task():
    pass


@router.post("/create")
async def create_project(file: UploadFile, template_id: int = Form(),
                         repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo))):
    template = await repo.get_by_id(template_id)
    if not template:
        raise InternalException(
            code=-2,
            err="template file not exists"
        )
    oss_path = await utils.upload_oss(file, "")  # todo
    task_req = GenWav2LipTask(
        template.oss_url,
        oss_path
    )

    task = gen_wav2lip.delay(task_req)

    return task.id
