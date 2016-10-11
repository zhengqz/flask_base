#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 9:59
"""
from __future__ import absolute_import

import os.path

from celery import Celery
from flask import Flask
from flask_security import SQLAlchemyUserDatastore

from .DBCore import db, security
from apps.api.models import User, Role
from .middleware import HTTPMethodOverrideMiddleware


def create_app(package_name, package_path, app=None, settings_overrider=None, register_security_blueprint=True):
    app = app or Flask(package_name, instance_relative_config=True)
    app.config.from_object("apps.settings")
    app.config.from_pyfile("settings.cfg", silent=True)
    app.config.from_object(settings_overrider)
    db.init_app(app)
    # mail.init_app(app)
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role),
                      register_blueprint=register_security_blueprint)

    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
    return app


def create_celery_app(app=None):
    app = app or create_app("base", os.path.dirname(__file__))
    celery = Celery(__name__)
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
