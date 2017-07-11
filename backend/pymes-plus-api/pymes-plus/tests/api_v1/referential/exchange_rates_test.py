#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential  TEST module
# app
# This create_app from app with Blueprint (modular flask)
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import Flask
import unittest
import json
import time
import logging


from app import create_app
from app.api_v1 import api
import copy

"""
This Class is a Test Case for Exchange Rates API class
"""
class ExchangeRates(unittest.TestCase):
    """
    This Class is a Test Case for Exchange Rates API class
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
        """Sent get request to #/api/v1/exchange_rates# with exchange-rates data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/exchange_rates'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/exchange_rates# with exchange-rates data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/exchange_rates'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/exchange_rates# with exchange-rates data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/exchange_rates'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/exchange_rates# with exchange-rates data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/exchange_rates'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_exchange_rates(self):
        """
        This function test get all exchange_rates
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        self.exchange_rate = response.json['data'][0]

        response = self.request_get("","/"+str(self.exchange_rate['exchangeRateId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertIn('currency', response.json)
        self.assertIn('currencyId', response.json)
        self.assertIn('rate', response.json)
        self.assertIn('exchangeRateId', response.json)
        self.assertIn('date', response.json)

        # # envio la peticion al sevidor
        response = self.request_get("", "/search?branch_id=14&search=")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.exchange_rate = response.json['data'][0]

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a exchange_rates
         ** First test create with bad exchange_rates data
         ** Second test create with correct exchange_rates data
         ** Third test update exchange_rates
         ** Fourth test delete exchange_rates
        """
        self.exchange_rate={
          "rate": 1.31,
          "currency": {
            "symbol": "CAD",
            "code": "CAD",
            "currencyId": 36,
            "name": "DOLAR CANADIENSE",
          },
          "date": "Mon, 26 Sep 2016 19:33:27 GMT"
        }

        response = self.request_post(self.exchange_rate)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("exchangeRateId", response.json)
        self.exchangeRateId = response.json['exchangeRateId']

        response = self.request_get("", "/" + str(self.exchangeRateId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('currency', response.json)
        self.assertIn('currencyId', response.json)
        self.assertIn('rate', response.json)
        self.assertIn('exchangeRateId', response.json)
        self.assertIn('date', response.json)

        # *********************UPDATE*************************
        order_copy = copy.deepcopy(self.exchange_rate)
        order_copy['rate'] = 1.35
        order_copy['exchangeRateId'] = self.exchangeRateId

        response = self.request_put(order_copy, "/" + str(self.exchangeRateId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.exchangeRateId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(order_copy['rate'], response.json['rate'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(99999))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.exchangeRateId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)