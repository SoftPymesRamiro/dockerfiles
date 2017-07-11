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
import time
import logging


from app import create_app
from app.api_v1 import api
import copy
"""
This Class is a Test Case for division API class
"""
class ProductionOrderTest(unittest.TestCase):
    """
    This Class is a Test Case for Divisions API class
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
        """Sent get request to #/api/v1/production_orders# with production_orders data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/production_orders'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/production_orders# with production_orders data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/production_orders'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/production_orders# with production_orders data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/production_orders'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/production_orders# with production_orders data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/production_orders'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_production_orders(self):
        """
        This function test get all production_orders
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        self.production_order = response.json['data'][0]

        response = self.request_get("","/"+str(self.production_order['productionOrderId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertIn('name', response.json)
        self.assertIn('divisionId', response.json)
        self.assertIn('pucId', response.json)
        self.assertIn('costCenterId', response.json)

        # # envio la peticion al sevidor
        response = self.request_get("", "/search?branch_id=14&search=")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.production_order = response.json['data'][0]


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a production_orders
         ** First test create with bad production_orders data
         ** Second test create with correct production_orders data
         ** Third test update production_orders
         ** Fourth test delete production_orders
        """
        self.production_order={
          "isKit": 0,
          "budget": 80000.555,
          "costCenterId": 4,
          "createdBy": "TEST",
          "customerId": 251,
          "updateBy": "TEST",
          "comments": "TEST COMMENTS",
          "divisionId": 13,
          "orderNumber": "0000000001",
          "sectionId": 7,
          "pucId": 84678,
          "branchId": 14,
          "dateTo": "Tue, 10 Nov 2015 05:00:00 GMT",
          "name": "TEST PROD",
          "isDeleted": 0,
          "dateFrom": "Tue, 03 Nov 2015 05:00:00 GMT",
          "date": "Mon, 11 May 2015 00:00:00 GMT",
          "productionUnits": 900,
          "state": 0,
          "mode": 2,
          "dependencyId": None
        }
        response = self.request_post(self.production_order)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("productionOrderId", response.json)
        self.productionOrderId = response.json['productionOrderId']

        response = self.request_get("", "/" + str(self.productionOrderId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('createdBy', response.json)
        self.assertIn('budget', response.json)
        self.assertIn('productionUnits', response.json)
        self.assertIn('branchId', response.json)
        self.assertIn('date', response.json)
        self.assertIn('comments', response.json)

        # *********************UPDATE*************************
        order_copy = copy.deepcopy(self.production_order)
        order_copy['name'] = "TEST PROD UPDATE"
        order_copy['comments'] = "COMMEnTS UPDATE"
        order_copy['productionOrderId'] = self.productionOrderId

        response = self.request_put(order_copy, "/" + str(self.productionOrderId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.productionOrderId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(order_copy['name'], response.json['name'])
        self.assertEqual(order_copy['comments'], response.json['comments'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(99999))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("error", response.json)
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.productionOrderId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)