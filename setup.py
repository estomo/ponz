#!usr/bin/env python
#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
from ponz import __author__, __version__, __license__
 
setup(name="ponz",
    version=__version__,
    description="mecab wrapper",
    license= __license__,
    author= __author__,
    url="https://github.com/estomo/ponz.git",
    packages=find_packages(),
    install_requires = [],
    )
