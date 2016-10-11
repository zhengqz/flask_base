#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 15:51
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from apps import api, fronted

app = fronted.create_app()
app = api.create_app(app)

application = DispatcherMiddleware(app, {
    "/test": app,  # /test and / is same
})

if __name__ == "__main__":
    run_simple("0.0.0.0", 5000, application, use_reloader=True, use_debugger=True)
