#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
from functools import wraps
from flask import request
from src.misc.render import json_detail_render
from config.settings import YML_JSON, logger
import datetime,json

def transfer(column):
    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            tmap = {
                '?': "",
                '!': "",
                '@': [],
                '#': {},
                '$': False,
            }
            result = func(*args, **kwargs)
            if not isinstance(result, list):
                raise('should be a list')

            cols = [i.strip() for i in column.split('|')]
            pure_cols = map(lambda x : x[1:], cols)
            template = {col[1:]: tmap.get(col[0]) for col in cols}
            key_col = filter(lambda x: '?' in x, cols)[0][1:]
            tdata = [{item: getattr(res, item) for item in pure_cols} for res in result]

            data = []
            
            for d in tdata:
                tpl = deepcopy(template)
                for k, v in d.iteritems():
                    if isinstance(tpl[k], basestring) and v:
                        tpl[k] = v
                    elif isinstance(tpl[k], list) and v:
                        tlist = deepcopy(tpl[k])
                        tlist.append(v)
                        tpl[k] = tlist
                    elif isinstance(tpl[k], dict) and v:
                        tdict = deepcopy(tpl[k])
                        tdict.update(v)
                        tpl[k] = tdict
                    elif isinstance(tpl[k], bool):
                        t = deepcopy(tpl[k])
                        t = bool(v)
                        tpl[k] = t

                data.append(tpl)
            return data
        return _
    return dec


def transfer2json(column):
    """
    ? : key
    ! : string
    @ : list
    # : dict
    $ : bool
    & : tuple
    """

    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            tmap = {
                '?': "",
                '!': "",
                '@': [],
                '#': {},
                '$': False,
                '&': (),
                '~': ['~'],

            }
            result = func(*args, **kwargs)
            if not isinstance(result, list):
                raise('should be a list')
            cols = [i.strip() for i in column.split('|')]
            # key的list形式数据
            pure_cols = map(lambda x : x[1:], cols)
            # 键值对中给value赋值tmap
            template = {col[1:]: tmap.get(col[0]) for col in cols}
            key_col = filter(lambda x: '?' in x, cols)[0][1:]
            # 键值对中给value赋值数据库
            tdata = [{item: getattr(res, item) for item in pure_cols} for res in result]
            data = []
            for d in tdata:
                fu = [i for i in data if i.get(key_col) == d.get(key_col)]
                if len(fu) == 0:
                    tpl = deepcopy(template)
                    for k,v in d.iteritems():
                        if isinstance(tpl[k], basestring) and v!=None:
                            tpl[k] = v
                        elif tpl[k]==['~']:
                            tjlist = json.loads(v) if v else []
                            tpl[k] = tjlist
                        elif isinstance(tpl[k], list) and v:
                            tlist = deepcopy(tpl[k])
                            tlist.append(v)
                            tpl[k] = tlist
                        elif isinstance(tpl[k], dict) and v:
                            tdict = deepcopy(tpl[k])
                            tdict.update(v)
                            tpl[k] = tdict
                        elif isinstance(tpl[k], bool):
                            t = deepcopy(tpl[k])
                            t = bool(v)
                            tpl[k] = t
                        elif isinstance(tpl[k], tuple) and v:
                            tlist = deepcopy(tpl[k])
                            tmp = []
                            tmp.append(v)
                            tlist += tuple(tmp)
                            tpl[k] = tlist

                    data.append(tpl)
                else:
                    fu = fu[0]
                    for k,v in d.iteritems():
                        if isinstance(fu[k], basestring) and v:
                            fu[k] = v
                        elif isinstance(fu[k], list) and v:
                            tlist = deepcopy(fu[k])
                            tlist.append(v)
                            fu[k] = list(set(tlist))
                            fu[k].sort(key=tlist.index)
                        elif isinstance(fu[k], dict) and v:
                            tdict = deepcopy(fu[k])
                            tdict.update(v)
                            fu[k] = tdict
                        elif isinstance(tpl[k], bool):
                            t = deepcopy(tpl[k])
                            t = bool(v)
                            tpl[k] = t
                        elif isinstance(fu[k], tuple) and v:
                            tlist = deepcopy(fu[k])
                            tmp = []
                            tmp.append(v)
                            tlist += tuple(tmp)
                            fu[k] = tuple(tlist)
            return data
        return _
    return dec

def transfer2jsonwithoutset(column, ispagination=False):
    """
    ? : key
    ! : string
    @ : list
    # : dict
    $ : bool
    & : tuple
    """

    def dec(func):
        @wraps(func)
        def _(*args, **kwargs):
            t_map = {
                '?': "key",
                '!': "",
                '@': [],
                '#': {},
                '$': False,
                '&': (),
                '~': ['~'],

            }
            count = 0
            if ispagination:
                results, count = func(*args, **kwargs)
            else:
                results = func(*args, **kwargs)
            if not isinstance(results, list):
                raise TypeError('should be a list')

            # 原始 键值
            origin_keys = [key.strip() for key in column.split('|')]
            # 键值和类型对应的 字典
            result_map = {
                key.strip()[1:]: t_map.get(key.strip()[0])
                for key in column.split('|')
            }
            # 找到 ? 为前缀的键值作为 key
            key_of_data = list(filter(lambda x: '?' in x, origin_keys))[0][1:]
            # result dict
            results_dict = [{item: getattr(result, item) for item in result_map.keys()} for result in results]

            data = {}
            for result in results_dict:
                if result.get(key_of_data) in data.keys():
                    temp = data.get(result.get(key_of_data))
                    for key, value in result_map.items():
                        data_value = result.get(key)
                        if isinstance(value, str) and data_value:
                            temp[key] = data_value
                        elif isinstance(value, list) and data_value:
                            t_list = deepcopy(temp[key])
                            t_list.append(data_value)
                            temp[key] = list(t_list)
                        elif isinstance(value, dict) and data_value:
                            tdict = deepcopy(temp[key])
                            tdict.update(data_value)
                            temp[key] = tdict
                        elif isinstance(value, bool):
                            t = bool(data_value)
                            temp[key] = t
                        elif isinstance(value, tuple) and data_value:
                            t_list = deepcopy(temp[key])
                            tmp = [data_value]
                            t_list += tuple(tmp)
                            temp[key] = tuple(t_list)
                else:
                    temp = deepcopy(result_map)
                    for key, value in result_map.items():
                        data_value = result.get(key)
                        if isinstance(value, str) and data_value is not None:
                            temp[key] = data_value
                        elif value == ['~']:
                            tjlist = json.loads(data_value) if data_value else []
                            temp[key] = tjlist
                        elif isinstance(value, list) and data_value:
                            temp[key] = [data_value]
                        elif isinstance(value, dict) and data_value:
                            temp[key] = {data_value}
                        elif isinstance(value, bool):
                            temp[key] = bool(data_value)
                        elif isinstance(value, tuple) and data_value:
                            temp[key] = tuple([data_value])

                data.update({result.get(key_of_data): temp})
            if ispagination:
                return list(data.values()), count
            else:
                return list(data.values())

        return _

    return dec

def slicejson(settings):

    def _slicejson(ret):
        config = [setting.split('|') for setting in settings]
        for conf in config:
            na = [[dict(i) for i in map(lambda x: zip((conf[1],conf[2]), x), zip(r.get(conf[3]),r.get(conf[4])))] for r in ret]
            for index, item in enumerate(ret):
                for k in [conf[3], conf[4]]:
                    del item[k]
                item[conf[0]] = na[index]
        return ret

    def wrapper(func):
        @wraps(func)
        def _(*args, **kwargs):
            ret = func(*args, **kwargs)
            return _slicejson(ret)
        return _
    return wrapper


def validation(validate_name = None):

    def validate_required(key, value):
        request_value = request.json.get(key)
        expect_value = value
        if request_value is None:
            return False, json_detail_render(201, [], "{} is required".format(key))
        return True, 1


    def validate_min_length(key, value):
        request_value = request.json.get(key)
        expect_value = value
        if request_value is not None and len(request_value) < expect_value:
            return False, json_detail_render(202, [], "{} min length is {}".format(key, value))
        return True, 1


    def validate_max_length(key, value):
        request_value = request.json.get(key)
        expect_value = value
        if request_value is not None and len(request_value) > expect_value:
            return False, json_detail_render(202, [], "{} max length is {}".format(key, value))
        return True, 1

    def validate_type(key, value):
        ttype_dict = {
            'list': list,
            'basestring': basestring,
            'dict': dict,
            'int': int,
            'bool': bool,
        }
        request_value = request.json.get(key)
        expect_value = value
        if request_value is not None and not isinstance(request_value, ttype_dict.get(value)):
            return False, json_detail_render(203, [], "{} should be a {}".format(key, value))
        return True, 1

    KEY_FUNC_MAP = {
        'required': validate_required,
        'min_length': validate_min_length,
        'max_length': validate_max_length,
        'type': validate_type,
    }

    def wrapper(func):
        @wraps(func)
        def _(*args, **kwargs):
            protocol, vname = validate_name.split(':')
            if request.method == protocol:
                all_json = YML_JSON
                validate_json = deepcopy(all_json.get(vname))
                del validate_json['returnvalue']
                for item, settings in validate_json.items():
                    for key, value in settings.items():
                        f = KEY_FUNC_MAP.get(key)
                        ret = f(item, value)
                        if not ret[0]:
                            return ret[1]
            return func(*args, **kwargs)
        return _
    return wrapper










