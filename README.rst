ircelsos
========

Downloading air quality data from the SOS of IRCEL - CELINE.

Installing (running from this directory)::

    python setup.py install

This will automatically install the dependency `OWSlib <https://github.com/geopython/OWSLib>`_.
ircesos supports python 2.7 and 3.3+. For python 3, OWSlib 9.0 or higher is needed.

Installing ircelsos will register a ``ircelsos`` command. This can be used from
the command line to download data::

    ircelsos o3 -s BETN060 -p 2015-03-27T00:00:00 2015-03-27T10:00:00

For more details on the arguments, call ``ircelsos -h``.

Alternatively, you can also run the same script from the ``ircelsos``
directory::

    python -m ircelsos ...
