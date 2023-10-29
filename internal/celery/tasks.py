#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 12:46
Author  : ren
"""
import logging
import sys
from logging import Logger

import gradio_client.serializing

import utils
from patch import patch_gradio

patch_gradio()

import json
import time
from dataclasses import asdict
from typing import Any

import celery
import pydantic
from celery.exceptions import InvalidTaskError, TaskError
from config import config
from dependence import get_db, oss
from ext.webui_client import webui_client
from internal.celery.app import celery_app
from internal.db.models import Project, Status
from schema.celery.task_schema import GenWav2LipRequest, TTSTask

logger: Logger = logging.getLogger("celery.task")
hd = logging.StreamHandler(sys.stdout)
hd.setFormatter(logging.Formatter("%(asctime)s %(pathname)s:%(lineno)s %(levelname)s %(msg)s"))
logger.addHandler(hd)


class BaseTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"task[{self.name}-{task_id}] execute successful retval[{retval}]")
        with get_db() as db:
            project = db.query(Project).filter(Project.task_id == task_id).first()
            if not project:
                logger.error(f"no project attach with this task{task_id}")
                return
            elif retval:
                project.task_status = Status.SUCCESS
                project.result_oss = retval
                db.commit()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        with get_db() as db:
            project = db.query(Project).filter(Project.task_id == task_id).first()
            if not project:
                logger.error(f"no project attach with this task{task_id}")
                return
            if einfo:
                project.task_status = Status.FAILED
                project.result_oss = einfo.msg
                db.commit()


@celery_app.task(name="gen_tts", base=BaseTask)
def tts(req: TTSTask):
    return


@celery_app.task(name="gen_wav2lip", base=BaseTask, bind=True)
def gen_wav2lip(self, task_req: Any) -> str:
    def fn_callback(*args):
        logger.info("wav2lip task finish")
        pass

    logger.info("start task ...")
    task_req = pydantic.TypeAdapter(GenWav2LipRequest).validate_python(json.loads(task_req), strict=False)
    req_args = task_req.to_wav2lip_req()
    job = None
    try:
        job = webui_client.submit(*req_args, fn_index=config.wav2lip_fn_index, result_callbacks=fn_callback)
        while not job.done():
            status = asdict(job.status())
            status['code'] = str(status.get('code', None))
            self.update_state(state='PROGRESS', meta=status)
            logger.info(f"{job.status()}")
            time.sleep(3)
        else:
            if job:
                logger.info(f"{job.status()}")
    except Exception as e:
        logger.exception(f"webui task error {e}")
        job.cancel()
        raise InvalidTaskError("webui task submit failed")
    ret = job.result()
    if ret is not None:
        fp = ret[-1]
        logger.info(f"get generated output {type(fp)}:{fp}")
        key = utils.gen_oss_path()
        oss().put_object_from_file(key, fp)
        return utils.get_oss_url(key)
    raise TaskError("null generate result")
