#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/10/11 18:05
Author  : ren
"""
import enum

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Enum, TEXT

from internal.db.database import Base


class DateMixin(object):
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    create_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class User(DateMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    wx_id = Column(String(64), index=True)

    voice_prompt_oss = Column(String(512), comment="语音提示oss地址", nullable=True)


class Status(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Project(DateMixin, Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    wx_id = Column(String(32), index=True, comment="wx openid")
    deleted = Column(Boolean, default=False, comment="是否删除")

    template_id = Column(Integer, comment="数字人模板id")
    background_id = Column(Integer, comment="背景id")
    voice_oss = Column(String(512), comment="音频文件地址", nullable=True)
    speech_text = Column(TEXT, comment="语音文本", nullable=True)
    # task
    task_id = Column(String(64), comment="celery task id")
    task_status = Column(Enum(Status))
    result_oss = Column(String(512), comment="oss 存储地址")


class DigitalTemplate(DateMixin, Base):
    __tablename__ = "digital_template"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), comment="模板名称")
    template_oss = Column(String(512), comment="数字人模板文件")


class BackgroundPic(DateMixin, Base):
    __tablename__ = "background_pic"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), comment="背景名称")
    background_oss = Column(String(512), comment="背景文件")
    is_system = Column(Boolean, default=False, comment="是否是系统背景")
