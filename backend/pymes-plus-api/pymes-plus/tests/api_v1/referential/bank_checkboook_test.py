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

"""
This module shows various methods and function by allow
handled checkbook
"""
class BankcheckbookTest(unittest.TestCase):
    """
    This Class is a  Test Case for Bankcheckbook Api class
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
        """Sent get request to #/api/v1/bank_checkbook# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/bank_checkbooks'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/bank_checkbook# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/bank_checkbooks'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/bank_checkbook# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/bank_checkbooks'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/bank_checkbook# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/bank_checkbooks'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_bank_checkbook(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.bank_checkbook = response.json['data'][0]

        response = self.request_get("", "/bankaccount/"+str(self.bank_checkbook['bankAccountId'])) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        # validate keys in response
        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.bank_checkbook = response.json['data'][0]

        response = self.request_get("", "/"+str(self.bank_checkbook['bankCheckBookId'])) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        # validate keys in response
        self.assertTrue("prefix" in response.json, 'incorrect response by correct request' )
        self.assertTrue("initialCheck" in response.json, 'incorrect response by correct request' )
        self.assertTrue("finalCheck" in response.json, 'incorrect response by correct request' )
        self.assertTrue("state" in response.json, 'incorrect response by correct request' )
        self.assertTrue("creationDate" in response.json, 'incorrect response by correct request' )

        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(9999))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a bank_checkbook
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        bank_checkbook=[{
          "bankAccountId": "14",
          "bankCheckBookId": "1",
          "finalCheck": "321",
          "initialCheck": "123",
          "isDeleted": 0,
          "lastConsecutive": 145,
          "prefix": "1",
          "state": 1
        }]
        response = self.request_post(bank_checkbook)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)
        self.bank_checkbookId = bank_checkbook[0]['bankCheckBookId']

        response = self.request_post(bank_checkbook)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)
        self.bank_checkbookId = bank_checkbook[0]['bankCheckBookId']
        # *********************DELETE*************************
        response = self.request_delete("", "/9999")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.bank_checkbookId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)