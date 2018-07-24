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


# Utilities


def safe_issubclass(cls, class_or_tuple):
    from inspect import isclass
    return isclass(cls) and issubclass(cls, class_or_tuple)
