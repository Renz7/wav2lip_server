#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 17:13
Author  : ren
"""

import click
import uvicorn
from click_default_group import DefaultGroup


@click.group(cls=DefaultGroup, default='run', default_if_no_args=True)
def cli():
    pass


@cli.command()
@click.option("--port", "-p", default=8000)
@click.option("--debug", "-d", default=False, type=bool)
def run(port: int, debug: bool = True):
    print(f"server listen on :{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=debug)


@cli.command("initdb")
@click.option("--drop", "-d")
def init_db(drop=False):
    from internal.db import database
    database.init(drop)


@cli.command("celery")
@click.option("--concurrency", "-c", default=4)
def celery_cmd(concurrency: int):
    from config import webui_config
    webui_config.enable = True
    from internal.celery.app import celery_app
    celery_app.worker_main(
        argv=[
            "worker",
            "--loglevel=DEBUG",
            "--pool=threads",
            "-c {}".format(concurrency if concurrency else 4)
        ]
    )


if __name__ == "__main__":
    cli()
