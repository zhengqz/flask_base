#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:03
"""

# from flask_mail import Mail
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# mail = Mail()

security = Security()


class OverholtError(Exception):
    def __init__(self, msg):
        self.msg = msg


class OverholtFormError(Exception):
    def __init__(self, errors=None):
        self.errors = errors


class Service(object):
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError("%s is not of type %s" % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()
