==========================================
 :mod:`hask3.lang.lazylist` -- A lazy List
==========================================

.. automodule:: hask3.lang.lazylist
   :members: Enum, fromEnum, succ, pred, enumFromThen, enumFrom,
             enumFromThenTo, enumFromTo


.. object:: L

   ``L`` is the syntactic construct for Haskell-style list comprehensions and
   lazy list creation. To create a new List, just wrap an interable in
   ``L[ ]``.

   List comprehensions can be used with any instance of `Enum`:class:,
   including the built-in types ``int``, ``long`` (in Python 2), ``float``,
   and ``str`` (a char).

   There are four basic list comprehension patterns:

       >>> from hask3 import L
       >>> # list from 1 to infinity, counting by ones
       >>> L[1, ...]
       L[1, ...]


       >>> # list from 1 to infinity, counting by twos
       >>> L[1, 3, ...]
       L[1, 3, ...]

       >>> # list from 1 to 20 (inclusive), counting by ones
       >>> L[1, ..., 20]
       L[1, ..., 20]


       >>> # list from 1 to 20 (inclusive), counting by fours
       >>> L[1, 5, ..., 20]
       L[1, 5, ..., 20]


.. autoclass:: List
