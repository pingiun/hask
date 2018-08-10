# flake8: noqa
from __future__ import division, print_function, absolute_import

# Core language

## Typeclass instance declaration
from hask.lang.syntax import instance

## Operator sections
from hask.lang.syntax import __

## Guard expressions
from hask.lang.syntax import guard
from hask.lang.syntax import c
from hask.lang.syntax import otherwise
from hask.lang.syntax import NoGuardMatchException

## Lists/list comprehensions
from hask.lang.lazylist import L

## ADT creation
from hask.lang.syntax import data
from hask.lang.syntax import d
from hask.lang.syntax import deriving

## Type signatures
from hask.lang.syntax import sig
from hask.lang.syntax import H
from hask.lang.syntax import t
from hask.lang.syntax import func
from hask.lang.type_system import TypeSignatureError

## Pattern matching
from hask.lang.syntax import caseof
from hask.lang.syntax import m
from hask.lang.syntax import p
from hask.lang.syntax import IncompletePatternError

## REPL tools
from hask.lang.syntax import _t
from hask.lang.syntax import _i
from hask.lang.syntax import _q

## Type system/typeclasses
from hask.lang.type_system import typeof
from hask.lang.type_system import has_instance
from hask.lang.type_system import Typeclass
from hask.lang.type_system import Hask

# Basic Typeclasses
from hask.lang.typeclasses import Read
from hask.lang.typeclasses import Show
from hask.Data.Eq import Eq
from hask.Data.Ord import Ord
from hask.lang.lazylist import Enum
from hask.lang.typeclasses import Bounded
from hask.Data.Num import Num
from hask.Data.Num import Real
from hask.Data.Num import Integral
from hask.Data.Num import Fractional
from hask.Data.Num import Floating
from hask.Data.Num import RealFrac
from hask.Data.Num import RealFloat
from hask.Data.Functor import Functor
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad
from hask.Data.Traversable import Traversable
from hask.Data.Foldable import Foldable

# Standard types
from hask.Data.Maybe import Maybe
from hask.Data.Maybe import Just
from hask.Data.Maybe import Nothing
from hask.Data.Maybe import in_maybe

from hask.Data.Either import Either
from hask.Data.Either import Left
from hask.Data.Either import Right
from hask.Data.Either import in_either

from hask.Data.Ord import Ordering
from hask.Data.Ord import LT
from hask.Data.Ord import EQ
from hask.Data.Ord import GT
