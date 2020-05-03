#!/usr/bin/python 
# -*- coding: utf-8 -*-

from flask import Blueprint, request
from src.misc.parse import parse_list_args, parse_json_form
from src.misc.render import json_list_render, json_detail_render

from src.business import ProjectBusiness

project = Blueprint('project', __name__)


@project.route('/', methods=['GET'])
def project_query_handler():
    limit, offset = parse_list_args()
    data = ProjectBusiness.query_all(limit, offset)
    return json_list_render(0, data, limit, offset)
