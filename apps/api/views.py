#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 11:14
"""

from __future__ import absolute_import

import time
from flask import Blueprint
from flask_login import current_user

from . import UserService
from . import route

bp = Blueprint("user", __name__, url_prefix="/user")


@route(bp, "/test")
def test():
    time.sleep(5)
    return "OK"

@route(bp, "/")
def whoami():
    users = current_user._get_current_object()
    return users

@route(bp, "/<user_id>")
def show(user_id):
    user = UserService()
    return user.get_or_404(user_id)
