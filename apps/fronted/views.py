#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:13
"""
from __future__ import absolute_import

import os.path


from flask import Blueprint, render_template, request, redirect, url_for, current_app

from . import route

join = os.path.join

bp = Blueprint('dashboard', __name__, template_folder="templates")



#windows
GIT_DATA = os.path.sep.join(["apps", "git_api", "git-data"])


@route(bp, '/')
def index():
    return render_template("dashboard.html")


@route(bp, "/git/file/add", methods=["GET", "POST"])
def add_file():
    if request.method == "GET":
        return render_template("add_file.html")
    elif request.method == "POST":
        fileName = request.form.get("file_name", "")
        content = request.form.get("content", "")
        commit_msg = request.form.get("commit_msg", "")
        branch = request.form.get("branch", "")
        from apps.git_api import controller
        from apps.common import utils
        db_file = current_app.config["DB_FILE"]
        proj_name = utils.get_data(db_file, "project_name")
        workDir = join(GIT_DATA, proj_name)

        file_path = join(workDir, fileName)
        from apps.common import utils

        file_path = utils.path_sep(file_path)

        with open(file_path, "wb") as f:
            f.write(content)

        repo = controller.get_repo(workDir)

        controller.add_file(repo, fileName, commit_msg)
        return "OK"


@route(bp, "/git/repo/add", methods=["GET", "POST"])
def add_repo():

    if request.method == "GET":
        return render_template("add_repo.html")
    elif request.method == "POST":
        remote_path = request.form.get("remote_path", "")
        work_dir = request.form.get("work_dir", "")

        from apps.common import utils
        db_file = current_app.config["DB_FILE"]
        utils.write_data(db_file, "project_name", work_dir)

        from apps.git_api import controller
        work_dir = join(GIT_DATA, work_dir)

        controller.git_clone(remote_path, work_dir)
        return redirect(url_for(".add_file"))


@route(bp, "/git/file/update", methods=["GET", "POST"])
def update_file():
    db_file = current_app.config["DB_FILE"]
    from apps.common import utils
    proj_name = utils.get_data(db_file, "project_name")
    workDir = join(GIT_DATA, proj_name)

    if request.method == "GET":
        content = ""
        fileName= "nginx.conf"
        file_path = join(workDir, fileName)
        with open(file_path) as f:
            content = f.read()
        context = dict(
            fileName=fileName,
            content = content
        )
        return  render_template("update_file.html",context=context)
    elif request.method == "POST":
        from apps.git_api import controller
        fileName = request.form.get("fileName")
        content = request.form.get("content")
        commit_msg = request.form.get("commit_msg","")
        file_path = join(workDir, fileName)
        with open(file_path, "wb") as f:
            f.write(content)
        print(file_path,"file")

        repo = controller.get_repo(workDir)

        controller.add_file(repo, fileName, commit_msg)
        return "Ok"
