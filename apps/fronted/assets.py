#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/22
    Time: 10:04
"""

from flask_assets import Environment, Bundle

css_overholt = Bundle('/lees/overholt.css',
                      filters='less', output='css/overholt.css',
                      debug=False)

css_all = Bundle('css/bootstrap.min.css', css_overholt,
                 'css/bootstrap-responsive.min.css',
                 filters='cssmin', output='css/overholt.min.css')

js_vendor = Bundle("js/vendor/jquery-1.10.1.min.js",
                   "js/vendor/bootstrap-2.3.3.min.js",
                   filters="jsmin", output="js/vendor.min.js")

js_main = Bundle("coffee/*.coffee", filters="coffeescript", output="js/main.js")


def init_app(app):
    webassets = Environment(app)
    webassets.register("css_all", css_all)
    webassets.register("js_vendor", js_vendor)
    webassets.register("js_main", js_main)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
