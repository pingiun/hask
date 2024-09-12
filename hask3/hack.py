#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

'''General utilities not related with `hask` intentions.

Definitions of this module are candidates for migration to another package and
use them from there.

'''

import sys
import types

__python_builtins__ = {

    bool, dict, type(Ellipsis), float, int, type(None), str, tuple,
    complex, list, set, frozenset, slice, Exception,
    type, types.BuiltinFunctionType, types.BuiltinMethodType,
    types.CodeType, types.DynamicClassAttribute, types.FrameType,
    types.FunctionType, types.GeneratorType, types.GetSetDescriptorType,
    types.LambdaType, types.MappingProxyType, types.MemberDescriptorType,
    types.MethodType, types.ModuleType, types.TracebackType}

__python_function_types__ = tuple({
    types.FunctionType, types.LambdaType, types.MethodType,
    types.BuiltinFunctionType, types.BuiltinMethodType})


# Magic Names

_OPS = {
    # < <= == != > >=
    'comparison': {'lt', 'le', 'eq', 'ne', 'gt', 'ge'},
    'object-base': {'call', 'delattr', 'bool'},
    'context-manager': {'enter', 'exit'},
    # `obj[key]` `obj[key] = value` `del obj[key]` `key in obj` ...
    # length_hint?
    'container': {'getitem', 'setitem', 'delitem', 'contains', 'len', 'iter',
                   'reversed', 'missing'},
    'math': {'round', 'trunc', 'floor', 'ceil'},
    # - + abs() ~
    'arithmetic-unary': {'neg', 'pos', 'abs', 'invert'},
    # + - * @ / // % divmod() ** << >> & ^ |
    'arithmetic-binary': {'add', 'sub', 'mul', 'matmul', 'truediv',
                          'floordiv', 'mod', 'divmod', 'pow', 'lshift',
                          'rshift', 'and', 'xor', 'or'},
}

_MAGICS = set.union(
    {f'{p}{o}' for p in 'ri' for o in _OPS['arithmetic-binary']},
    *_OPS.values())


def settle_magic_methods(fn, names=_MAGICS):
    '''Decorator to settle all magic methods to function `fn`.

    Copied from `xoutil.decorator.settle`.

    '''
    names = (f'__{name}__' for name in names)

    def inner(target):
        try:
            if __sphinx_build__:
                return target
        except NameError:
            pass
        for attr in names:
            setattr(target, attr, fn)
        return target

    return inner


# Utilities

def safe_issubclass(cls, class_or_tuple):
    from inspect import isclass
    return isclass(cls) and issubclass(cls, class_or_tuple)


def isin(a, b):
    '''Same as ``a in b`` but using ``is`` operator to compare.'''
    return any(a is item for item in b)


def is_iterator(item):
    import sys
    name = 'next' if sys.version[0] == '2' else '__next__'
    return hasattr(item, name)


def is_collection(m):
    '''True if `m` is a collection.

    Strings are not collections.

    '''
    return hasattr(m, '__iter__') and not isinstance(m, str)


def is_builtin(cls):
    """Test whether a class or type is a Python builtin.

    :param cls: The class or type to examine.

    :returns: True if a type is a Python builtin type, and False otherwise.

    """
    return cls in __python_builtins__


def is_python_function(fn):
    '''Test whether an object is a Python function.'''
    return isinstance(fn, __python_function_types__)


def nt_to_tuple(nt):
    """Convert a namedtuple instance to a tuple.

    Even if the instance's __iter__ method has been changed.  Useful for
    writing derived instances of typeclasses.

    :param nt: namedtuple instance.

    :returns: A tuple containing each of the items in nt

    """
    return tuple(getattr(nt, f) for f in type(nt)._fields)


def decorator(caller):
    '''Eases the creation of decorators with arguments.

    Copied from `xoutil.decorator.meta.decorator`.

    '''
    from functools import wraps, partial
    from types import FunctionType as function

    @wraps(caller)
    def outer_decorator(*args, **kwargs):
        try:
            from zope.interface import Interface
        except ImportError:
            Interface = None
        if (len(args) == 1 and not kwargs and
            (isinstance(args[0], (function, type)) or
             issubclass(type(args[0]), type(Interface)))):
            func = args[0]
            return caller(func)
        elif len(args) > 0 or len(kwargs) > 0:
            def _decorator(func):
                return partial(caller, **kwargs)(*((func, ) + args))
            return _decorator
        else:
            return caller
    return outer_decorator


# TODO: Migrate to `xoutil.decorator`, and -maybe- deprecate `instantiate`.
@decorator
def objectify(target, *args, **kwargs):
    '''Instantiate a class returning a singleton object.

    Every argument, positional or keyword, is passed as such when invoking the
    target to create the resulting object.  The following code sample show
    this::

      >>> @objectify(name='bar')
      ... class foo(object):
      ...     def __init__(self, name='<empty>'):
      ...         self.name = name
      ...
      ...     def __str__(self):
      ...         res = f'{type(self).__name__}({self.name})'
      ...         return res
      ...
      ...     __repr__ = __str__

      >>> foo
      'foo(bar)'

      >>> isinstance(foo, type)
      False

    New Python 3 ``super`` style could be used in these definitions without
    any problem; but take special care in Python 2, we advise direct call of
    the base class method (``BaseClass.method(self, ...)``), or calculating
    the type (``super(type(self), self).method(...)``).  Watch the second case
    if you inherits from the class like in ``class SubFoo(type(foo))``.

    '''
    return target(*args, **kwargs)


del types, sys
