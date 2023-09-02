#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

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

argument_spec = {}
argument_spec.update(dict(
    input_path=dict(type="str"),
    output_path=dict(type="str"),
    timeout=dict(type="str"),
    token=dict(type="str"),
    api_key=dict(type="str"),
    ignore_certs=dict(type="str"),
    force=dict(type="str"),
    server=dict(type="str"),
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

    def get_collection_params(self, params):
        new_object = dict(
            input_path=params.get("input_path"),
            output_path=params.get("output_path"),
            timeout=params.get("timeout"),
            token=params.get("token"),
            api_key=params.get("api_key"),
            ignore_certs=params.get("ignore_certs"),
            force=params.get("force"),
            server=params.get("server"),
        )
        return new_object

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result["changed"] = False
        self._check_argspec()

        galaxy = AutomationHub(options=self.get_collection_params(self._task.args))
        galaxy.collection_build()

        self._result.update(dict(asdf="executed"))

        return self._result
