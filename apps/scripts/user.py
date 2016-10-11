#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 11:20
"""

from __future__ import absolute_import

from hashlib import md5

from flask_script import Command, prompt, prompt_pass
from flask_security import RegisterForm
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict

from apps.api import UserService


class CreateUserCommand(Command):
    """Create a user"""

    def run(self):
        md5_pass = md5()
        email = prompt("Email")
        username = prompt("UserName")
        password = prompt_pass("Password")
        password_confirm = prompt_pass("Confirm Password")
        data = MultiDict(dict(email=email, username=username, password=password, password_confirm=password_confirm))
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            # md5_pass.update(password)
            # password = md5_pass.hexdigest()
            new_user = register_user(email=email, username=username, password=password, active=False)
            print("\nUser created successfully")
            print("User(id=%s username=%s email=%s" % (new_user.id, new_user.username, new_user.email))
            return
        print("\nError creating user:")
        for errors in form.errors.values():
            print("\n".join(errors))


class DeleteUserCommand(Command):
    """Delete a user"""

    def run(self):
        email = prompt("Email")
        user = UserService()
        delete_user = user.first(email=email)
        if not delete_user:
            print("Invalid user")
            return
        user.delete(delete_user)
        print("User deleted successfully")


class ListUsersCommand(Command):
    """List all users"""

    def run(self):
        user = UserService()
        for u in user.all():
            print("<User: id:%s,username:%s,email=%s>" % (u.id, u.username, u.email))
