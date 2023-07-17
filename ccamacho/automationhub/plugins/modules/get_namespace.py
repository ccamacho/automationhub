#!/usr/bin/python


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: get_namespace

short_description: Verify if a namespace exists

version_added: "2.9.0"

author: "Carlos Camacho"

description:
  - "Verify if a namespace exists"

options:
  api_server:
    description:
      - The automationhub server to connect to.
    required: true
    type: str
  token:
    description:
      - The auth token.
    required: true
    type: str
  namespace:
    description:
      - The namespace to search for.
    required: true
    type: str
'''

EXAMPLES = '''
- name: Verify if a namespace exists
  ccamacho.automationhub.get_namespace:
    api_server: galaxy.ansible.com
    token: this_is_an_auth_token
    namespace: kubeinit
'''

RETURN = '''
'''
