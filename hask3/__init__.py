# flake8: noqa
from . import lang
from . import Data
from . import Control
from . import Python


# Core language

## Typeclass instance declaration
from hask3.lang import instance

## Operator sections
from hask3.lang import __

## Guard expressions
from hask3.lang import guard
from hask3.lang import c
from hask3.lang import otherwise
from hask3.lang import NoGuardMatchException

## Lists/list comprehensions
from hask3.lang import L

## ADT creation
from hask3.lang import data
from hask3.lang import d
from hask3.lang import deriving

## Type signatures
from hask3.lang import sig
from hask3.lang import H
from hask3.lang import t
from hask3.lang import func
from hask3.lang import TypeSignatureError

## Pattern matching
from hask3.lang import caseof
from hask3.lang import p
from hask3.lang import m
from hask3.lang import IncompletePatternError

## REPL tools
from hask3.lang import _t
from hask3.lang import _i
from hask3.lang import _q

## Type system/typeclasses
from hask3.lang import typeof
from hask3.lang import has_instance
from hask3.lang import Typeclass
from hask3.lang import Hask


# Basic Typeclasses
from hask3.Prelude import Read
from hask3.Prelude import Show
from hask3.Prelude import Eq
from hask3.Prelude import Ord
from hask3.Prelude import Enum
from hask3.Prelude import Bounded
from hask3.Prelude import Num
from hask3.Prelude import Real
from hask3.Prelude import Integral
from hask3.Prelude import Fractional
from hask3.Prelude import Floating
from hask3.Prelude import RealFrac
from hask3.Prelude import RealFloat
from hask3.Prelude import Functor
from hask3.Prelude import Applicative
from hask3.Prelude import Monad
from hask3.Prelude import Traversable
from hask3.Prelude import Foldable


# Standard types
from hask3.Prelude import Maybe
from hask3.Prelude import Just
from hask3.Prelude import Nothing
from hask3.Prelude import in_maybe

from hask3.Prelude import Either
from hask3.Prelude import Left
from hask3.Prelude import Right
from hask3.Prelude import in_either

from hask3.Prelude import Ordering
from hask3.Prelude import LT
from hask3.Prelude import EQ
from hask3.Prelude import GT
