#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
from copy import *
import time
import logging


from app import create_app
from app.api_v1 import api
import copy

"""
This module shows various methods and function by allow
handled Country
"""
class CountryTest(unittest.TestCase):
    """
    This Class is a Test Case for Country API class
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
        """Sent get request to #/api/v1/countries# with countries data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/countries'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent get request to #/api/v1/countries# with countries data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/countries'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent get request to #/api/v1/countries# with countries data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/countries'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent get request to #/api/v1/countries# with countries data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/countries'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_countries(self):
        """
        This function test get all countries
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_cost_countrie(self):
        """
        This function test get a color according to branch identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/1")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("createdBy" in response.json, 'incorrect response by correct request' )


        response = self.request_get("","/9148974")
        response.json = json.loads( response.data.decode("utf-8") )
        # no found en la respuesta
        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a cost_Centers
         ** First test create with bad cost-center data
         ** Second test create with correct cost-center data
         ** Third test update cost-center
         ** Fourth test delete cost-center
        """
        country_data = {
            'code': 'TST',
            'dianCode': '268',
            'indicative': '999',
            'name': 'TEST COUNTRY',
            'isDeleted': 0,
            'departments': [
                {
                    'name': 'TEST DEPTO1',
                    'code': '991',
                    'isDeleted': 0,
                    'departmentId': 35,
                    'cities': [

                    ],
                },
                {
                    'name': 'TEST DEPTO2',
                    'code': '992',
                    'isDeleted': 0,
                    'departmentId': 36,
                    'cities': [

                    ],
                },
                {
                    'name': 'TEST DEPTO3',
                    'code': '993',
                    'isDeleted': 0,
                    'departmentId': 37,
                    'cities': [
                        {
                            'name': 'TEST CITY DEPTO',
                            'code': '994',
                            'isDeleted': 0,
                            'departmentId': 37,
                            'cityId': 1117
                        }
                    ],
                }
            ]
        }

        response = self.request_post(country_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("countryId", response.json)
        self.countryId = response.json['countryId']

        response = self.request_get("", "/" + str(self.countryId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('code', response.json)
        self.assertIn('name', response.json)
        self.assertIn('dianCode', response.json)
        self.assertIn('indicative', response.json)

        # *********************UPDATE*************************
        brand_copy = copy.deepcopy(country_data)
        brand_copy['code'] = "TUP"
        brand_copy['dianCode'] = "278"
        brand_copy['name'] = "TEST COUNTRY UPDATE"
        brand_copy['countryId'] = self.countryId

        response = self.request_put(brand_copy, "/" + str(self.countryId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.countryId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(brand_copy['code'], response.json['code'])
        self.assertEqual(brand_copy['dianCode'], response.json['dianCode'])
        self.assertEqual(brand_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.countryId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

