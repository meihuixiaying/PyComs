#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from flask import jsonify
from flask import make_response
from config.settings import MSG_MAP


def _render(resp):
    response = make_response(jsonify(resp))
    #    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


def json_list_render(code, data, limit, offset, message=None):
    if message is None:
        message = MSG_MAP.get(code)
    resp = dict(
        code=code, limit=limit, offset=offset, message=message, data=data)
    return _render(resp)


def json_list_render2(code, data, page_size, page_index, total, message=None):
    if message is None:
        message = MSG_MAP.get(code)
    resp = dict(
        code=code, page_size=page_size, page_index=page_index, total=total, message=message, data=data)
    return _render(resp)


def json_detail_render(code, data=[], message=None):
    if message is None:
        message = MSG_MAP.get(code)
    resp = dict(code=code, message=message, data=data)
    return _render(resp)


def json_token_render(code, token, message=None):
    if message is None:
        message = MSG_MAP.get(code)
    resp = dict(code=code, token=token, message=message)
    return _render(resp)


def json_detail_render_sse(code, data=[], message=None):
    if message is None:
        message = MSG_MAP.get(code)
    resp = dict(code=code, message=message, data=data)
    return json.dumps(resp)
