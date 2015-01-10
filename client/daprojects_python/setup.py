from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='daprojects_python',
    version='0.0.1',
    description='Python client library for Dungeons&Projects',
    long_description=long_description,
    url='https://github.com/PIWEEK/dungeons-and-projects',
    author='Andrés Moya Velázquez',
    author_email='andres.moya@kaleidos.net',
    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='development software quality technical debt',

    packages=find_packages(exclude=[]),

    install_requires=['requests>=2.5'],

    extras_require = {},

    package_data={},

    data_files=[],

    entry_points={},
)
