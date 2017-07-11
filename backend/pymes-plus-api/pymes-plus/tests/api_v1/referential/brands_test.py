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
import copy
import time
import logging


from app import create_app
from app.api_v1 import api

"""
This module shows several methods and function by allow
handled brands
"""
class BrandsTest(unittest.TestCase):
    """
    This Class is a  Test Case for Brands Api class
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
        """Sent get request to #/api/v1/brands# with brands data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/brands'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/brands# with brands data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/brands'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/brands# with brands data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/brands'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/brands# with brands data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/brands'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_brands(self):
        """
        This function test get all brands
        ** First validate that contains the data key and content
        """
        response = self.request_get("") # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # validacoiojn de la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # debe tener contenido


    def test_get_brand(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/6") # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object
        # validate keys in response
        self.assertTrue("createdBy" in response.json, 'incorrect response by correct request' )


        response = self.request_get("","/9148974")# envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object
        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')




    def test_get_brand_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/search?search=milton&simple=1")# envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object
        # validate keys in response
        self.assertTrue("brandId" in response.json['data'][0]  , 'incorrect response by correct request' )


        response = self.request_get("","/search?search=4542&simple=1") # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object
        # validate response
        self.assertEqual(response.json['data'], [], 'incorrect')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a brands
         ** First test create with bad brand data
         ** Second test create with correct brand data
         ** Third test update brand
         ** Fourth test delete brand
        """
        brand_data ={
          'isDeleted': 0,
          'name': 'Brand Test',
        }

        response = self.request_post(brand_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("brandId", response.json)
        self.brandId = response.json['brandId']

        response = self.request_get("", "/" + str(self.brandId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('creationDate', response.json)
        self.assertIn('isDeleted', response.json)
        self.assertIn('isDeleted', response.json)
        self.assertIn('createdBy', response.json)

        # *********************UPDATE*************************
        brand_copy = copy.deepcopy(brand_data)
        brand_copy['creationDate'] = ""
        brand_copy['isDeleted'] = 1
        brand_copy['name'] = "Brand Test UPDATE"
        brand_copy['brandId'] = self.brandId

        response = self.request_put(brand_copy, "/" + str(self.brandId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.brandId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertNotEqual(brand_copy['creationDate'], response.json['creationDate'])
        self.assertEqual(brand_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(brand_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.brandId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
