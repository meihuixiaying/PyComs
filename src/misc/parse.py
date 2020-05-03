#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request
from hashlib import md5

from config.settings import SALT, YML_JSON, logger

parse_pwd = lambda pwd: md5(SALT + pwd).hexdigest()


def parse_list_args():
    req_args = request.args
    try:
        limit = int(req_args.get('limit', 99999))
    except Exception:
        limit = 10
    try:
        offset = int(req_args.get('offset', 0))
    except Exception:
        offset = 0
    # q = req_args.get('q', None)
    return limit, offset


def parse_list_args2():
    req_args = request.args
    try:
        page_size = req_args.get('page_size')
        if page_size:
            page_size = int(page_size)
    except Exception:
        page_size = 10

    try:
        page_index = req_args.get('page_index')
        if page_index:
            page_index = int(page_index)
    except Exception:
        page_index = 1
    return page_size, page_index


def parse_json_form(name):
    form_json = YML_JSON.get(name)
    returnvalue = form_json.get('returnvalue')
    logger.info(request.json)
    return [request.json.get(x) for x in returnvalue]


def parse_query_string(name):
    form_json = YML_JSON.get(name)
    returnvalue = form_json.get('returnvalue')
    logger.info(request.args)
    return [request.args.get(x) for x in returnvalue]
