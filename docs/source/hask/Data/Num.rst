==========================================
 :mod:`hask.Data.Num` -- The ``Data.Num``
==========================================

.. automodule:: hask.Data.Num

.. autoclass:: Num

.. autoclass:: Fractional

.. autoclass:: Floating

.. autoclass:: Real

.. autoclass:: Integral

.. autoclass:: RealFrac

.. autoclass:: RealFloat

.. object:: Ratio

   The ADT Ratio::

     Ratio, R =\
        data.Ratio("a") == d.R("a", "a") & deriving(Eq)

.. object:: Rational

   A `Ratio`:obj: over `int`:class:.  Defined as ``t(Ratio, int)``.

.. function:: R(a, a)

   The constructor of a Ratio.

.. autofunction:: negate

.. autofunction:: signum

.. autofunction:: abs

.. autofunction:: recip

.. autofunction:: exp

.. autofunction:: sqrt

.. autofunction:: log

.. autofunction:: pow

.. autofunction:: logBase

.. autofunction:: sin

.. autofunction:: cos

.. autofunction:: tan

.. autofunction:: asin

.. autofunction:: atan

.. autofunction:: acos

.. autofunction:: sinh

.. autofunction:: tanh

.. autofunction:: cosh

.. autofunction:: asinh

.. autofunction:: atanh

.. autofunction:: acosh

.. autofunction:: toRational

.. autofunction:: toRatio

.. autofunction:: properFraction

.. autofunction:: truncate

.. autofunction:: round

.. autofunction:: ceiling

.. autofunction:: floor

.. autofunction:: isNaN

.. autofunction:: isInfinite

.. autofunction:: isNegativeZero

.. autofunction:: atan2
