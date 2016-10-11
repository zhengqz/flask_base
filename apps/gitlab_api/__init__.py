#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/27
    Time: 15:37
"""
from __future__ import absolute_import

from functools import wraps

from flask import jsonify

from apps.common import factory
from apps.common.helpers import register_blueprints, JSONEncoder


def create_app(app=None, settings_override=None, register_security_blueprint=True):
    app = app or factory.create_app(__name__, __path__, settings_override,
                                    register_security_blueprint=register_security_blueprint)
    app.json_encoder = JSONEncoder

    register_blueprints(app, __name__, __path__)

    return app


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            status = 200
            ret = f(*args, **kwargs)
            if isinstance(ret, tuple):
                status = ret[1]
                ret = ret[0]
            return jsonify(dict(data=ret)), status

        return f

    return decorator
