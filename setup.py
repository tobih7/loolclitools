# lool #

import sys, os
from setuptools import setup, find_packages

sys.path.insert(0, os.getcwd())
from src.loolclitools import __doc__, __version__


# SETUP
setup(
    name='loolclitools',
    version=__version__,
    author='lool',
    author_email='txhx38@gmail.com',
    description=__doc__,
    url='https://github.com/txhx38/loolclitools',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires='>= 3.8',
)
