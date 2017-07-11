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
class CityTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/citiesn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/cities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/citiesn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/cities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/citiesn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/cities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/citiesn# with city data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/cities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################


    def test_get_cities(self):
        """
        This function test get all city
        ** First validate that contians the data key and content
        """
        response = self.request_get("") # envio petiocn al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # valido la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # no puede ser vacio

    def test_get_city(self):
        """
        This function test get a city according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("") # envio petiocn al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # valido la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # no puede ser vacio

        city = response.json['data'][0]
        self.cityId = city['cityId']

        response = self.request_get("","/"+str(self.cityId)) # envio petion al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto la respuesta a json
        # validate keys in response
        self.assertTrue("departmentId" in response.json, 'incorrect response by correct request' )

        response = self.request_get("","/9148974") # envio petion al sevidor
        response.json = json.loads( response.data.decode("utf-8") )
        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')

    def test_get_city_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("") # envio petiocn al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # valido la clave en la respuesta
        self.assertIsNotNone(response.json['data']) # no puede ser vacio

        city = response.json['data'][0]
        self.cityId = city['cityId']

        response = self.request_get("","/search?city_id="+str(self.cityId)+"&search=1") # envio petion al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto la respuesta a json

        # validate keys in response
        self.assertTrue("totalCount" in response.json, 'incorrect response by correct request' )
        self.assertTrue("cities" in response.json, 'incorrect response by correct request' )
        self.assertTrue("totalPages" in response.json, 'incorrect response by correct request' )

        response = self.request_get("","/search?city_id=822&search=1") # envio petion al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto la respuesta a json

        # validate keys in response
        self.assertTrue("totalCount" in response.json, 'incorrect response by correct request' )
        self.assertTrue("cities" in response.json, 'incorrect response by correct request' )
        self.assertTrue("totalPages" in response.json, 'incorrect response by correct request' )

        response = self.request_get("","/search?search=4542&simple=1") # OJO SI SE ACTIVA PURSHASE IGUAL RETORNA
        response.json = json.loads( response.data.decode("utf-8") ) # convierto la respuesta a json

        self.assertTrue('error' in response.json, 'incorrect')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a ciites
         ** First test create with bad city data
         ** Second test create with correct city data
         ** Third test update city
         ** Fourth test delete city
        """
        city_data={
            'departmentId': 11,
            'indicative': '56',
            'name': 'CITY TEST',
            'code': '999',
            'isDeleted': 0,
        }

        response = self.request_post(city_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("cityId", response.json)
        self.cityId = response.json['cityId']

        response = self.request_get("", "/" + str(self.cityId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('departmentId', response.json)
        self.assertIn('cityId', response.json)
        self.assertIn('code', response.json)
        self.assertIn('indicative', response.json)

        # *********************UPDATE*************************
        city_copy = copy.deepcopy(city_data)
        city_copy['name'] = "CITY TEST UPDATE"
        city_copy['isDeleted'] = 1
        city_copy['code'] = "998"
        city_copy['cityId'] = self.cityId

        response = self.request_put(city_copy, "/" + str(self.cityId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.cityId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(city_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(city_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.cityId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
