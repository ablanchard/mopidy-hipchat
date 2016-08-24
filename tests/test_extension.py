from __future__ import unicode_literals

import unittest

from mopidy_hipchat import Extension


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        config = Extension().get_default_config()
        self.assertIn('[hipchat]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        schema = Extension().get_config_schema()
        self.assertIn('api_key', schema)
        self.assertIn('api_key_header_name', schema)
        self.assertIn('webhook_url', schema)
