import ctypes as CTYPES
from _libgrok import *

_fixed_buffer_size = 4096

class GrokError(Exception):
    def __init__(self, message=None, err=0):
        if message:
            Exception.__init__(self, message)
        else:
            Exception.__init__(self, self.error_to_message(err))

    def error_to_message(self, err):
        if err == 1:
            return "File not found"
        if err == 2:
            return "Pattern not found"
        if err == 3:
            return "Unexpected read size"
        if err == 4:
            return "Compile failed"
        if err == 5:
            return "Uninitialized"
        if err == 6:
            return "PCRE Error"
        if err == 7:
            return "No match"
        else:
            return "Unknown Error: %d" % (err)

class GrokMatch(object):
    def __init__(self):
        self._grok_match = _libgrok._grok_match()
        self._captures = None 

    @property
    def subject(self):
        return self._grok_match.subject

    @property
    def start(self):
        return self._grok_match.start

    @property
    def end(self):
        return self._grok_match.end

    @property
    def captures(self):
        if self._captures is None:
            self._captures = dict()
            for name, data in self.walk():
                self._captures[name] = data
        return self._captures

    def walk(self):
        _libgrok._grok_match_walk_init(self._grok_match)
        name = CTYPES.create_string_buffer( _fixed_buffer_size)
        name_ptr = CTYPES.c_char_p(CTYPES.addressof(name))
        name_len = CTYPES.c_int(0)
        data = CTYPES.create_string_buffer( _fixed_buffer_size)
        data_ptr = CTYPES.c_char_p(CTYPES.addressof(data))
        data_len = CTYPES.c_int(0)
        while _libgrok._grok_match_walk_next(self._grok_match,
                                                CTYPES.byref(name_ptr),
                                                CTYPES.byref(name_len),
                                                CTYPES.byref(data_ptr),
                                                CTYPES.byref(data_len)) == _libgrok.GROK_OK:
            yield name_ptr.value[:name_len.value], data_ptr.value[:data_len.value]
        _libgrok._grok_match_walk_end(self._grok_match)

    def __getitem__(self, k):
        substring = CTYPES.create_string_buffer( _fixed_buffer_size)
        substring_ptr  = CTYPES.c_char_p(CTYPES.addressof(substring))
        substring_len = CTYPES.c_int(0)
        ret = _libgrok._grok_match_get_named_substring(self._grok_match, k, CTYPES.byref(substring_ptr), CTYPES.byref(substring_len))
        if ret != _libgrok.GROK_OK:
            return None 
        return substring_ptr.value[:substring_len.value]

class Grok(object):

    def __init__(self):
        self._grok = _libgrok._grok_new()

    def __del__(self):
        _libgrok._grok_free(self._grok)

    def add_pattern(self, name, pattern):
        ret = _libgrok._grok_pattern_add(self._grok, name, len(name), pattern, len(pattern))
        if ret != _libgrok.GROK_OK:
            raise GrokError(err=ret)

    def add_patterns_from_file(self, filename):
        ret = _libgrok._grok_patterns_import_from_file(self._grok, filename)
        if ret != _libgrok.GROK_OK:
            raise GrokError(err=ret)

    def compile(self, pattern):
        ret = _libgrok._grok_compile(self._grok, pattern)
        if ret != _libgrok.GROK_OK:
            raise GrokError(err=ret)

    def execute(self, text, match=None):
        grok_match_p = None if match is None else CTYPES.pointer(match._grok_match)
        ret = _libgrok._grok_exec(self._grok, text, grok_match_p) 
        return ret == _libgrok.GROK_OK

    def __call__(self, text):
        match = GrokMatch()
        if self.execute(text, match):
            return match
        else:
            return None

