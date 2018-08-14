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

.. autofunction:: maybe(default, f, maybe_a)

.. autofunction:: isJust(a)

.. autofunction:: isNothing(a)

.. autofunction:: fromJust(x)

.. autofunction:: fromMaybe(default, maybe_a)

.. autofunction:: listToMaybe(ls)

.. autofunction:: maybeToList(maybe_a)

.. autofunction:: catMaybes(ms)

.. autofunction:: mapMaybe(f, ls)
