import ctypes

_libgrok = ctypes.cdll.LoadLibrary('libgrok.dylib')

_grok_new = _libgrok.grok_new
_grok_new.argtypes = []
_grok_new.restype = ctypes.c_void_p

_grok_free = _libgrok.grok_free
_grok_free.argtypes = [ctypes.c_void_p]

_grok_compile = _libgrok.grok_compile
_grok_compile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_grok_compile.restype = ctypes.c_int

_grok_exec = _libgrok.grok_exec
_grok_exec.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
_grok_exec.restype = ctypes.c_int

_grok_pattern_add = _libgrok.grok_pattern_add
_grok_pattern_add.argtypes = [ctypes.c_void_p,
                              ctypes.c_char_p, ctypes.c_size_t,
                              ctypes.c_char_p, ctypes.c_size_t]
_grok_pattern_add.restype = ctypes.c_int

_grok_patterns_import_from_file = _libgrok.grok_patterns_import_from_file
_grok_patterns_import_from_file.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_grok_patterns_import_from_file.restype = ctypes.c_int


