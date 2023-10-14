#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:31
Author  : ren
"""

import celery

from config import celery_config


def get_celery():
    return celery.Celery(
        "wav2lip",
        backend=celery_config.broker,
        broker=celery_config.backend,
        include=["internal.celery.tasks"]
    )


celery_app = get_celery()
