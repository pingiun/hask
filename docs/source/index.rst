.. Hask documentation master file, created by
   sphinx-quickstart on Tue Jul 17 09:19:33 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===================================
 Welcome to Hask3's documentation!
===================================

This is a fork for the original project `hask`_.  We're naming it ``hask3``
because we're intending this project to be used exclusively in Python 3.4+.

Most of the code of this project is still from the original authors.

.. warning:: Python 2.7 support is being dropped.

   We officially support only Python 3.4+ (see the our `Travis CI builds`_ to
   get the full list of supported versions), even though the original project
   only supports Python 2.7.

   We keep the code running in Python 2.7 as the baseline, but Python 2.7 is
   not supported and it may become broken at any time.

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Contents:

   overview
   hask/index.rst
   history.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _hask: https://github.com/billpmurphy/hask
.. _Travis CI builds: https://travis-ci.org/mvaled/hask/
