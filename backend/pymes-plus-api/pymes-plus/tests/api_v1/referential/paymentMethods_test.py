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


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for paymentMethods Test API class
"""
class paymentMethodsTest(unittest.TestCase):
    """
    This Class is a Test Case for paymentMethods API class
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
        """Sent get request to #/api/v1/paymentMethods# with paymentMethods data values

        :param data: paymentMethods data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/paymentMethods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/paymentMethods# with paymentMethods data values

        :param data: paymentMethods data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/paymentMethods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/paymentMethods# with paymentMethods data values

        :param data: paymentMethods data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/paymentMethods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/paymentMethods# with paymentMethods data values

        :param data: paymentMethods data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/paymentMethods'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_paymentMethods(self):
        """
        This function test get all paymentMethods
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

    def test_get_paymentMethod(self):
        """
        This function test get a items according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/3")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("pymentType" in response.json)
        self.assertTrue("name" in response.json)

        self.assertIsNotNone(response.json['createdBy'])


        response = self.request_get("","/125")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')
        # print("#"*10, response.json)

    def test_search_paymentMethods(self):
        """
        This function test search a paymentMethods according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/search?search='DEPOSITO'&words='DEPOSITO' ")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        # print("#"*10, response.json)



    ##################################################################################
    # FALTAN POST, PUT AND DELETE