ircelsos
========

Downloading air quality data from the SOS of IRCEL - CELINE

Installing (running from this directory)::

    python setup.py install

.. note::

    Note on Python 3: the dependency
    `OWSlib <https://github.com/geopython/OWSLib>`_ is not yet python 3
    compatible, however the development version has been ported. To install the
    development version::

        pip install git+https://github.com/geopython/OWSLib.git

    This has to be installed before installing ircelsos.

Installing ircelsos will register a ``ircelsos`` command. This can be used from
the command line to download data::

    ircelsos o3 -s BETN060 -p 2015-03-27T00:00:00 2015-03-27T10:00:00

For more details on the arguments, call ``ircelsos -h``.

Alternatively, you can also run the same script from the ``ircelsos``
directory::

    python -m ircelsos ...
