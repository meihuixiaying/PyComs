#!/usr/bin/python 
# -*- coding: utf-8 -*-

from src.models.basemodels import EntityWithNameModel
from src.misc.exts import db


class Project(EntityWithNameModel):
    ACTIVE = 1
    DISABLE = 0

    description = db.Column(db.String(1000), nullable=True)
    status = db.Column(db.Integer, default=ACTIVE)
    weight = db.Column(db.Integer, default=1)
    logo = db.Column(db.String(2048), comment="Project Logo")
    ext = db.Column(db.Text())
