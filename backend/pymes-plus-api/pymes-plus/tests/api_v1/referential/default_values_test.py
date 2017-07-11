#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]


from flask import Flask
import unittest
import json
import copy
import time
import logging


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for DefaultVaslues API class
"""
class DefaultValuesTest(unittest.TestCase):
    """
    This Class is a Test Case for Default values API class
    """

    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
            password='Admin*2') # valid data by access to SoftPymes plus

        app = Flask(__name__) # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self) # test client
        self.test_client.testing = False # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                    data=json.dumps(self.userdata),
                        content_type='application/json')
        # User token
        self.token = json.loads( self.response.data.decode("utf-8") )['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}


    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/default_values# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/default_values'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/default_values# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/default_values'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/default_values# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/default_values'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/default_values# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/default_values'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_default_values(self):
        """
        This function test get all default
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

    def test_get_default_value(self):
        """
        This function test get a default value according a identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/1")
        response.json = json.loads(response.data.decode("utf-8") )

        self.assertTrue("printDescription" in response.json)
        self.assertTrue("sourceWarehouse" in response.json)
        self.assertTrue("updateDate" in response.json)
        self.assertTrue("sectionId" in response.json)
        self.assertTrue("destinyWarehouse" in response.json)
        self.assertTrue("manualUnitValue" in response.json)

        self.assertTrue("purchaseCostCenterId" in response.json)
        self.assertTrue("purchaseDivisionId" in response.json)
        self.assertTrue("purchaseSectionId" in response.json)
        self.assertTrue("purchaseDependencyId" in response.json)

        self.assertTrue("treasuryCostCenterId" in response.json)
        self.assertTrue("treasuryDivisionId" in response.json)
        self.assertTrue("treasurySectionId" in response.json)
        self.assertTrue("treasuryDependencyId" in response.json)

        # **************************************
        response = self.request_get("","/1658")
        response.json = json.loads(response.data.decode("utf-8") )

        # no found en la respuesta
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_search_default_value(self):
        """
        This function test searching a default value according a identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/search")
        response.json = json.loads( response.data.decode("utf-8") )
        self.assertEquals({}, response.json )

        response = self.request_get("","/search?by_branch=1&branch_id=9")
        response.json = json.loads( response.data.decode("utf-8") )

        # no found en la respuesta
        self.assertEqual('NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a default-values
         ** First test create with bad default-values data
         ** Second test create with correct default-values data
         ** Third test update default-values
         ** Fourth test delete default-values
        """
        default_values = {
            'quantityDecimals': None,
            'posAlwaysCash': None,
            'currencyId': None,
            'lastDayPay': None,
            'paymentBy': None,
            'destinyWarehouse': {
                'destinyWarehouseId': 22,
                'code': '005',
                'name': 'OMEGA4',
                'typeWarehouse': 'G'
            },
            'dependencyId': None,
            'provisionMethod': None,
            'sourceWarehouse': {
                'typeWarehouse': 'G',
                'code': '001',
                'name': 'YEFF BODEGA',
                'sourceWarehouseId': 20
            },
            'bank': None,
            'debitAccountId': None,
            'printPOSComments': None,
            'sectionId': None,
            'section': None,
            'valueDecimals': None,
            'productionWarehouse': {
                'productionWarehouseId': 21,
                'code': '002',
                'name': 'OMEGA',
                'typeWarehouse': 'G'
            },
            'sourceWarehouseId': 20,
            'descriptionFrom': None,
            'allowNegativeStock': None,
            'printDescription': None,
            'costCenter': None,
            'posRoundValue': None,
            'destinyWarehouseId': 22,
            'activateTip': None,
            'isDeleted': None,
            'productionWarehouseId': 21,
            'costCenterId': None,
            'division': None,
            'controlCreditLimit': None,
            'iprfid': '987654321',
            'manualUnitValue': None,
            'hideCost': None,
            'dependency': None,
            'activateOtherDisccount': None,
            'disccount2TaxBase': None,
            'posText': None,
            'invoiceText': None,
            'commentsGiftVoucher': None,
            'alertBefore': None,
            'currency': None,
            'alertAfter': None,
            'divisionId': None,
            'controlPastPortfolio': None,
            "branchId": 30,

            "treasuryCostCenterId": 4,
            "treasuryDependencyId": None,
            "treasuryDivisionId": 13,
            "treasurySectionId": 7,

            "purchaseCostCenterId": 4,
            "purchaseDependencyId": None,
            "purchaseDivisionId": 13,
            "purchaseSectionId": 7
        }

        response = self.request_post(default_values)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        print(">>>DV ", response.json)
        if 'message' in response.json:
            response = self.request_get("", "/search?by_branch=1&branch_id="+str(default_values["branchId"]))
            response.json = json.loads(response.data.decode("utf-8"))
        else:
            self.assertIn("defaultValueId", response.json)

        print(">>>DV ", response.json)
        self.defaultValueId = response.json['defaultValueId']

        response = self.request_get("", "/" + str(self.defaultValueId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('quantityDecimals', response.json)
        self.assertIn('printDescription', response.json)
        self.assertIn('costCenter', response.json)
        self.assertIn('controlPastPortfolio', response.json)

        # *********************UPDATE*************************
        branchdata_copy = copy.deepcopy(default_values)
        branchdata_copy['quantityDecimals'] = 3
        branchdata_copy['printDescription'] = 1
        branchdata_copy['division'] = 6
        branchdata_copy['defaultValueId'] = self.defaultValueId

        response = self.request_put(branchdata_copy, "/" + str(self.defaultValueId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.defaultValueId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(branchdata_copy['quantityDecimals'], response.json['quantityDecimals'])
        self.assertEqual(branchdata_copy['printDescription'], response.json['printDescription'])

        # *********************DELETE*************************
        # response = self.request_delete("", "/" + str(self.defaultValueId))  # envio el request al server
        # response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        #
        # self.assertIn("message", response.json)