'''
test_preg_replace.py

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


class TestPreg(PluginTest):

    target_url = 'http://moth/w3af/audit/preg_replace/'

    _run_configs = {
        'cfg': {
            'target': target_url,
            'plugins': {
                'audit': (PluginConfig('preg_replace'),),
                'crawl': (
                    PluginConfig(
                        'web_spider',
                        ('only_forward', True, PluginConfig.BOOL)),
                )
            }
        }
    }

    def test_found_preg(self):
        # Run the scan
        cfg = self._run_configs['cfg']
        self._scan(cfg['target'], cfg['plugins'])

        # Assert the general results
        vulns = self.kb.get('preg_replace', 'preg_replace')
        self.assertEquals(len(vulns), 2)

        titles = all(['Unsafe preg_replace usage' == v.get_name() for v in vulns])
        self.assertEquals(titles, True)

        expected_results = (
            ('preg_all_regex.php', 'regex'),
            ('preg_section_regex.php', 'search')
        )

        found = [(str(v.get_url()), v.get_var()) for v in vulns]
        expected = [((self.target_url + end), param) for (end,
                    param) in expected_results]

        self.assertEquals(
            set(found),
            set(expected)
        )
