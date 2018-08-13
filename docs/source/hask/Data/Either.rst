================================================
 :mod:`hask3.Data.Either` -- The ``Data.Either``
================================================

.. automodule:: hask3.Data.Either

.. object:: hask3.Data.Either.Either

   The ADT Either::

      data.Either == d.Left('a') | d.Right('b') & deriving(Read, Show, Eq, Ord)

.. function:: hask3.Data.Either.Left(a)

.. function:: hask3.Data.Either.Right(b)

.. autofunction:: either

.. autofunction:: in_either

.. autofunction:: lefts

.. autofunction:: rights

.. autofunction:: isLeft

.. autofunction:: isRight

.. autofunction:: partitionEithers
