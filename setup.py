#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md', 'rt') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', 'rt') as history_file:
    history = history_file.read()


setup(
    author="EPIC",
    author_email='software@earthscope.org',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved ::  GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    description="Provide access to the NRL v2 web service",
    entry_points={
        'console_scripts': [],
    },
    install_requires=['configobj', 'requests', 'types-requests', 'pyyaml'],
    setup_requires=[],
    extras_require={
        'dev': [
            'flake8',
            'tox',
            'mypy',
            'coverage',
            'genbadge',
        ]
    },
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nrl',
    name='nrl',
    packages=find_packages(),
    url='https://gitlab.com/earthscope/public/epic/nrl',
    version='2025.1.0.0',
    zip_safe=False,
)
