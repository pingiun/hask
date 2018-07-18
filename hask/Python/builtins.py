'''Typed wrappers for builtin Python functions.

This makes it easier to chain lots of things together in function composition
without having to manually add type signatures to Python builtins.

Each function is a `~hask.lang.type_system.TypedFunc`:class: replacement of
the corresponding Python builtin with the right signature.

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)

from ..lang import H

try:
    from __builtin__ import cmp as pycmp
except ImportError:
    def pycmp(a, b):
        if a == b:
            return 0
        elif a < b:
            return -1
        else:
            return 1

callable = callable ** (H/ "a" >> bool)
cmp = pycmp ** (H/ "a" >> "a" >> int)
delattr = delattr ** (H/ "a" >> str >> None)
divmod = divmod ** (H/ "a" >> "b" >> ("c", "c"))
getattr = getattr ** (H/ "a" >> str >> "b")
hasattr = hasattr ** (H/ "a" >> str >> bool)
hash = hash ** (H/ "a" >> int)
hex = hex ** (H/ int >> str)
isinstance = isinstance ** (H/ "a" >> "b" >> bool)
issubclass = issubclass ** (H/ "a" >> "b" >> bool)
len = len ** (H/ "a" >> int)
oct = oct ** (H/ int >> str)
repr = repr ** (H/ "a" >> str)
setattr = setattr ** (H/ "a" >> str >> "b" >> None)
sorted = sorted ** (H/ "a" >> list)
try:
    from __builtin__ import unichr as pyunichr
except ImportError:
    pyunichr = chr
    unicode = str

unichr = pyunichr ** (H/ int >> unicode)
