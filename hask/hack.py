#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

'''General utilities not related with main `hask` intentions.

Definitions of this module are candidates for migration to another package,
for example `xoutil`.

'''

from __future__ import division, print_function, absolute_import

from xoutil.decorator.meta import decorator


import sys
import types

if sys.version[0] == '2':
    __python_builtins__ = {
        types.BooleanType, types.BufferType, types.BuiltinFunctionType,
        types.BuiltinMethodType, types.ClassType, types.CodeType,
        types.ComplexType, types.DictProxyType, types.DictType,
        types.DictionaryType, types.EllipsisType, types.FileType,
        types.FloatType, types.FrameType, types.FunctionType,
        types.GeneratorType, types.GetSetDescriptorType, types.InstanceType,
        types.IntType, types.LambdaType, types.ListType, types.LongType,
        types.MemberDescriptorType, types.MethodType, types.ModuleType,
        types.NoneType, types.NotImplementedType, types.ObjectType,
        types.SliceType, types.StringType, types.StringTypes,
        types.TracebackType, types.TupleType, types.TypeType,
        types.UnboundMethodType, types.UnicodeType, types.XRangeType, set,
        frozenset}

else:
    __python_builtins__ = {
        bool, dict, type(Ellipsis), float, int, type(None), str, tuple,
        complex, list, set, frozenset, slice,
        type, types.BuiltinFunctionType, types.BuiltinMethodType,
        types.CodeType, types.DynamicClassAttribute, types.FrameType,
        types.FunctionType, types.GeneratorType, types.GetSetDescriptorType,
        types.LambdaType, types.MappingProxyType, types.MemberDescriptorType,
        types.MethodType, types.ModuleType, types.TracebackType}

del types, sys


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


# TODO: Next construction must go in `xoutil.decorator`, and -maybe- deprecate
# `instantiate`.

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
      ...         res = '"{}" instance named "{}"'
      ...         return res.format(type(self).__name__, self.name)
      ...
      ...     __repr__ = __str__

      >>> foo
      '"foo" instance named "bar"'

      >>> isinstance(foo, type)
      False

    New Python 3 ``super`` style could be used in these definitions without
    any problem; but take special care in Python 2, we advise direct call of
    the base class method (``BaseClass.method(self, ...)``), or calculating
    the type (``super(type(self), self).method(...)``).  Watch the second case
    if you inherits from the class like in ``class SubFoo(type(foo))``.

    '''
    return target(*args, **kwargs)
