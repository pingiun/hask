==================================================================
 :mod:`hask.Python.builtins` -- Python builtins as Hask functions
==================================================================

.. automodule:: hask.Python.builtins

.. function:: callable

   ``callable ** (H/ "a" >> bool)``

.. function:: cmp

   ``cmp ** (H/ "a" >> "a" >> int)``

   .. note:: In Python 3, `cmp` is not a builtin.

.. function:: delattr

   ``delattr ** (H/ "a" >> str >> None)``

.. function:: divmod

   ``divmod ** (H/ "a" >> "b" >> ("c", "c"))``

.. function:: getattr

   ``getattr ** (H/ "a" >> str >> "b")``

.. function:: hasattr

   ``hasattr ** (H/ "a" >> str >> bool)``

.. function:: hash

   ``hash ** (H/ "a" >> int)``

.. function:: hex

   ``hex ** (H/ int >> str)``

.. function:: isinstance

   ``isinstance ** (H/ "a" >> "b" >> bool)``

.. function:: issubclass

   ``issubclass ** (H/ "a" >> "b" >> bool)``

.. function:: len

   ``len ** (H/ "a" >> int)``

.. function:: oct

   ``oct ** (H/ int >> str)``

.. function:: repr

   ``repr ** (H/ "a" >> str)``

.. function:: setattr

   ``setattr ** (H/ "a" >> str >> "b" >> None)``

.. function:: sorted

   ``sorted ** (H/ "a" >> list)``

   .. note:: Python's ``sorted`` may take an optional `key` argument.  This
             cannot be properly capture by Hask.
