==============================================
 :mod:`hask.Data.Maybe` -- The ``Data.Maybe``
==============================================

.. automodule:: hask.Data.Maybe

.. object:: hask.Data.Maybe.Maybe

   The ADT Maybe::

      data.Maybe("a") == d.Nothing | d.Just("a") & deriving(Read, Show, Eq, Ord)

.. object:: hask.Data.Maybe.Nothing

.. function:: Just(a)

.. autofunction:: in_maybe

.. autofunction:: maybe

.. autofunction:: isJust

.. autofunction:: isNothing

.. autofunction:: fromJust

.. autofunction:: listToMaybe

.. autofunction:: maybeToList

.. autofunction:: catMaybes

.. autofunction:: mapMaybe
