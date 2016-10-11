#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 9:55
"""

from __future__ import absolute_import

from functools import wraps

from flask import jsonify
from flask_login import login_required

from .models import User
from apps.common import factory
from apps.common.DBCore import OverholtError, OverholtFormError
from apps.common.DBCore import Service
from apps.common.helpers import JSONEncoder, register_blueprints


class UserService(Service):
    __model__ = User


def create_app(app=None, settings_override=None, register_security_blueprint=True):
    app = app or factory.create_app(__name__, __path__, settings_override,
                                    register_security_blueprint=register_security_blueprint)
    app.json_encoder = JSONEncoder

    app.errorhandler(OverholtError)(on_overholt_error)
    app.errorhandler(OverholtFormError)(on_overholt_form_error)
    app.errorhandler(404)(on_404)
    register_blueprints(app, __name__, __path__)

    return app


def on_overholt_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_overholt_form_error(e):
    return jsonify(dict(errors=e.errors)), 400


def on_404(e):
    return jsonify(dict(error="Not Found")), 404


def route(bp, *args, **kwargs):
    # kwargs.setdefault("strict_slashes", False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        # @login_required
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
