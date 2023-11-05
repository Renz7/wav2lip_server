#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:03
Author  : ren
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, UploadFile, Depends, Form
from loguru import logger
from oss2 import Bucket

import utils
from dependence import get_repository, oss, get_user
from exceptions import *
from internal.celery.tasks import gen_wav2lip
from internal.db.models import Project
from repositories.digital_template_repo import DigitalTemplateRepo
from repositories.project_repo import ProjectRepository
from schema.celery.task_schema import GenWav2LipRequest
from schema.common import res_err
from schema.common import res_ok

router = APIRouter(prefix="/project")


def submit_task():
    pass


@router.post("/create")
async def create_project_api(video: UploadFile,
                             speech: UploadFile,
                             template_id: int = Form(),
                             repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo)),
                             project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
                             oss: Bucket = Depends(oss),
                             user: str = Depends(get_user)):
    template = await repo.get_by_id(template_id)
    if not template:
        raise RecordNotFound()
    video_path = utils.gen_oss_path(utils.get_file_suffix(video.filename))
    ret = oss.put_object(video_path, data=await video.read())
    if ret.status != 200:
        raise OSSError()

    speech_path = utils.gen_oss_path(utils.get_file_suffix(speech.filename))
    ret = oss.put_object(speech_path, data=await speech.read())
    if ret.status != 200:
        raise OSSError()

    v_url = utils.get_oss_url(video_path)
    s_url = utils.get_oss_url(speech_path)

    logger.info(f"upload file to oss {v_url}, {s_url}")
    task_req = GenWav2LipRequest(
        video=v_url,
        speech=s_url,
    )
    task = gen_wav2lip.apply_async(
        kwargs={"task_req": task_req.model_dump_json()},
        expires=datetime.now() + timedelta(hours=6))
    project = Project()
    project.origin_video_oss = v_url
    project.voice_oss = s_url
    project.task_id = task.task_id
    project.wx_id = user
    project = await project_repo.create(project)
    logger.info(f"insert project {project.id}")
    return res_ok({
        "project_id": project.id,
        "task_id": project.task_id
    })


@router.get("/{pid}")
async def get_project(pid: int, project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
                      wx_id: str = Depends(get_user)):
    if pid is None or not isinstance(pid, int):
        raise InvalidParam("projectId")
    project = await project_repo.get_by_id(pid)
    if not project or project.wx_id != wx_id:
        raise RecordNotFound()
    return res_ok(project)


@router.get("/")
async def get_user_project(
        offset: int = 0, size=5,
        project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
        wx_id=Depends(get_user)):
    if not wx_id:
        return res_err(0, "login required", 401)
    projects = project_repo.db.query(Project).offset(offset).limit(5).filter(Project.wx_id == wx_id).all()
    return res_ok(data=projects)
