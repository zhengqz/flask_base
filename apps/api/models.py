#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:59
"""

from __future__ import absolute_import

from datetime import datetime

from flask_security import RoleMixin, UserMixin

from apps.common.DBCore import db
from apps.common.helpers import JSONSerializer

role_user = db.Table(
    'role_user',
    db.Column('user_id', db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)


class Role(RoleMixin, db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __eq__(self, other):
        return (self.name == other.name or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return (self.name != other.name and
                self.name != getattr(other, 'name', None))


class UserJsonSerializer(JSONSerializer):
    __json_public__ = ["id", "username", "email"]


class User(UserJsonSerializer, UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(15))
    current_login_ip = db.Column(db.String(15))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=False)
    roles = db.relationship("Role", secondary=role_user,
                            backref=db.backref('user', lazy='dynamic'))
