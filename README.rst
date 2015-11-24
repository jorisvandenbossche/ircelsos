ircelsos
========

Downloading air quality data from the SOS of IRCEL - CELINE, the Belgian
Interregional Environment Agency (http://www.irceline.be).

This packages provides both a command line interface, as a python module
that downloads the data as pandas DataFrames.

Installation
------------

*ircelsos* is a Python package. If you have Python installed, *ircelsos* can
easily be installed with pip::

    pip install ircelsos

This will automatically install the dependency `OWSlib <https://github.com/geopython/OWSLib>`_.
ircelsos supports python 2.7 and 3.3+. For python 3, OWSlib 9.0 or higher is needed.

Command line usage
------------------

Installing ircelsos will register a ``ircelsos`` command. This can be used from
the command line to download data and to retrieve info about the stations and
pollutants available in the SOS, using the two subcommands ``query`` and
``info``.

Downloading data
^^^^^^^^^^^^^^^^

To download data, you can use the ``ircelsos query`` command. Eg::

    ircelsos query o3 -s BETN060 -p 2015-03-27T00:00:00 2015-03-27T10:00:00

This will save a csv file in the current directory.

Specifying no stations or no period, will download the data for that pollutant
for all stations for the full available period.

For more details on the arguments, call ``ircelsos query -h``.

Retrieving info
^^^^^^^^^^^^^^^

The ``ircelsos info`` command can be used to inspect available stations and
pollutants. The following will give a list of all pollutants::

    $ ircelsos info --pollutant
    SOS of IRCEL - CELINE

    id                     | short | name                         | stations
    -----------------------+-------+------------------------------+---------
    16111 - Black Carbon   | bc    | Black Carbon                 | 25
    42101 - CO             | co    | Carbon Monoxide              | 24
    ...

To get the detailed information about one pollutant, you can specify this after
``--pollutant``. Eg::

    $ ircelsos info --pollutant bc
    SOS of IRCEL - CELINE

          id = 16111 - Black Carbon
       short = bc
        name = Black Carbon
    stations = 25

    This pollutant is measured at the following stations:

    name   | EU_code | location             | region   | type
    -------+---------+----------------------+----------+-----------
    40AB01 | BELAB01 | ANTWERPEN            | suburban | Background
    40AL01 | BELAL01 | LINKEROEVER          | suburban | Background
    ...

The same can be done to get information about the stations:
``ircelsos info --station`` for a list of all stations and
``ircelsos info --station STATION_CODE`` for the detailed information of one
station.

Alternatively to the command line, you can also run the same script from
the ``ircelsos`` directory::

    python -m ircelsos query ...


Interactive usage (pandas)
--------------------------

To use the packages in an interactive python session, you need an extra
dependency: `pandas <http://pandas.pydata.org/>`_.

To download data as a pandas DataFrame, you can use the ``query`` function:

.. code-block:: python

    >>> import ircelsos
    >>> df = ircelsos.query('no2', station=['42R801', '42R802'], utc_start='2015-11-15')
    >>> df.head()
                                   42R801  42R802
    time
    2015-11-24T01:00:00.000+01:00    27.0    28.5
    2015-11-24T02:00:00.000+01:00    17.5    19.5
    2015-11-24T03:00:00.000+01:00    16.0    16.5
    2015-11-24T04:00:00.000+01:00    17.0    17.5
    2015-11-24T05:00:00.000+01:00    24.0    24.5


----

* Author: Joris Van den Bossche
* License: BSD 2-clause
