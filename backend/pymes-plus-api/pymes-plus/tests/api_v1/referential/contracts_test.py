#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
# app
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
import copy
import time
import logging


from app import create_app
from app.api_v1 import api
from datetime import datetime
from copy import copy

"""
This module shows various methods and function by allow
handled contracts
"""
class ContractsTest(unittest.TestCase):
    """
    This Class is a  Test Case for Import Api class
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
        """Sent get request to #/api/v1/contracts# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/contracts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/contracts# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/contracts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/contracts# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/contracts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/contracts# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/contracts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_search_contracts(self):
        """
        This function test get a import concept according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?branch_id=14&search=A") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.contracts = response.json['data'][0]

        # validate keys in response
        self.assertTrue("divisionId" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("createdBy" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("description" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("creationDate" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("branchId" in self.contracts, 'incorrect response by correct request')

        response = self.request_get("",  "/search?branch_id=1464564&search=A") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertTrue("data" in response.json)
        self.assertEquals(response.json['data'], [])

        response = self.request_get("",  "/search?search=A") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a contracts
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        contracts={
          'budget': 90000000.0,
          'isDeleted': 0,
          'costCenterId': 6,
          'creationDate': 'Wed, 16 Sep 2015 09:54:32 GMT',
          'comments': 'TEST AGREEMENT',
          'sectionId': 8,
          'state': False,
          'puc': {
            'percentage': 0.0,
            'name': 'VIAS DE COMUNICACION',
            'companyId': 1,
            'account': '115515005',
            'pucId': 84789
          },
          'providerId': None,
          'pucId': 84789,
          'code': '099',
          'divisionId': 17,
          'description': 'TEST AGREEMENT',
          'dependencyId': None,
          'branchId': 14
        }
        #
        response = self.request_post(contracts)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("contractId", response.json)
        self.contractId = response.json['contractId']

        response = self.request_get("", "/search?branch_id=14&code=099") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.contracts = response.json

        # validate keys in response
        self.assertTrue("divisionId" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("createdBy" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("description" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("creationDate" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("branchId" in self.contracts, 'incorrect response by correct request')

        # # *********************UPDATE*************************
        contracts_copy = copy(contracts)
        contracts_copy['comments'] = "TEST AGREEMENT UPDATE"
        contracts_copy['description'] = "TEST AGREEMENT UPDATE"
        contracts_copy['contractId'] = self.contractId
        #
        response = self.request_put(contracts_copy,"/"+str(self.contractId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/search?branch_id=14&code=099") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.contracts = response.json

        # validate keys in response
        self.assertTrue("divisionId" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("createdBy" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("description" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("creationDate" in self.contracts, 'incorrect response by correct request')
        self.assertTrue("branchId" in self.contracts, 'incorrect response by correct request')
        self.assertEqual(self.contracts['code'], "099")
        self.assertNotEqual(self.contracts['comments'], 'TEST AGREEMENT')
        self.assertEqual(self.contracts['comments'], 'TEST AGREEMENT UPDATE')

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.contractId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/45646546")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')
