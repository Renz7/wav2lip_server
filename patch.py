#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/28 17:53
Author  : ren
"""
import os
import secrets
import tempfile
from pathlib import Path

import gradio_client.utils as gutils
import requests
from gradio_client.serializing import VideoSerializable


def patch_video_deserialize():
    origin_deserialize = VideoSerializable.deserialize

    def patched_deserialize(self, x, save_dir, root_url, hf_token):
        if x is None:
            return None
        else:
            return origin_deserialize(self, x, save_dir, root_url, hf_token)

    VideoSerializable.deserialize = patched_deserialize


def patch_download_tmp_copy_of_file():
    def patched_download_tmp_copy_of_file(
            url_path: str, hf_token: str | None = None, dir: str | None = None
    ) -> str:
        if dir is not None:
            os.makedirs(dir, exist_ok=True)
        headers = {"Authorization": "Bearer " + hf_token} if hf_token else {}
        directory = Path(dir or tempfile.gettempdir()) / secrets.token_hex(20)
        directory.mkdir(exist_ok=True, parents=True)
        file_path = directory / Path(url_path).name

        with requests.get(url_path, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(r.content)
        return str(file_path.resolve())

    gutils.download_tmp_copy_of_file = patched_download_tmp_copy_of_file


def patch_gradio():
    patch_video_deserialize()
    patch_download_tmp_copy_of_file()
