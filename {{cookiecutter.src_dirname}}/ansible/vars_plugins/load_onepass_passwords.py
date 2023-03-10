"""
References for creating a vars plugin:

* https://docs.ansible.com/ansible/latest/plugins/vars.html
* https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#vars-plugins
* https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/vars/host_group_vars.py

"""
__metaclass__ = type

import pathlib

from ansible.errors import AnsibleError
from ansible.plugins.vars import BaseVarsPlugin

# Something like the following should get you what you need here:
# pip install -e ~/projects/level12-cli-src/[onepass]
from level12.libs.ansible import onepass_lookup

map_secrets_fpath = pathlib.Path(__file__).parent.parent.joinpath('files', 'map_secrets.py')
map_secrets_globals = {}
with map_secrets_fpath.open() as fo:
    exec(fo.read(), map_secrets_globals)

op_result = onepass_lookup(
    map_secrets_globals['varmap'], map_secrets_globals['onepass_vault'], jsonify=True
)


class VarsModule(BaseVarsPlugin):
    def get_vars(self, loader, path, entities, cache=True):
        if op_result.exc:
            msg = 'unhandled exception when running lookup-passwords'
            raise AnsibleError('{}\n{}'.format(msg, op_result.exc))

        # A simple error message that just needs to be shown to the user.  Use AnsibleError
        # so that the message is displayed nicely and the playbooks stop running.
        if op_result.error:
            raise AnsibleError(op_result.error)

        return op_result.vars

