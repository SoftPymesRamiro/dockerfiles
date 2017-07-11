#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
import time
import logging
import copy

from app import create_app
from app.api_v1 import api

"""
This module shows various methods and function by allow
handled cities
"""
class ClosePeriods(unittest.TestCase):
    """
    This Class is a  Test Case for Close Periods Api class
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
    def request_get(self, data, path="/"):
        """Sent get request to #/api/v1/close_periods# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/close_periods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/close_periodsn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/close_periods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/close_periodsn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/close_periods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/close_periodsn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/close_periods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_closed_periods(self):
        """
        This function test get a close periods
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("") # envio petiocn al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # valido la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # no puede ser vacio


    def test_get_closeperiods_search(self):
        """
        This function test get a close periods
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("") # envio petiocn al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # valido la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # no puede ser vacio

        closed_period = response.json['data'][0]
        branchId = closed_period['branchId']
        dayClosed = "Wed, 09 Jan 2014 19:00:00 GMT"  # -- fecha en js

        response = self.request_get("", "/search?branch_id="+str(branchId)+"&day="+str(dayClosed))  # envio petiocn al sevidor
        response.json = json.loads(response.data.decode("utf-8"))  # convierto a json object

        self.assertTrue("close_day" in response.json)  # valido la clave en la respuesta