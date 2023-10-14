#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 12:46
Author  : ren
"""
import celery
from loguru import logger

from dependence import get_db
from internal.celery.app import celery_app
from internal.db.models import Project, Status
from schema.wav2lip import GenWav2LipTask


class BaseTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"successfully submit a task[{self.name}-{task_id}]")

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        with get_db() as db:
            project = db.query(Project).filter(Project.task_id == task_id).first()
            if not project:
                logger.error(f"no project attach with this task{task_id}")
                return
            if einfo:
                project.task_status = Project.Status.FAILED
                db.commit()
                return
            elif retval:
                project.task_status = Status.SUCCESS
                project.result_oss = retval
                db.commit()


@celery_app.task(name="gen_wav2lip", base=BaseTask)
def gen_wav2lip(task_req: GenWav2LipTask) -> str:
    return "oss_url"


if __name__ == '__main__':
    gen_wav2lip.delay(GenWav2LipTask(template_oss="xx", wav_oss="xx").dict())
