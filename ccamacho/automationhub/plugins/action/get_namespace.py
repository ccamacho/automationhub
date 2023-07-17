#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from ansible.plugins.action import ActionBase

try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible.errors import AnsibleActionFail

from ansible_collections.ccamacho.automationhub.plugins.plugin_utils.automationhub import AutomationHub

from ansible import context

argument_spec = {}
argument_spec.update(dict(
    api_server=dict(type="str"),
    token=dict(type="str"),
    namespace=dict(type="str"),
))

required_if = []
required_one_of = []
mutually_exclusive = []
required_together = []

class ActionModule(ActionBase):
    def __init__(self, *args, **kwargs):
        if not ANSIBLE_UTILS_IS_INSTALLED:
            raise AnsibleActionFail("ansible.utils is not installed. Execute 'ansible-galaxy collection install ansible.utils'")
        super(ActionModule, self).__init__(*args, **kwargs)
        self._supports_async = False
        self._supports_check_mode = True
        self._result = None

    # Checks the supplied parameters against the argument spec for this module
    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=dict(argument_spec=argument_spec),
            schema_format="argspec",
            schema_conditionals=dict(
                required_if=required_if,
                required_one_of=required_one_of,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
            ),
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def get_object(self, params):
        new_object = dict(
            api_server=params.get("api_server"),
            token=params.get("token"),
            namespace=params.get("namespace"),
        )
        return new_object

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result["changed"] = False
        self._check_argspec()

        api_server = self._task.args.get("api_server")
        token = self._task.args.get("token")
        namespace = self._task.args.get("namespace")

        options={'api_server': api_server, 'token':token, 'repo':namespace,}

        galaxy = AutomationHub(options=options)
        galaxy.get_namespace()

        self._result.update(dict(asdf="executed"))

        return self._result
