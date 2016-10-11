#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/27
    Time: 15:39
"""

import base64
import json
import urllib

from tornado import httpclient


def encode_base64(content):
    return base64.b64encode(content)


def decode_base64(content):
    return base64.b64decode(content)


def client_request(url, method, headers, body=None):
    request = httpclient.HTTPRequest(
        url=url,
        method=method,
        headers=headers,
        body=body
    )
    client = httpclient.HTTPClient()
    resp = client.fetch(request)
    return resp.body


def create_file(host,headers, prj_id, file_path, branch_name, content, commit_message, encoding="base64"):
    if encoding != "text":
        content = encode_base64(content)

    URL = "/projects/{0}/repository/files".format(prj_id)

    URL = "%s%s" % (host, URL)
    body = dict(
        file_path=file_path,
        branch_name=branch_name,
        content=content,
        commit_message=commit_message,
        encoding=encoding
    )
    body = urllib.urlencode(body)

    ret = client_request(URL, "POST", headers, body)
    return ret


def delete_file(host,headers, prj_id, file_path, branch_name, commit_message):
    URL = "/projects/{0}/repository/files?file_path={1}&branch_name={2}&commit_message={3}".format(prj_id, file_path,
                                                                                                   branch_name,
                                                                                                   commit_message)

    URL = "%s%s" % (host, URL)
    ret = client_request(URL, "DELETE", headers)
    return ret


def update_file(host,headers, prj_id, file_path, branch_name, content, commit_message, encoding="base64"):
    if encoding != "text":
        content = encode_base64(content)
    URL = "/projects/{0}/repository/files".format(prj_id)

    URL = "%s%s" % (host, URL)
    body = dict(
        file_path=file_path,
        branch_name=branch_name,
        content=content,
        commit_message=commit_message,
        encoding=encoding
    )
    body = json.dumps(body)
    headers.update({'Content-Type': 'application/json; charset:UTF-8'})
    ret = client_request(URL, "PUT", headers, body)
    return ret


def get_file(host, headers,prj_id, file_path, ref):
    URL = "/projects/{0}/repository/files?file_path={1}&ref={2}".format(prj_id, file_path, ref)
    URL = "%s/%s" % (host, URL)
    ret = client_request(URL, "GET", headers)
    ret = json.loads(ret)
    encode_content = ret['content']
    ret['content'] = decode_base64(encode_content)
    return ret


if __name__ == "__main__":
    prj_id = 2
    file_path = "beibei/beibei_web/test"
    branch_name = "master"
    content = u"tets gor ipa"
    commit_message = "test"
    #
    # delete_file(prj_id, file_path, branch_name, commit_message)

    # ret = create_file(prj_id, file_path, branch_name, content, commit_message)
    # print(ret)
    # import time
    # time.sleep(5)
    # content = "modify"
    # commit_message = "modify haha"
    # ret = update_file(prj_id, file_path, branch_name, content, commit_message)
    # print(ret)

    ret = get_file(prj_id, file_path, branch_name)

    print(ret)
