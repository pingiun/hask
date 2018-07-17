================================================
 :mod:`hask.Data.Either` -- The ``Data.Either``
================================================

.. automodule:: hask.Data.Either

.. object:: Either

   The ADT Either::

      data.Either == d.Left('a') | d.Right('b') & deriving(Read, Show, Eq, Ord)

.. object:: Left
.. object:: Right

.. autofunction:: either

.. autofunction:: in_either

.. autofunction:: lefts

.. autofunction:: rights

.. autofunction:: isLeft

.. autofunction:: isRight

.. autofunction:: partitionEithers
