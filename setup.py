# lool #

import setuptools


# VERSION
__version__ = '0.0'
# with open('src/lofile/core/__init__.py') as file:
    # for line in file.readlines():
        # if '__version__' in line:
            # __version__: str
            # exec(line)


# SETUP
setuptools.setup(

    name = 'loolclitools',
    version = __version__,
    author = 'lool',
    author_email = 'txhx@gmail.com',
    description = 'This moudle brings some tools for building CLIs.',
    url = 'https://github.com/user3838',

    package_dir = {'': 'src'},
    packages = setuptools.find_packages('src'),
    python_requires = '>= 3.8',
)
