================================================
 :mod:`hask.Data.Either` -- The ``Data.Either``
================================================

.. automodule:: hask.Data.Either

.. object:: hask.Data.Either.Either

   The ADT Either::

      data.Either == d.Left('a') | d.Right('b') & deriving(Read, Show, Eq, Ord)

.. function:: hask.Data.Either.Left(a)

.. function:: hask.Data.Either.Right(b)

.. autofunction:: either

.. autofunction:: in_either

.. autofunction:: lefts

.. autofunction:: rights

.. autofunction:: isLeft

.. autofunction:: isRight

.. autofunction:: partitionEithers
