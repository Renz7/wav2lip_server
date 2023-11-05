#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:31
Author  : ren
"""

import celery

from config import celery_config


def get_celery():

    app = celery.Celery(
        "wav2lip",
        backend=celery_config.broker,
        broker=celery_config.backend,
        include=["internal.celery.tasks"],
        broker_connection_retry_on_startup=True
    )
    return app


celery_app = get_celery()
