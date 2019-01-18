# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

#
# Put this file in lookup_plugins/ alongside your playbooks.
#
# Lookup plugins can be called two ways: via with_ as a task loop construct,
# or via lookup('name').
#
# For further documentation see
# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# 

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
import httplib
import json
import urllib

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):

    def run(self, terms, inject=None, **kwargs):

        # lookups in general are expected to both take a list as input and
        # output a list.  This is done so they work with the looping 
        # construct 'with_'.
        results = []

        # the 8ball lookup does not require any input parameters
        conn = httplib.HTTPSConnection("8ball.delegator.com")
        question = urllib.pathname2url('Will a black cat cross me today?')
        conn.request('GET', '/magic/JSON/' + question)
        response = conn.getresponse()
        responseJson = response.read()

        # responseJson is JSON string like
        # {
        #  "magic": {
        #    "question": "Will a black cat cross me today?",
        #    "answer": "Outlook not so good",
        #    "type": "Contrary"
        #  }
        #}        
        responseObj = json.loads(responseJson)
        answer = responseObj['magic']['answer']

        # append answer to results
        results.append(answer)

        return results


