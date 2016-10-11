#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/10/8
    Time: 11:02
"""
from __future__ import absolute_import, print_function

import platform
import re
import shelve


def get_system():
    return platform.system()


def path_sep(filePath):
    _system = get_system()
    if _system == "Windows":
        pattern = re.compile(u"/")
        ret = re.sub(pattern, r"\\\\", filePath)
    elif _system == "Linux":
        pattern = re.compile(u"\\")
        ret = re.sub(pattern, u"/", filePath)
    else:
        ret = filePath
    return unicode(ret)


def get_data(db_file, attr):
    afile = shelve.open(db_file)
    ret = afile.get(attr)
    afile.close()
    return ret

def write_data(db_file, attr, data):
    afile = shelve.open(db_file)
    afile[attr] = data
    afile.sync()
    afile.close()




if __name__ == "__main__":
    write_data("test.db", "a", "1")
    print(get_data("test.db", "a"))