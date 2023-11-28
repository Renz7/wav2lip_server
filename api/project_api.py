#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:03
Author  : ren
"""
from __future__ import annotations

from fastapi import APIRouter, UploadFile, Depends, Form
from loguru import logger
from oss2 import Bucket
from starlette.background import BackgroundTasks

import utils
from dependence import get_repository, get_oss, get_user
from exceptions import *
from internal.db.models import Project, BackgroundPic, Status
from repositories.backendground_pic_repo import BackedgroundPicRepo
from repositories.digital_template_repo import DigitalTemplateRepo
from repositories.project_repo import ProjectRepository
from schema.common import res_ok
from schema.project import DRIVEN_MODE
from services import wav2lip

router = APIRouter(prefix="/project")


@router.get("/")
async def get_projects(status: int | None = None,
                       page: int = 1, size: int = 5,
                       project_repo: ProjectRepository = Depends(get_repository(ProjectRepository))):
    if not status:
        projects, total = project_repo.page(page, size)
    else:
        projects, total = await project_repo.page_by_status(status, page, size)
    return res_ok(data={
        "data": projects,
        "total": total
    })


@router.post("/create", description="创建项目")
async def create_project_api(
        background_task: BackgroundTasks,
        template_id: int = Form(),
        background_id: int | None = Form(default=None),
        background_pic: UploadFile | None = Form(default=None),
        driven_mode: int = Form(),
        speech_text: str | None = Form(default=None),
        voice: UploadFile | None = Form(default=None),
        template_repo: DigitalTemplateRepo = Depends(get_repository(DigitalTemplateRepo)),
        background_repo: BackedgroundPicRepo = Depends(get_repository(BackedgroundPicRepo)),
        project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
        user: str = Depends(get_user),
        oss: Bucket = Depends(get_oss),
):
    """
    创建项目
    :param background_task: 
    :param template_id: 数字人物模板id
    :param background_id: 背景图片id
    :param background_pic:背景图片
    :param driven_mode: 驱动模式
    :param speech_text: 语音文本
    :param voice: 语音文件
    :param template_repo:
    :param background_repo:
    :param project_repo:
    :param user: 用户id
    :param oss: oss
    :return:
    """
    if not (template_id or (background_pic or background_id)):
        raise InvalidParam("templateId or (backendPic and backendId) required")
    template = template_repo.get_by_id(template_id)
    if not template:
        raise RecordNotFound("template not found")
    pic = None
    if background_id:
        pic = background_repo.get_by_id(background_id)
    if background_pic:
        if len(background_pic.filename.split(".")) < 2:
            raise InvalidParam("file type error")
        file_type = background_pic.filename.split(".")[-1]
        path = utils.gen_oss_path(file_type)
        oss.put_object(path, await background_pic.read())
        logger.info(f"upload background pic to oss {path}")
        db_model = BackgroundPic()
        db_model.name = background_pic.filename
        db_model.is_system = False
        db_model.background_oss = path
        db_model.wx_id = user
        pic = background_repo.create(db_model)
        logger.info(f"insert background pic {pic.id}")
    if not pic:
        raise RecordNotFound("background pic not found")
    voice_oss = None
    if driven_mode == DRIVEN_MODE.TEXT and not speech_text:
        raise InvalidParam("speechText required")
    elif driven_mode == DRIVEN_MODE.VOICE:
        if not voice:
            raise InvalidParam("voice required")
        else:
            if len(voice.filename.split(".")) < 2:
                raise InvalidParam("file type error")
            file_type = voice.filename.split(".")[-1]
            voice_oss = utils.gen_oss_path(file_type)
            oss.put_object(voice_oss, await voice.read())
            logger.info(f"upload voice to oss {voice_oss}")
    project = Project()
    project.template_id = template_id
    project.background_id = background_id
    project.driven_mode = driven_mode
    project.speech_text = speech_text
    project.voice_oss = voice_oss
    project.task_status = Status.PENDING
    project.wx_id = user
    project = project_repo.create(project)
    logger.info(f"create project{project.id} success")
    background_task.add_task(wav2lip.wav2lip_task, project, template, pic)
    return res_ok({
        "project_id": project.id
    })


@router.get("/{pid}")
async def get_project(pid: int, project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
                      wx_id: str = Depends(get_user)):
    if pid is None or not isinstance(pid, int):
        raise InvalidParam("projectId")
    project = project_repo.get_by_id(pid)
    if not project or project.wx_id != wx_id:
        raise RecordNotFound()
    return res_ok(project)
