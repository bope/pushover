# coding: utf-8
from setuptools import setup


setup(
    name='pushover',
    packages=['pushover'],
    description='',
    long_description='',
    entry_points={
        'console_scripts': ['pushover = pushover.cli:main'],
    },
    install_requires=['pyyaml', 'requests'],
)
