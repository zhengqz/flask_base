#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 16:39
"""

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from apps.api import create_app as api
from apps.fronted import create_app as frontend

app = frontend()
app = api(app)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()
