#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 16:25
"""

from gevent.wsgi import WSGIServer

from apps.api import create_app as api
from apps.fronted import create_app as frontend

app = api()
app = frontend(app)

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
