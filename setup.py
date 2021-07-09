# lool #

import setuptools


# VERSION
with open('src/loolclitools/__init__.py') as file:
    for line in file.readlines():
        if '__version__' in line:
            __version__: str
            exec(line.strip())
            break


# SETUP
setuptools.setup(

    name = 'loolclitools',
    version = __version__,
    author = 'lool',
    author_email = 'txhx38@gmail.com',
    description = 'This moudle brings some tools for building CLIs.',
    url = 'https://github.com/txhx38/loolclitools',

    package_dir = {'': 'src'},
    packages = setuptools.find_packages('src'),
    python_requires = '>= 3.8',
)
