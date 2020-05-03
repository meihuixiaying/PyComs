#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir
from os.path import dirname, join, abspath, splitext

import yaml
import logging.config

SECRET = '*>_<*'
ALGORITHM = 'HS256'
SESSION_TIME = 60 * 60

PROJECT_NAME = 'pycoms'

SQLALCHEMY_DATABASE_URI = ''

SQLALCHEMY_TRACK_MODIFICATIONS = True
SCHEDULER_API_ENABLED = True

PROJECT_PATH = dirname(dirname(abspath(__file__)))

SALT = "pycoms"
VALIDATE_YML_PATH = join(PROJECT_PATH, 'src', 'validations')

YML_JSON = {}
for fi in listdir(VALIDATE_YML_PATH):
    if splitext(fi)[-1] !='.yml':
        continue
    with open(join(VALIDATE_YML_PATH, fi),'rb') as f:
        YML_JSON.update(yaml.load(f.read()))

logging.config.fileConfig(join(PROJECT_PATH,'config', 'logging.conf'))
logger = logging.getLogger('pycoms')

MSG_MAP = {
    0: 'ok',

    101: 'can not find object',
    102: 'save object error',
    103: 'duplicate data',
    104: 'can not create object',
    105: 'remove failed',
    106: 'operate failed',
    108: 'permission denied',
    109: 'project permission denied',

    201: 'field required',
    202: 'field length error',

    301: 'password wrong',
    303: 'username or password wrong',

    403: 'not allowed',
    410: 'auth expired',
    411: 'auth error',
    412: 'not login',
    413: 'username is not exist or password error',
    414: 'invalid data',
}

try:
    from config.local_settings import *
except Exception as e:
    pass
