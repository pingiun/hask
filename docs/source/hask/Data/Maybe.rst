==============================================
 :mod:`hask3.Data.Maybe` -- The ``Data.Maybe``
==============================================

.. automodule:: hask3.Data.Maybe

.. object:: hask3.Data.Maybe.Maybe

   The ADT Maybe::

      data.Maybe("a") == d.Nothing | d.Just("a") & deriving(Read, Show, Eq, Ord)

.. object:: hask3.Data.Maybe.Nothing

.. function:: Just(a)

.. autofunction:: in_maybe

.. autofunction:: maybe

.. autofunction:: isJust

.. autofunction:: isNothing

.. autofunction:: fromJust

.. autofunction:: fromMaybe

.. autofunction:: listToMaybe

.. autofunction:: maybeToList

.. autofunction:: catMaybes

.. autofunction:: mapMaybe
