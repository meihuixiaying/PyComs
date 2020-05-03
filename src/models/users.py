#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.misc.exts import db
from src.models.basemodels import EntityWithNameModel


class User(EntityWithNameModel):
    ACTIVE = 1
    DISABLE = 0

    nickname = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(30))
    weight = db.Column(db.Integer, default=1)
    status = db.Column(db.Integer, default=ACTIVE)
    ext = db.Column(db.Text())
