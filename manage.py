#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/21
    Time: 18:05
"""
from flask_script import Manager

from apps.api import create_app as api
from apps.fronted import create_app as frontend
from apps.ansible_API import create_app as ansible
# from apps.gitlab_api import create_app as gitlab
from apps.git_api import create_app as git
from apps.scripts import CreateUserCommand, ListUsersCommand, DeleteUserCommand, InitDB

app = api()
app = frontend(app)
# app = ansible(app)
# app = gitlab(app)
app = git(app)
print(app.url_map)

manager = Manager(app)
manager.add_command("create_user", CreateUserCommand)
manager.add_command("delete_user", DeleteUserCommand)
manager.add_command("list_users", ListUsersCommand)
manager.add_command("init_db", InitDB)

if __name__ == "__main__":
    manager.run()
