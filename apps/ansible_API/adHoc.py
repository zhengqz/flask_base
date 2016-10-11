#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    Date: 2016/9/27
    Time: 10:54
"""
from __future__ import absolute_import

import json
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars import VariableManager


class ResultCallback(CallbackBase):
    def v2_runner_item_on_ok(self, result):
        host = result._host
        ret = json.dumps({host.name: result._result}, indent=4)
        # return ret


class AdHocRun(object):
    def __init__(self):
        self.options = namedtuple("Options",
                                  ['connection', 'module_name', 'module_path', 'module_args', 'forks', 'become',
                                   'become_method', 'become_user', 'check'])

    def run(self, name, pattern, gather_facts='no', module_name=None, module_args=None, module_path=None):
        variable_manager = VariableManager()
        loader = DataLoader()
        self.options = self.options(connection='smart', module_name=module_name, module_path=module_path,
                                    module_args=module_args, forks=100, become=None, become_method=None,
                                    become_user=None,
                                    check=False)
        passwords = dict(vault_pass='secret')
        result_callback = ResultCallback()
        inventory = Inventory(loader=loader, variable_manager=variable_manager)
        variable_manager.set_inventory(inventory)

        play_source = dict(
            name=name,
            hosts=pattern,
            gather_facts=gather_facts,
            tasks=[
                dict(action=dict(module=module_name or module_path, args=module_args)),
            ]
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        self._tqm = None
        try:
            self._tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=self.options,
                passwords=passwords,
                stdout_callback=result_callback,
            )

            result = self._tqm.run(play)

        finally:
            if self._tqm is not None:
                self._tqm.cleanup()
            if loader:
                loader.cleanup_all_tmp_files()
        return result
