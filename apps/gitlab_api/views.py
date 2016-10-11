#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/27
    Time: 17:40
"""

# @route(bp, "/gitlab/update_file", methods=["POST"])
# def gitlab_update_file():
#     if request.method == "POST":
#         update_form = UpdateFileForm(request.form)
#         print(update_form, update_form.validate())
#         if update_form.validate_on_submit():
#
#             # get field from form
#             file_path = request.form.get("file_path")
#             branch_name = request.form.get("branch")
#             content = request.form.get("content")
#             commit_msg = request.form.get("commit_msg")
#             # get config from app
#             app = current_app
#             host = app.config["GITLAB_HOST"]
#             gitlab_token = app.config["PRIVATE_TOKEN"]
#             prj_id = app.config["PROJ_ID"]
#             headers = {"PRIVATE-TOKEN": gitlab_token}
#             # update gitlab file
#             update_file(host, headers, prj_id, file_path, branch_name, content, commit_msg)
#     return "OK"