#!/usr/bin/env python
req = ['numpy','scipy',
       'tincanradar',]
#%% install
from setuptools import setup,find_packages

setup(name='harmonicradar',
      packages=find_packages(),
      version='0.1',
	  description='Detect targets in very cluttered zones by listening to non-linear junction-generated harmonic',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/harmonicradar',
      install_requires=req,
      python_requires='>=3.6',
      extras_require={'plot':['matplotlib','seaborn'],'io':['pygame']},
      dependency_links = ['https://github.com/scivision/tincanradar/tarball/master#egg=tincanradar-999'],
	  )

