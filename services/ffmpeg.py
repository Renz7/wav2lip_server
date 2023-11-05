#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/11/5 19:19
Author  : ren
"""
import shutil
import subprocess
import tempfile
import uuid

from loguru import logger

import exceptions


def ffmpeg_swap_background(video: str, pic: str, out: str = None) -> str:
    """
    run ffmpeg swap background process
    :param video: fround video path
    :param pic: background pic path
    :param out: out file path
    :return: outfile path
    """
    if out:
        output = out
    else:
        output = tempfile.mktemp(f"{uuid.uuid4().hex}.mp4")

    if shutil.which("ffmpeg") is None:
        raise exceptions.ExecutableNotFound()
    else:
        p_args = ["ffmpeg", "-loop", "1", "-i", pic, "-i", video,
                  "-filter_complex", "[0:v][1:v]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p", "-an", output]
        logger.info(f"swap background process [{p_args}]")
        p = subprocess.Popen(p_args)
        p.wait(3 * 60)
        if p.returncode != 0:
            raise exceptions.SubProcessError(f"ffmpeg subprocess error with code:[{p.returncode}]")
        return output
