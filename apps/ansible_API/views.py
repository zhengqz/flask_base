#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/27
    Time: 11:33
"""

from flask import Blueprint, jsonify

from . import route
from .adHoc import AdHocRun

bp = Blueprint("ansible_adhoc", __name__, url_prefix="/ansible")


@route(bp, "/adhoc")
def run_adhoc():
    name = "ansible"
    pattern = "all"
    module_name = "shell"
    module_args = "echo 'wahaha wacaca'>/tmp/test"

    print(AdHocRun().run(name, pattern, module_name=module_name, module_args=module_args))
    return "ok"
