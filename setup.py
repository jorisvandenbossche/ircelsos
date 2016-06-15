"""A setuptools based setup module.

"""

import os
from io import open
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ircelsos',
    version='0.2.0',
    description='Downloading air quality data from the SOS of IRCEL - CELINE',
    long_description=long_description,
    url='https://github.com/jorisvandenbossche/ircelsos',
    author='Joris Van den Bossche',
    author_email='jorisvandenbossche@gmail.com',
    license='BSD',
    packages=['ircelsos'],
    install_requires=['owslib==0.9.0', 'six'],
    entry_points={
        'console_scripts': [
            'ircelsos=ircelsos.main:main',
        ],
    },
)
