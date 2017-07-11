# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# TEST Auth module
#
# To execute this test run python auth_test.py on 
# the Terminal. 
# Reading the defined test you'll see that we should
# expect
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

import coverage
COV = coverage.coverage(branch=True, include='app/*', debug="data")
COV.start()

import unittest
from tests import all_tests
envresult = unittest.TextTestRunner(verbosity=0, buffer=False, descriptions=False).run(all_tests)

COV.stop()
COV.report(show_missing=1, omit=['*test*', '*__init__*'])
COV.html_report(directory='../docs/covhtml', omit=['*test*', '*__init__*'])

