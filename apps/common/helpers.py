#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:19
"""

from __future__ import absolute_import

import importlib
import pkgutil

from flask import Blueprint
from flask.json import JSONEncoder as BaseJSONEncoder


def register_blueprints(app, package_name, package_path):
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module("%s.%s" % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class JSONEncoder(BaseJSONEncoder):
    def default(self, obj):
        if isinstance(obj, JSONSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JSONSerializer(object):
    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()
        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)

        for key, modifier in modifiers.iteritems():
            value = getattr(self, key)
            rv[key] = modifier(value, self)

        for key in hidden:
            rv.pop(key, None)
        return rv
