#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import settings
from src.views.v1.project import project
from src.misc.exts import db, ma
from flask import Flask

DEFAULT_APP_NAME = settings.PROJECT_NAME
DEFAULT_MODULES = (
    (project, '/project'),
)


def create_app(app_name=None, modules=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME
    if modules is None:
        modules = DEFAULT_MODULES

    app = Flask(app_name)
    configure_conf(app)
    configure_exts(app)
    configure_modules(app, modules)
    return app


def configure_conf(app):
    app.config.from_pyfile('config/settings.py')


def configure_modules(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix='/v1{}'.format(url_prefix))


def configure_exts(app):
    db.init_app(app)
    ma.init_app(app)
