#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 9:56
"""
from __future__ import absolute_import

from functools import wraps

from flask import render_template
# from flask_login import login_required

from . import assets
from apps.common import factory
from apps.common.helpers import register_blueprints


def create_app(app=None, settings_override=None):
    app = app or factory.create_app(__name__, __path__, settings_override)
    register_blueprints(app, __name__, __path__)
    assets.init_app(app)

    if not app.debug:
        for e in [500, 404]:
            app.errorhandler(e)(handler_error)
    return app


def handler_error(e):
    return render_template("errors/{}.html".format(e.code)), e.code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        # @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return f

    return decorator
