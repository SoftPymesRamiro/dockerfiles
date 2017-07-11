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
handled amortization
"""
class AmortizationTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/amortization# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/amortizations'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/amortizations# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/amortizations'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/amortizations# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/amortizations'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/amortizations# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/amortizations'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_amortization_bycompany(self):
        """

        :return:
        """
        response = self.request_get("", "/company/1") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a amortization
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        amortization= {
            'isDeleted': 0,
            'companyId': 1,
            # 'amortizationId': 1378,
            'expensePuc': {
                'pucId': 84156,
                'account': '105205005',
                'name': 'NOMBREPRUEBAAUXILIAR'
            },
            'expensePUCId': 84156,
            'deferredPuc': {
                'pucId': 84156,
                'account': '105205005',
                'name': 'NOMBREPRUEBAAUXILIAR'
            },
            'deferredPUCId': 84156
        }
        #
        response = self.request_post(amortization)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("amortizationId", response.json)
        self.amortizationId = response.json['amortizationId']

        # *********************UPDATE*************************
        amortization_copy = copy(amortization)
        amortization_copy['deferredPuc'] = {'pucId': 84111, 'account': '105105003', 'name': 'ASDFG' }
        amortization_copy['deferredPUCId'] = 84111
        amortization_copy['amortizationId'] = self.amortizationId

        response = self.request_put(amortization_copy, "/"+str(self.amortizationId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.amortizationId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/45646546")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')
