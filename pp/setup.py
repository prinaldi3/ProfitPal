import setuptools
from setuptools import setup
import glob
import os

from src.pp import __version__, _program

setup(name='pp',
      version=__version__,
      packages=setuptools.find_packages(where='src'),
      package_dir={'': 'src'},
      description="A simple CLI application for logging, summarizing, and extrapolating financial data.",
      url='',
      author='Phil Rinaldi',
      author_email='pg3rinaldi@gmail.com',
      license='MIT',
      entry_points="""
      [console_scripts]
      {program} = pp.cli:main
      """.format(program = _program),
      keywords=[],
      tests_require=[],
      zip_safe=False)