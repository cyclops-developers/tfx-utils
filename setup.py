#!/usr/bin/env python3
import os.path
import sys
from pkg_resources import VersionConflict, require
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)


PACKAGE_NAME = "ltfx"
PACKAGE_DESCRIPTION = "Laguro TFX utils"
AUTHOR_NAME = 'Laguro Team'
AUTHOR_EMAIL = ''

URL = "https://github.com/laguro-developers/tfx-utils"

# External dependencies
# More info https://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies
REQUIREMENTS_EXTERNAL = [
    'six>=1.10.0',
    'bumpversion>=0.5.3',
    'click>=3.3',
    'jupyter>=1.0.0',
    'pep8>=1.7.0',
    'virtualenv>=15.0.1',
    'pytest>=2.6.4',
    'pytest-cov>=1.8.1',
    'mock>=2.0.0',
    'tox>=2.2.0',
    'pytest-watch>=4.1.0',
    'jsonschema>=2.5.1',
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


def _get_version():
    """Return the project version from VERSION file."""
    with open(os.path.join(os.path.dirname(__file__), PACKAGE_NAME, 'VERSION'), 'rb') as f:
        version = f.read().decode('ascii').strip()
    return version


class Tox(TestCommand):
    """Run the test cases using TOX command."""
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        else:
            # Run all tests by default
            args = ['-c', os.path.join(os.path.dirname(__file__), 'tox.ini'), 'tests']
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name=PACKAGE_NAME,
    version=_get_version(),
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
    cmdclass={'test': Tox},
)
