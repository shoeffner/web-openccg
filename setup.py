# -*- coding: utf-8 -*-
import re
from pathlib import Path

from setuptools import setup, find_packages


REPOSITORY = 'https://github.com/shoeffner/web-openccg'
README = re.sub(r' _(.+): ([^(http)].+)',
                r' _\1: {}/blob/master/\2'.format(REPOSITORY),
                Path('README.md').read_text())

setup(
    name='WebOpenCCG',
    version='1.0.0',

    description="A thin web wrapper around OpenCCG's wccg.",
    long_description=README,
    author='Sebastian Höffner',
    author_email='shoeffner@tzi.de',
    url='https://litmus.informatik.uni-bremen.de/openccg',
    project_urls={
        'Bug Tracker': f'{REPOSITORY}/issues',
        'Documentation': f'{REPOSITORY}/tree/master/README.md',
        'Source Code': f'{REPOSITORY}/tree/master',
    },

    install_requires=Path('requirements.txt').read_text(),

    packages=find_packages(),
    package_data={
        'webopenccg': ['static/*', 'templates/*']
    },

    entry_points={
        'console_scripts': [
            'webopenccg = webopenccg.webapp:app.run'
        ]
    },

    test_suite="tests",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    license='MIT'
)
