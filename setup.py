"""A setuptools based setup module.

"""

from setuptools import setup

setup(
    name='ircelsos',
    version='0.1.dev',
    description='Downloading air quality data from the SOS of IRCEL - CELINE',
    #long_description=long_description,
    url='https://github.ugent.be/jorvdnbo/ircelsos',
    author='Joris Van den Bossche',
    author_email='jorisvandenbossche@gmail.com',
    #license='MIT',
    packages=['ircelsos'],
    install_requires=['owslib'],
    entry_points={
        'console_scripts': [
            'ircelsos=ircelsos:main',
        ],
    },
)
