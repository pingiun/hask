============================================
 :mod:`hask.Data.Char` -- The ``Data.Char``
============================================

.. automodule:: hask.Data.Char

.. autofunction:: isControl

.. autofunction:: isSpace

.. autofunction:: isLower

.. autofunction:: isUpper

.. autofunction:: isAlpha

.. autofunction:: isAlphaNum

.. autofunction:: isPrint

.. autofunction:: isDigit

.. autofunction:: isOctDigit

.. autofunction:: isHexDigit

.. autofunction:: isLetter

.. autofunction:: isMark

.. autofunction:: isNumber

.. autofunction:: isPunctuation

.. autofunction:: isSymbol

.. autofunction:: isSeparator

.. autofunction:: isAscii

.. autofunction:: isLatin1

.. autofunction:: isAsciiUpper

.. autofunction:: isAsciiLower

.. autofunction:: toLower

.. autofunction:: toUpper

.. autofunction:: toTitle

.. autofunction:: digitToInt

.. autofunction:: intToDigit


.. function:: chr(x)

   The builtin `chr` converted to a `~hask.lang.type_system.TypedFunc`:class:.
   Defined as ``chr ** (H/ int >> str)``


.. function:: ord(x)

   The builtin `ord` converted to a `~hask.lang.type_system.TypedFunc`:class:.
   Defined as ``ord ** (H/ int >> str)``
