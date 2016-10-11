#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:42
"""
from werkzeug.urls import url_encode


class HTTPMethodOverrideMiddleware(object):
    bodyless_methods = frozenset(["GET", "HEAD", "OPTIONS", "DELETE"])

    def __init__(self, app, header_name=None, querystring_param=None, allowed_methods=None):
        header_name = header_name or 'X-HTTP-METHOD-OVERRIDE'
        self.app = app
        self.header_name = 'HTTP_' + header_name.replace("-", "_")
        self.qeurystring_param = querystring_param or '__METHOD__'
        self.allowed_methods = frozenset(
            allowed_methods or ["GET", "HEAD", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"])

    def _get_from_querystring(self, environ):
        if self.qeurystring_param in environ.get("QUERY_STRING", ""):
            args = url_encode(environ["QUERY_STRING"])
            return args.get(self.qeurystring_param)
        return None

    def _get_method_override(self, environ):
        return environ.get(self.header_name, None) or self._get_from_querystring(environ) or ''

    def __call__(self, environ, start_response, *args, **kwargs):
        method = self._get_from_querystring(environ)
        if method is None:
            return self.app(environ, start_response)
        else:
            method = method.upper()
        if method in self.allowed_methods:
            method = method.encode("ascii", "replace")
            environ['REQUEST_METHOD'] = method

        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'
        return self.app(environ, start_response)
