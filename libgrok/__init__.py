from _libgrok import *

print dir()

class Grok(object):

    def __init__(self):
        self._grok = _libgrok._grok_new()

    def __del__(self):
        _libgrok._grok_free(self._grok)

    def add_pattern(self, name, pattern):
        _libgrok._grok_pattern_add(self._grok, name, len(name), pattern, len(pattern))

    def add_patterns_from_file(self, filename):
        _libgrok._grok_patterns_import_from_file(self._grok, filename)

    def compile(self, pattern):
        _libgrok._grok_compile(self._grok, pattern)

    def __call__(self, text):
        return _libgrok._grok_exec(self._grok, text, None)
