#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/29
    Time: 10:48
"""
import os.path

from git import Repo

join = os.path.join


def git_clone(remote_path, work_dir):
    Repo.clone_from(remote_path, work_dir)

def get_repo(work_dir):
    if os.path.exists(work_dir) and os.path.isdir(work_dir):
        repo = Repo(work_dir)
    else:
        repo = None
    return repo


def add_file(repo, filePath=None, commit_msg=""):
    """
    filePath relative to workspace dir
    """

    if filePath is None or filePath == r".":
        repo.git.add(A=True)

    elif isinstance(filePath, basestring) and filePath != r".":
        new_file_path = join(repo.working_tree_dir, filePath)
        index = repo.index

        index.add([new_file_path])
        print(filePath, new_file_path)
        _commit(index, commit_msg)



def _commit(index, commit_msg):
    index.commit(commit_msg)


if __name__ == "__main__":
    git_clone("git@192.168.8.29:atom/ansible.git","C:\Users\qinzhou.zheng\config_files")
