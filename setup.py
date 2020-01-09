#!/usr/bin/env python3
import os.path
import sys
from pkg_resources import VersionConflict, require
from setuptools import setup, find_packages

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

version = '0.0.2'

PACKAGE_NAME = "ltfx"
PACKAGE_DESCRIPTION = "Laguro TFX utils"
AUTHOR_NAME = 'Laguro Team'
AUTHOR_EMAIL = ''

URL = "https://github.com/laguro-developers/tfx-utils"

# External dependencies
# More info https://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies
REQUIREMENTS_EXTERNAL = [
    'apache-beam[gcp]<2.17,>=2.16',
    'tfx>=0.15.0',
    'tensorflow<2.1.0,>=2.0.0',
    'tensorflow-data-validation>=0.15.0',
    'tensorflow-estimator<2.1.0,>=2.0.1',
    'tensorflow-metadata<0.21.0,>=0.15.2',
    'tensorflow-model-analysis>=0.15.4',
    'tensorflow-serving-api>=2.0.0',
    'tensorflow-transform>=0.15.0',
    'scipy<1.2,>=1.1.0',
    'tensorboard<2.1.0,>=2.0.0',
    'prompt-toolkit<2.1.0,>=2.0.10'
]

# Test dependencies
REQUIREMENTS_TESTS = [
]

# This is normally an empty list
DEPENDENCY_LINKS_EXTERNAL = []

SCRIPTS = ['bin/ltfx']


DEVELOPMENT_STATUS = {
    'planning': '1 - Planning',
    'pre-alpha': '2 - Pre-Alpha',
    'alpha': 'Alpha',
    'beta': '4 - Beta',
    'stable': '5 - Production/Stable',
    'mature': '6 - Mature',
    'inactive': '7 - Inactive',
}

STATUS = 'alpha'

CLASSIFIERS = [
        'Development Status :: {}'.format(DEVELOPMENT_STATUS[STATUS]),
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]



setup(
    name=PACKAGE_NAME,
    version=version,
    url=URL,
    description=PACKAGE_DESCRIPTION,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author=AUTHOR_NAME,
    maintainer=AUTHOR_NAME,
    maintainer_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS_EXTERNAL,
    tests_require=REQUIREMENTS_TESTS,
    dependency_links=DEPENDENCY_LINKS_EXTERNAL,
    scripts=SCRIPTS,
)
