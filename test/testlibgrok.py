import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libgrok import *

class GrokTestCase(unittest.TestCase):

    def setUp(self):
        self.grok = Grok()
        self.grok.add_patterns_from_file('test/patterns/base')

    def tearDown(self):
        del self.grok

    def test_grok_add_patterns_file(self):
        self.assertRaises(GrokError, self.grok.add_patterns_from_file, 'nosuchfile')

    def test_grok_compile(self):
        self.assertRaises(GrokError, self.grok.compile, '%{URI)')

    def test_grok_substring(self):
        self.grok.compile("%{URI}")
        match = self.grok('https://example.com/test/')
        self.assertEquals(match['URIPROTO'], 'https')
        self.assertEquals(match['URIPATH'], '/test/')
        self.assertEquals(match['foo'], None)

    def test_grok_substring_named(self):
        self.grok.compile("%{URI:foo}")
        match = self.grok('https://example.com/test/')
        self.assertEquals(match['URIPROTO'], 'https')
        self.assertEquals(match['URIPATH'], '/test/')
        self.assertEquals(match['foo'], 'https://example.com/test/')
        self.assertEquals(match['bar'], None)

    def test_grok_captures(self):
        self.grok.compile("%{URI}")
        match = self.grok('https://example.com/test/')
        self.assertTrue('HOSTNAME' in match.captures)
        self.assertEquals(match.captures['HOSTNAME'], 'example.com')
        self.assertTrue('URIPROTO' in match.captures)
        self.assertEquals(match.captures['URIPROTO'], 'https')
        self.assertTrue('URIPATH' in match.captures)
        self.assertEquals(match.captures['URIPATH'], '/test/')

    def test_grok_captures_named(self):
        self.grok.compile("%{URI:foo}")
        match = self.grok('https://example.com/test/')
        self.assertTrue('URI:foo' in match.captures)
        self.assertEquals(match.captures['URI:foo'], 'https://example.com/test/')

    def test_grok_execute(self):
        self.grok.compile("%{URI}")
        self.assertTrue(self.grok.execute('https://example.com/test/'))
        self.assertFalse(self.grok.execute('thisisnotauri.com'))

    def test_grok_call(self):
        self.grok.compile("%{URI}")
        self.assertTrue(self.grok('https://example.com/test/') != None)
        self.assertTrue(self.grok('thisisnotauri.com') == None)

if __name__ == "__main__":
    unittest.main()
