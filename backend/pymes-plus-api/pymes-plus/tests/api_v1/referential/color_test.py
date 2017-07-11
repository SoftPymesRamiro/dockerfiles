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
import copy

"""
This module shows various methods and function by allow
handled color
"""
class ColorTest(unittest.TestCase):
    """
    This Class is a  Test Case for Color API class
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
        """Sent get request to #/api/v1/colors# with colors data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/colors'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/colors# with colors data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/colors'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/colors# with colors data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/colors'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/colors# with colors data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/colors'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_colors(self):
        """
        This function test get all colors
        ** First validate that contians the data key and content
        """
        response = self.request_get("") # envio la petion al sevidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("data" in response.json) # clave da en colores
        self.assertIsNotNone(response.json['data']) # no puede vacia



    def test_get_color(self):
        """
        This function test get a color according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?search=") # envio la peticion
        response.json = json.loads( response.data.decode("utf-8") ) # convierte a json object
        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        response.json = response.json['data'][0]
        # validacion de la clave en la respuesta
        self.assertTrue("name" in response.json, 'incorrect response by correct request' )

        response = self.request_get("", "/9148974") # envio la peticion
        response.json = json.loads( response.data.decode("utf-8") ) # convierte a json object
        # no found en la respuesta
        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')


    def test_get_color_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?search=BLAN Hola") # envio la peticion
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object
        #
        self.assertEqual(len(response.json['data']), 2, 'incorrect response by correct request' )

        response = self.request_get("", "/search?search=dsadsadlsakdjs") ## OJO SI SE ACTIVA PURSHASE IGUAL RETORNA
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue('data' in response.json, 'incorrect')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a ciites
         ** First test create with bad city data
         ** Second test create with correct city data
         ** Third test update city
         ** Fourth test delete city
        """
        color_data={
          'code': 'TST',
          'isDeleted': 0,
          'name': 'TESTCOLOR'
        }

        response = self.request_post(color_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("colorId", response.json)
        self.colorId = response.json['colorId']

        response = self.request_get("", "/" + str(self.colorId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('creationDate', response.json)
        self.assertIn('code', response.json)
        self.assertIn('colorId', response.json)

        # *********************UPDATE*************************
        color_copy = copy.deepcopy(color_data)
        color_copy['name'] = "TESTUPDATE"
        color_copy['code'] = "UPDT"
        color_copy['colorId'] = self.colorId

        response = self.request_put(color_copy, "/" + str(self.colorId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.colorId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(color_copy['name'], response.json['name'])
        self.assertEqual(color_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.colorId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
