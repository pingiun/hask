.. _overview:

==========
 Overview
==========

Hask3 is a pure-Python, zero-dependencies library that mimics most of the core
language tools from Haskell, including:

* Full Hindley-Milner type system (with typeclasses) that will typecheck any
  function decorated with a Hask type signature

* Easy creation of new algebraic data types and new typeclasses, with
  Haskell-like syntax

* Pattern matching with ``case`` expressions

* Automagical function currying/partial application and function composition

* Efficient, immutable, lazily evaluated `List` type with Haskell-style
  list comprehensions

* All your favorite syntax and control flow tools, including operator sections,
  monadic error handling, guards, and more

* Python port of (some of) the standard libraries from Haskell's `base`,
  including:

  * Algebraic datatypes from the Haskell `Prelude`, including `Maybe` and
    `Either`

  * Typeclasses from the Haskell `base` libraries, including `Functor`,
    `Applicative`, `Monad`, `Enum`, `Num`, and all the rest

  * Standard library functions from `base`, including all functions from
    `Prelude`, `Data.List`, `Data.Maybe`, and more.


Features
========

The List type and list comprehensions
-------------------------------------

Hask provides the `~hask.lang.lazylist.List`:class: type, a lazy and
statically-typed list, similar to Haskell's standard list type.

To create a new List, just put the elements inside ``L[`` and ``]`` brackets,
or wrap an existing iterable inside ``L[ ]``:

    >>> L[1, 2, 3]
    L[1, 2, 3]

    >>> my_list = ["a", "b", "c"]
    >>> L[my_list]
    L['a', 'b', 'c']

    >>> L[(x**2 for x in range(1, 11))]
    L[1 ... ]


To add elements to the front of a List, use ``^``, the cons operator.  To
combine two lists, use ``+``, the concatenation operator:

    >>> 1 ^ L[2, 3]
    L[1, 2, 3]

    >>> "goodnight" ^ ("sweet" ^ ("prince" ^ L[[]]))
    L["goodnight", "sweet", "prince"]

    >>> "a" ^ L[1.0, 10.3]  # doctest: +ELLIPSIS
    Traceback (...)
    ...
    TypeError: ...

    >>> L[1, 2] + L[3, 4]
    L[1, 2, 3, 4]


Lists are always evaluated lazily, and will only evaluate list elements as
needed, so you can use infinite Lists or put never-ending generators inside of
a `List`.  (Of course, you can still blow up the interpreter if you try to
evaluate the entirety of an infinite List, e.g. by trying to find the length
of the List with `len`.)

One way to create infinite lists is via list comprehensions.  As in Haskell,
there are four basic type of list comprehensions::


       >>> # list from 1 to infinity, counting by ones
       >>> L[1, ...]


       >>> # list from 1 to infinity, counting by twos
       >>> L[1, 3, ...]

       >>> # list from 1 to 20 (inclusive), counting by ones
       >>> L[1, ..., 20]


       >>> # list from 1 to 20 (inclusive), counting by fours
       >>> L[1, 5, ..., 20]


List comprehensions can be used on ints, longs, floats, one-character strings,
or any other instance of the `~hask.lang.lazylist.Enum`:class: typeclass (more
on this later).

Hask provides all of the Haskell functions for List manipulation
(`~hask.Data.List.take`:func:, `~hask.Data.List.drop`:func:,
`~hask.Data.List.takeWhile`:func:, etc.), or you can also use Python-style
indexing:

    >>> L[1, ...]
    L[1 ...]


    >>> from hask.Data.List import take
    >>> take(5, L["a", "b", ...])
    L['a', 'b', 'c', 'd', 'e']


    >>> L[1,...][5:10]
    L[6, 7, 8, 9, 10]


    >>> from hask.Data.List import map
    >>> from hask.Data.Char import chr
    >>> letters = map(chr, L[97, ...])
    >>> letters[:9]
    L['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


    >>> # DON'T do this: len(L[1, 3, ...])

Otherwise, you can use `~hask.lang.lazylist.List`:class: just like you would
use a regular Python list:

    >>> for i in L[0, ..., 3]:
    >>>     print(i)
    0
    1
    2
    3


    >>> 55 in L[1, 3, ...]
    True


Algebraic Data Types
--------------------

Hask allows you to define `algebraic datatypes`_, which are immutable objects
with a fixed number of typed, unnamed fields.

.. _algebraic datatypes: https://wiki.haskell.org/Algebraic_data_type

Here is the definition for the infamous `~hask.Data.Maybe.Maybe`:class: type:

    >>> from hask import data, d, deriving
    >>> from hask import Read, Show, Eq, Ord

    >>> Maybe, Nothing, Just =\
    ...     data.Maybe("a") == d.Nothing | d.Just("a") & \
    ...                        deriving(Read, Show, Eq, Ord)


Let's break this down a bit. The syntax for defining a new `type constructor
<https://wiki.haskell.org/Constructor#Type_constructor__>`__ is::


    >>> data.TypeName("type param", "type param 2" ... "type param n")

This defines a new algebraic datatype with type parameters.

To define `data constructors
<https://wiki.haskell.org/Constructor#Data_constructor__>`__ for this type,
use ``d``.  The name of the data constructor goes first, followed by its
fields. Multiple data constructors should be separated by ``|``. If your data
constructor has no fields, you can omit the parens. For example:

    >>> FooBar, Foo, Bar =\
    ...    data.FooBar("a", "b") == d.Foo("a", "b", str) | d.Bar


To automagically derive typeclass instances for the type, add ``&
deriving(...typeclasses...)`` after the data constructor declarations.
Currently, the only typeclasses that can be derived are
`~hask.Data.Eq.Eq`:class:, `~hask.Data.Show.Show`:class:,
`~hask.Data.Read.Read`:class:, `~hask.Data.Ord.Ord`:class:, and
`~hask.Data.Bounded.Bounded`:class.

Putting it all together, here are the definitions of
`~hask.Data.Either.Either`:class: and `~hask.Data.Ordering.Ordering`:class:\ :

    >>> from hask import Read, Show, Eq, Ord, Bounded

    >>> Either, Left, Right =\
    ...    data.Either("a", "b") == d.Left("a") | d.Right("b") & deriving(Read, Show, Eq)


    >>> Ordering, LT, EQ, GT =\
    ...     data.Ordering == d.LT | d.EQ | d.GT & deriving(Read, Show, Eq, Ord, Bounded)

You can now use the data constructors defined in a `data` statement to create
instances of these new types. If the data constructor takes no arguments, you
can use it just like a variable:

    >>> Just(10)
    Just(10)

    >>> Nothing
    Nothing

    >>> Just(Just(10))
    Just(Just(10))

    >>> Left(1)
    Left(1)

    >>> Foo(1, 2, "hello")
    Foo(1, 2, 'hello')

You can view the type of an object with `~hask.lang.syntax._t`:func:
(equivalent to `:t` in ghci).

    >>> from hask import _t, L

    >>> _t(1)
    'int'

    >>> _t(Just("soylent green"))
    '(Maybe str)'

    >>> _t(Right(("a", 1)))
    '(Either a (str, int))'

    >>> _t(Just)
    '(a -> (Maybe a))'

    >>> _t(L[1, 2, 3, 4])
    '[int]'
