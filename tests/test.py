#!/usr/bin/env python
from numpy.testing import run_module_suite
#
from harmonicradar import noisepower

def test_fwdmodel():
    assert_allclose(noisepower(8,25e3),-121.995788617)
    assert_allclose(friis(1e3,144e6), 75.6150330638)

if __name__ == '__main__':
    run_module_suite()
