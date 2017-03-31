#!/usr/bin/env python
from setuptools import setup #enables develop

req = ['numpy','matplotlib','scipy','seaborn','pygame',
       'tincanradar']

#%% install
setup(name='harmonicradar',
      version='0.1',
	  description='Detect targets in very cluttered zones by listening to non-linear junction-generated harmonic',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/harmonicradar',
      install_requires=req,
      dependency_links = ['https://github.com/scivision/tincanradar/tarball/master#egg=tincanradar'],
      packages=['harmonicradar'],
	  )

