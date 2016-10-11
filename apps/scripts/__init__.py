#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 11:20
"""
from __future__ import absolute_import

from flask_script import Command

from .user import CreateUserCommand, DeleteUserCommand, ListUsersCommand
from apps.common.DBCore import db

__all__ = ["CreateUserCommand", "DeleteUserCommand", "ListUsersCommand", "InitDB"]


class InitDB(Command):
    """Init database"""
    def run(self):
        db.drop_all()
        db.create_all()
