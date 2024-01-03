#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/26 14:39
Author  : ren
"""
from datetime import datetime, timedelta

from loguru import logger

import utils
from dependence import get_db, get_oss
from internal.celery.tasks import gen_wav2lip
from internal.db.models import Project, DigitalTemplate, Status, BackgroundPic
from schema.celery.task_schema import GenWav2LipRequest
from services.ffmpeg import ffmpeg_swap_background
from services.tts import tts


def wav2lip_task(
        project: Project,
        template: DigitalTemplate,
        background_pic: BackgroundPic
):
    """
    后台创建任务
    :param project:
    :return:
    """
    voice_oss, video_oss = None, None
    if project.voice_oss:
        voice_oss = utils.get_oss_url(project.voice_oss)
    elif project.speech_text:
        voice_oss = tts(project.speech_text)

    video = utils.get_oss_url(template.template_oss)
    if background_pic:
        pic = utils.get_oss_url(background_pic.background_oss)
        out = ffmpeg_swap_background(video, pic)
        get_oss().put_object_from_file(out.split("/")[-1], out)
        video = utils.get_oss_url(out.split("/")[-1])
        logger.info("swap background success: {}", out)

    task_req = GenWav2LipRequest(
        speech=voice_oss,
        video=video,
    )
    task = gen_wav2lip.apply_async(
        kwargs={"task_req": task_req.model_dump_json()},
        expires=datetime.now() + timedelta(hours=6))
    with get_db() as db:
        logger.info("create project{} task: {}", project.id, task.id)
        db.query(Project).filter(Project.id == project.id).update(
            {
                "task_id": task.id,
                "task_status": Status.RUNNING
            }
        )
        db.commit()
