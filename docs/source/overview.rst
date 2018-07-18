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

    >>> from hask import L
    >>> L[1, 2, 3]
    L[1, 2, 3]

    >>> my_list = ["a", "b", "c"]
    >>> L[my_list]
    L['a', 'b', 'c']

    >>> L[(x**2 for x in range(1, 11))]
    L[1 ...]


To add elements to the front of a List, use ``^``, the cons operator.  To
combine two lists, use ``+``, the concatenation operator:

    >>> 1 ^ L[2, 3]
    L[1, 2, 3]

    >>> "goodnight" ^ ("sweet" ^ ("prince" ^ L[[]]))
    L['goodnight', 'sweet', 'prince']

    >>> "a" ^ L[1.0, 10.3]  # doctests: +ELLIPSIS
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
       >>> L[1 ...]


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

    >>> from hask import L
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

    >>> from hask import L
    >>> for i in L[0, ..., 3]:
    ...     print(i)
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
`~hask.lang.typeclasses.Eq`:class:, `~hask.lang.typeclasses.Show`:class:,
`~hask.lang.typeclasses.Read`:class:, `~hask.lang.typeclasses.Ord`:class:, and
`~hask.lang.typeclasses.Bounded`:class:.

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


The type system and typed functions
-----------------------------------

So what's up with those types? Hask operates its own shadow `Hindley-Milner
type system`_ on top of Python's type system; `~hask.lang.syntax._t`:func:
shows the Hask type of a particular object.

In Hask, typed functions take the form of
`~hask.lang.type_system.TypedFunc`:func: objects, which are typed wrappers
around Python functions. There are two ways to create TypedFunc objects:

- Use the `sig` decorator to decorate the function with the type signature::

    @sig(H/ "a" >> "b" >> "a")
    def const(x, y):
        return x

- Use the ``**`` operator (similar to ``::`` in Haskell) to provide the type.

  Useful for turning functions or lambdas into TypedFunc objects in the REPL,
  or wrapping already-defined Python functions::

    def const(x, y):
        return x

    const = const ** (H/ "a" >> "b" >> "a")

TypedFunc objects have several special properties.  First, they are type
checked -- when arguments are supplied, the type inference engine will check
whether their types match the type signature, and raise a TypeError if there
is a discrepancy.

    >>> f = (lambda x, y: x + y) ** (H/ int >> int >> int)

    >>> f(2, 3)
    5

    >>> f(9, 1.0)  # doctest: +ELLIPSIS
    Traceback (...)
       ...
    TypeError: ...



Second, TypedFunc objects can be partially applied:

   >>> g = (lambda a, b, c: a / (b + c)) ** (H/ int >> int >> int >> int)

   >>> g(10, 2, 3)
   2

   >>> part_g = g(12)
   >>> part_g(2, 2)
   3

   >>> g(20, 1)(4)
   4


TypedFunc objects also have two special infix operators, the ``*`` and ``%``
operators. ``*`` is the compose operator (equivalent to ``.`` in Haskell), so
``f * g`` is equivalent to ``lambda x: f(g(x))``. ``%`` is just the apply
operator, which applies a TypedFunc to one argument (equivalent to ``$`` in
Haskell).  The convinience of this notation (when combined with partial
application) cannot be overstated -- you can get rid of a ton of nested
parenthesis this way:


   >>> from hask.Prelude import flip
   >>> h = (lambda x, y: x / y) ** (H/ float >> float >> float)
   >>> h(3.0) * h(6.0) * flip(h, 2.0) % 36.0
   9.0


The compose operation is also typed-checked, which makes it appealing to write
programs in `pointfree style`_, i.e. chaining together lots of functions with
composition and relying on the type system to catch programming errors.

As you would expect, data constructors are also just TypedFunc objects:

   >>> Just * Just * Just * Just % 77
   Just(Just(Just(Just(77))))


The type signature syntax is very simple, and consists of a few basic
primitives that can be combined to build any type signature:

- Type literal for Python builtin type or user-defined class:

  ``int``, ``float``, ``set``, ``list``

- Type variable:

  ``"a"``, ``"b"``, ``"zz"``

- ``List`` of some type:

  ``[int]``, ``["a"]``, ``[["a"]]``

- Tuple type:

  ``(int, int)``, ``("a", "b", "c")``, ``(int, ("a", "b"))``

- ADT with type parameters:

  ``t(Maybe, "a")``, ``t(Either, "a", str)``

- Unit type (``None``):

  ``None``

- Untyped Python function:

  ``func``

- Typeclass constraint:

  ``H[(Eq, "a"), (Show, "b")]/``, ``H[(Functor, "f"), (Show, "f")]/``

Some examples::

  # add two ints together
  @sig(H/ int >> int >> int)
  def add(x, y):
      return x + y


  # reverse order of arguments to a function
  @sig(H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
  def flip(f, b, a):
      return f(a, b)


  # map a Python (untyped) function over a Python (untyped) set
  @sig(H/ func >> set >> set)
  def set_map(fn, lst):
      return set((fn(x) for x in lst))


  # map a typed function over a List
  @sig(H/ (H/ "a" >> "b") >> ["a"] >> ["b"])
  def map(f, xs):
      return L[(f(x) for x in xs)]


  # type signature with an Eq constraint
  @sig(H[(Eq, "a")]/ "a" >> ["a"] >> bool)
  def not_in(y, xs):
      return not any((x == y for x in xs))


  # type signature with a type constructor (Maybe) that has type arguments
  @sig(H/ int >> int >> t(Maybe, int))
  def safe_div(x, y):
      return Nothing if y == 0 else Just(x/y)


  # type signature for a function that returns nothing
  @sig(H/ int >> None)
  def launch_missiles(num_missiles):
      print("Launching {0} missiles! Bombs away!" % num_missiles)


It is also possible to create type synonyms using
`~hask.lang.syntax.t`:func:. For example, check out the definition of
:obj:`~hask.Data.Num.Rational`:

::

    Ratio, R =\
            data.Ratio("a") == d.R("a", "a") & deriving(Eq)


    Rational = t(Ratio, int)


    @sig(H/ Rational >> Rational >> Rational)
    def addRational(rat1, rat2):
        ...

.. _Hindley-Milner type system: https://en.wikipedia.org/wiki/Hindley%E2%80%93Milner_type_system
.. _pointfree style: https://wiki.haskell.org/Pointfree


Pattern matching
----------------

Pattern matching is a more powerful control flow tool than the ``if``
statement, and can be used to deconstruct iterables and ADTs and bind values
to local variables.

Pattern matching expressions follow this syntax::

    ~(caseof(value_to_match)
        | m(pattern_1) >> return_value_1
        | m(pattern_2) >> return_value_2
        | m(pattern_3) >> return_value_3)

Here is a function that uses pattern matching to compute the fibonacci
sequence.  Note that within a pattern match expression, ``m.*`` is used to
bind variables, and ``p.*`` is used to access them:

  >>> def fib(x):
  ...     return ~(caseof(x)
  ...                 | m(0)   >> 1
  ...                 | m(1)   >> 1
  ...                 | m(m.n) >> fib(p.n - 1) + fib(p.n - 2))

  >>> fib(1)
  1

  >>> fib(6)
  13


As the above example shows, you can combine pattern matching and recursive
functions without a hitch.

You can also deconstruct an iterable using ``^`` (the cons operator). The
variable before the ``^`` is bound to the first element of the iterable, and
the variable after the ``^`` is bound to the rest of the iterable. Here is a
function that adds the first two elements of any iterable, returning
``Nothing`` if there are less than two elements:

  >>> from hask import sig, t, caseof, m, p
  >>> from hask import Num, Maybe, Just, Nothing

  >>> @sig(H[(Num, "a")]/ ["a"] >> t(Maybe, "a"))
  ... def add_first_two(xs):
  ...     return ~(caseof(xs)
  ...                 | m(m.x ^ (m.y ^ m.z)) >> Just(p.x + p.y)
  ...                 | m(m.x)               >> Nothing)

  >>> add_first_two(L[1, 2, 3, 4, 5])
  Just(3)

  >>> add_first_two(L[9.0])
  Nothing

Pattern matching is also very useful for deconstructing ADTs and assigning
their fields to temporary variables.

    >>> from hask import caseof, m, p
    >>> from hask import Num, Maybe, Just, Nothing

    >>> def default_to_zero(x):
    ...     return ~(caseof(x)
    ...                 | m(Just(m.x)) >> p.x
    ...                 | m(Nothing)   >> 0)

    >>> default_to_zero(Just(27))
    27


    >>> default_to_zero(Nothing)
    0


If you find pattern matching on ADTs too cumbersome, you can also use numeric
indexing on ADT fields.  An `IndexError` will be thrown if you mess something
up.

   >>> Just(20.0)[0]
   20.0

   >>> Left("words words words words")[0]
   'words words words words'

   >>> Nothing[0]  # IndexError
