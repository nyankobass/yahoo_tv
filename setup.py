# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


try:
    with open('README.rst') as f:
        readme = f.read()
except IOError:
    readme = ''
try:
    with open('LICENSE') as f:
        license = f.read()
except IOError:
    license = ''


setup(
    name='yahoo_tv',
    version='1.0.0',
    description='Getting TV schedule for Yahoo TV',
    long_description=readme,
    author='nyankobass',
    author_email='',
    url='https://github.com/nyankobass/yahoo_tv.git',
    license=license,
    install_requires=_requires_from_file('requirements.txt'),
    packages=find_packages(exclude=('tests', 'docs'))
)
