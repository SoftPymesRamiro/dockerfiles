# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
# TEST Purchase module
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

import unittest
from .purchase.purchase_functions_test import PurchaseFunctionsTest
purchase_functions_test = unittest.TestLoader().loadTestsFromTestCase(PurchaseFunctionsTest)
purchase_test = unittest.TestSuite([purchase_functions_test])