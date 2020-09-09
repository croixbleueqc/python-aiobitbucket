#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='aiobitbucket',
    version='0.0.2',
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests']),
    install_requires=['aiohttp[speedups]', 'typing-engine>=2.0.0'],

    # Metadata
    author="Croix Bleue du Quebec",
    author_email="devops@qc.croixbleue.ca",
    license="LGPL-3.0-or-later",
    description="Bitbucket Asyncio",
    long_description=open('README.rst').read(),
    url="https://github.com/croixbleueqc/python-aiobitbucket",
    keywords=["bitbucket", "asyncio", "git"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite="tests"
)
