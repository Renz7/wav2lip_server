#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/26 15:49
Author  : ren
"""

from gradio_client import Client

from config import webui_config as config

webui_client: Client = Client(
    src=config.webui_url,
    max_workers=8, output_dir=config.webui_output_dir,
    serialize=True
)
