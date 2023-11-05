#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/5 16:17
Author  : ren
"""
import os
import pathlib
import tempfile
import uuid

from fastapi import APIRouter, UploadFile, BackgroundTasks
from loguru import logger
from starlette.responses import FileResponse, Response

import exceptions
from services import ffmpeg

router = APIRouter(prefix="/ffmpeg")

tmp_dir = tempfile.tempdir + "/wav2lip/"
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)


def clean_up(*files):
    for fp in files:
        os.remove(fp)


@router.post("/swap_background")
async def swap_background(background_pic: UploadFile, front_video: UploadFile, backend_task: BackgroundTasks) \
        -> FileResponse:
    # save file to tmp
    if not background_pic or not front_video:
        return exceptions.InvalidParam("video ,backgroundPic")
    pic_fn = background_pic.filename or uuid.uuid4().hex
    pic_fn = pathlib.Path(tmp_dir, pic_fn)
    print(pic_fn)
    with open(pic_fn, "wb+") as pic_file:
        pic_file.write(await background_pic.read())
    video_fn = front_video.filename or uuid.uuid4().hex
    video_fn = pathlib.Path(tmp_dir, video_fn)
    with open(video_fn, "wb+") as video_file:
        video_file.write(await front_video.read())

    outfile = pathlib.Path(tmp_dir, uuid.uuid4().hex + '.mp4')
    ffmpeg.ffmpeg_swap_background(video_fn, pic_fn, outfile)
    logger.debug(f"remove files [{video_fn, pic_fn, outfile}]")
    backend_task.add_task(clean_up, video_fn, pic_fn, outfile)

    return FileResponse(path=outfile)
