#!/usr/bin/env python3
from setuptools import setup #enables develop
import subprocess


with open('README.rst','r') as f:
	  long_description = f.read()

#%% install
setup(name='harmonicradar',
      version='0.1',
	  description='Detect targets in very cluttered zones by listening to non-linear junction-generated harmonic',
	  long_description=long_description,
	  author='Michael Hirsch',
	  url='https://github.com/scivision/harmonicradar',
   install_requires=['tincanradar'],
     dependency_links = ['https://github.com/scienceopen/tincanradar/tarball/master#egg=tincanradar'],
      packages=['harmonicradar'],
	  )

try:
    subprocess.run(['conda','install','--yes','--quiet','--file','requirements.txt']) #don't use os.environ
except Exception as e:
    print('you will need to install packages in requirements.txt  {}'.format(e))
