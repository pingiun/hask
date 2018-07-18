==========================================
 :mod:`hask.Data.Ord` -- The ``Data.Ord``
==========================================

.. automodule:: hask.Data.Ord

.. object:: Ordering

   The ADT Ordering::

     data Ordering = LT | EQ | GT deriving(Show, Eq, Ord, Bounded)

.. object:: LT
.. object:: EQ
.. object:: GT

.. autofunction:: max

.. autofunction:: min

.. autofunction:: compare

.. autofunction:: comparing
