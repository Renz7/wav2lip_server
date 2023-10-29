#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/14 11:39
Author  : ren
"""
from typing import Any

from pydantic import BaseModel


class TaskResult(BaseModel):
    status: str = None
    data: object = None


class GenWav2LipRequest(BaseModel):
    video: str = ""
    face_swap: Any = None
    face_index: int = 0
    speech: str = ""
    checkpoint: str = "wav2lip"
    face_restoration_model: str = "GFPGAN"
    no_smooth: Any = None
    only_mouth: Any = None
    resize_factor: int = 1
    mouth_mask_dilate: int = 15
    face_mask_erode: int = 15
    mask_blur: int = 15
    pad_top: int = 0
    pad_bottom: int = 0
    pad_left: int = 0
    pad_right: int = 0
    active_debug: Any = None
    code_former_fidelity: float = 0.75

    def to_wav2lip_req(self):
        """
        组装请求参数
        :return:
        """
        return [
            self.video,
            self.face_swap,
            self.face_index,
            self.speech,
            self.checkpoint,
            self.face_restoration_model,
            self.no_smooth,
            self.only_mouth,
            self.resize_factor,
            self.mouth_mask_dilate,
            self.face_mask_erode,
            self.mask_blur,
            self.pad_top,
            self.pad_bottom,
            self.pad_left,
            self.pad_right,
            self.active_debug,
            self.code_former_fidelity,
        ]


class TTSTask(BaseModel):
    audio: bytes


if __name__ == '__main__':
    from ext.webui_client import webui_client

    res = webui_client.submit(*GenWav2LipRequest().to_wav2lip_req(), fn_index=314)
    r = res.result()
    GenWav2LipRequest().model_dump_json()
    import kombu

    kombu.serialization.register("")
    print(r)
