import ctypes as CTYPES

_libgrok_so = CTYPES.cdll.LoadLibrary('libgrok.dylib')

GROK_OK = 0

class _grok_match(CTYPES.Structure):
    _fields_ = [("grok_t", CTYPES.c_void_p),
                ("subject", CTYPES.c_char_p),
                ("start", CTYPES.c_int),
                ("end", CTYPES.c_int)]

_grok_match_p = CTYPES.POINTER(_grok_match)

_grok_new = _libgrok_so.grok_new
_grok_new.argtypes = []
_grok_new.restype = CTYPES.c_void_p

_grok_free = _libgrok_so.grok_free
_grok_free.argtypes = [CTYPES.c_void_p]

_grok_compile = _libgrok_so.grok_compile
_grok_compile.argtypes = [CTYPES.c_void_p, CTYPES.c_char_p]
_grok_compile.restype = CTYPES.c_int

_grok_exec = _libgrok_so.grok_exec
_grok_exec.argtypes = [CTYPES.c_void_p, CTYPES.c_char_p, _grok_match_p]
_grok_exec.restype = CTYPES.c_int

_grok_pattern_add = _libgrok_so.grok_pattern_add
_grok_pattern_add.argtypes = [CTYPES.c_void_p,
                              CTYPES.c_char_p, CTYPES.c_size_t,
                              CTYPES.c_char_p, CTYPES.c_size_t]
_grok_pattern_add.restype = CTYPES.c_int

_grok_patterns_import_from_file = _libgrok_so.grok_patterns_import_from_file
_grok_patterns_import_from_file.argtypes = [CTYPES.c_void_p, CTYPES.c_char_p]
_grok_patterns_import_from_file.restype = CTYPES.c_int

_grok_match_get_named_substring = _libgrok_so.grok_match_get_named_substring
_grok_match_get_named_substring.argtypes = [_grok_match_p, CTYPES.c_char_p, CTYPES.POINTER(CTYPES.c_char_p), CTYPES.POINTER(CTYPES.c_int)]
_grok_match_get_named_substring.restype = CTYPES.c_int

_grok_match_walk_init = _libgrok_so.grok_match_walk_init
_grok_match_walk_init.argtypes = [_grok_match_p]

_grok_match_walk_next = _libgrok_so.grok_match_walk_next
_grok_match_walk_next.argtypes = [_grok_match_p,
                                    CTYPES.POINTER(CTYPES.c_char_p),
                                    CTYPES.POINTER(CTYPES.c_int),
                                    CTYPES.POINTER(CTYPES.c_char_p),
                                    CTYPES.POINTER(CTYPES.c_int)]
_grok_match_walk_next.restype = CTYPES.c_int

_grok_match_walk_end = _libgrok_so.grok_match_walk_end
_grok_match_walk_end.argtypes = [_grok_match_p]
