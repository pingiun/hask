======
 Hask
======

.. image:: https://travis-ci.org/mvaled/hask.svg


Hask is a pure-Python, zero-dependencies library that mimics most of the core
language tools from Haskell, including:

* Full Hindley-Milner type system (with typeclasses) that will typecheck any
  function decorated with a Hask type signature

* Easy creation of new algebraic data types and new typeclasses, with
  Haskell-like syntax

* Pattern matching with `case` expressions

* Automagical function currying/partial application and function composition

* Efficient, immutable, lazily evaluated `List` type with Haskell-style list
  comprehensions

* All your favorite syntax and control flow tools, including operator
  sections, monadic error handling, guards, and more

* Python port of (some of) the standard libraries from Haskell's `base`,
  including:

  * Algebraic datatypes from the Haskell `Prelude`, including `Maybe` and
    `Either`

  * Typeclasses from the Haskell `base` libraries, including `Functor`,
    `Applicative`, `Monad`, `Enum`, `Num`, and all the rest

  * Standard library functions from `base`, including all functions from
    `Prelude`, `Data.List`, `Data.Maybe`, and more


Features not yet implemented, but coming soon:

* Better support for polymorphic return values/type defaulting

* Better support for lazy evaluation (beyond just the `List` type and pattern
  matching)

* More of the Haskell standard library (`Control.*` libraries, QuickCheck, and
  more)

* Monadic, lazy I/O

.. warning:: Note that all of this is still very much pre-alpha, and some
             things may be buggy!


Credits
=======

This is a fork of `hask <https://github.com/billmurphy/hask_>`__ modified to
run in Python 3.4+.

See the `LICENSE file <https://github.com/mvaled/hask/blob/master/LICENSE_>`__
keeps the original author and rights.

Changes are copyright `Merchise Autrement [~º/~] and Contributors`, but with
the same
