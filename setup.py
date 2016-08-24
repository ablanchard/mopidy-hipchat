# future imports
from __future__ import unicode_literals

# stdlib imports
import re
from setuptools import find_packages
from setuptools import setup


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


setup(
    name='Mopidy-Hipchat',
    version=get_version('mopidy_hipchat/__init__.py'),
    url='https://github.com/ablanchard/mopidy-hipchat',
    license='Apache License, Version 2.0',
    author='Alexandre Blanchard',
    author_email='alexandre.blanchard@laposte.net',
    description='Mopidy extension that integrates with hipchat',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.18',
        'Pykka >= 1.1',
        'requests',
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock >= 1.0',
    ],
    entry_points={
        'mopidy.ext': [
            'hipchat= mopidy_hipchat:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
