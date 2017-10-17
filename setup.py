#!/usr/bin/env python

req = ['numpy','matplotlib','scipy','seaborn']
pipreq=['pygame','tincanradar']

import pip
try:
    import conda.cli
    conda.cli.main('install',*req)
except Exception as e:
    pip.main(['install'] + req)
pip.main(['install'] + pipreq)

#%% install
from setuptools import setup #enables develop

setup(name='harmonicradar',
      packages=['harmonicradar'],
      version='0.1',
	  description='Detect targets in very cluttered zones by listening to non-linear junction-generated harmonic',
	  author='Michael Hirsch, Ph.D.',
	  url='https://github.com/scivision/harmonicradar',
      install_requires=req+pipreq,
      dependency_links = ['https://github.com/scivision/tincanradar/tarball/master#egg=tincanradar'],
	  )

