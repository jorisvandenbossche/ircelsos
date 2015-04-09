ircelsos
========

Downloading air quality data from the SOS of IRCEL - CELINE

Installing::

    python setup.py install

This will register a ``ircelsos`` command. This can be used to download data::

    ircelsos o3 -s BETN060 -p 2015-03-27T00:00:00 2015-03-27T10:00:00

For more details on the arguments, call ``ircelsos -h``.
