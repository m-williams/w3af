'''
test_dns_wildcard.py

Copyright 2012 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from w3af.plugins.tests.helper import PluginTest, PluginConfig


class TestDNSWildcard(PluginTest):

    base_url = 'http://moth/'

    _run_configs = {
        'cfg': {
            'target': base_url,
            'plugins': {'infrastructure': (PluginConfig('dns_wildcard'),)}
        }
    }

    def test_wildcard(self):
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        infos = self.kb.get('dns_wildcard', 'dns_wildcard')

        self.assertEqual(len(infos), 2, infos)

        expected = set(['Default virtual host', 'No DNS wildcard'])

        self.assertEqual(expected,
                         set([i.get_name() for i in infos]))
