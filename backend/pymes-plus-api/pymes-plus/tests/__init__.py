# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
# TEST module
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

import unittest
from .api_v1 import api_tests_accounting, api_tests_referential, api_tests_auth, api_tests_security, api_tests_payroll
from .models import purchase_test, sales, inventory

api_tests = unittest.TestSuite([api_tests_referential,
                                api_tests_auth,
                                api_tests_security,
                                api_tests_accounting,
                                api_tests_payroll])
# all_tests = unittest.TestSuite([api_tests, purchase])
all_tests = unittest.TestSuite([purchase_test])