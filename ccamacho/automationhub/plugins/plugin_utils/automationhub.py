"""Collection automationhub driver."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import yaml

from collections import namedtuple
from ansible.galaxy.api import GalaxyAPI
from ansible.galaxy.api import _urljoin

from ansible.cli.galaxy import GalaxyCLI
from ansible.galaxy.token import GalaxyToken
from ansible.galaxy.role import GalaxyRole
from ansible.errors import AnsibleError, AnsibleOptionsError
from ansible.playbook.role.requirement import RoleRequirement

from ansible.galaxy.collection import build_collection


class AutomationHub(object):

    def __init__(self, options=None):
        options = options or {}
        opts = {
            'verbosity': 3,
            'force': False,
            'role_file': None,
            'keep_scm_meta': False,
            'api_server': 'https://galaxy.ansible.com',
            'ignore_errors': False,
            'no_deps': False,
            'offline': False,
        }

        opts.update(options)
        Options = namedtuple('Options', sorted(opts))
        self.options = Options(**opts)
        self.galaxy = None
    

    def get_namespace(self):
        """
        searches for the existance of a namespace given a namespace
        """
        page_size = 1       
        tokken = GalaxyToken(token=self.options.token)
        api = GalaxyAPI(self.galaxy, "test", self.options.api_server, token=tokken)
        try:
            what= 'namespaces'
            url = _urljoin(api.api_server,'api', api.available_api_versions['v1'], what, "?name="+ self.options.namespace.split("/")[0]+"&page_size="+str(page_size))
            data = api._call_galaxy(url)
            if data['count'] == 0:
                print("This namespace does not exists.")
                return False
            else:
                print("This namespace exists.")
                return True
        except Exception as error:
            raise AnsibleError("get_namespace failed with: %s" % (error))

    def collection_build(self):
        """
        build a collection
        """
        try:
            in_path = GalaxyCLI._resolve_path(self.options.input_path)
            build_collection(in_path, self.options.output_path, True)
            return True
        except Exception as error:
            raise AnsibleError("collection_build failed with: %s" % (error))


if __name__ == '__main__':
    options={'namespace':'kubeinit/kubeinit', 'token':'thisisatoken'}
    galaxy = AutomationHub(options=options)
    galaxy.get_namespace()
    galaxy.collection_build()

    # galax.get_collection_metadata()
    # galax.install_collection()
    # galax.publish_collection()
