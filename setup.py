#!/usr/bin/env python
from setuptools import setup

version='0.2'

setup(
    name='django-profiling-dashboard',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['profiling_dashboard'],
    package_data={
        'profiling_dashboard': ['templates/profiling_dashboard/*.html', 'static/profiling_dashboard/css/*.css']
    },

    url='https://github.com/kmike/django-profiling-dashboard',
    license = 'MIT license',
    description = """ Django profiling dashboard for debugging CPU, memory and other resources usage in live servers """,

    long_description = open('README.rst').read(),
    requires = ['django (>= 1.5)', 'yappi (>= 0.54)', 'psutil (>= 0.4.1)', 'pympler (>= 0.2.1)', 'query_exchange'],

    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)
