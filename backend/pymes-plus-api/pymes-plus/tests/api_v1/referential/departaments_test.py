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
import copy
import logging


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for Departament API class
"""
class DepartamentsTest(unittest.TestCase):
    """
    This Class is a Test Case for Departament API class
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
        """Sent get request to #/api/v1/departments# with departament data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/departments'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/departments# with departament data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/departments'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/departments# with departament data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/departments'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/departments# with departament data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/departments'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_departaments(self):
        """
        This function test get all departaments
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_departament(self):
        """
        This function test get a departament according a identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        departament = response.json['data'][0]

        response = self.request_get("", "/"+str(departament['departmentId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("cities" in response.json)
        self.assertIsNotNone(response.json['cities'])


    def test_get_country_departament(self):
        """
        This function test search a departament according a identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        departament = response.json['data'][0]

        response = self.request_get("", "/country/"+str(departament['countryId']))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        departament = response.json['data'][0]

        self.assertTrue("departmentId" in departament)
        self.assertTrue("code" in departament)
        self.assertTrue("name" in departament)
        self.assertTrue("cities" in departament)
        self.assertIsNotNone(departament['code'])

        response = self.request_get("", "/country/822")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertEqual([], response.json['data'])


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a departaments
         ** First test create with bad departament data
         ** Second test create with correct departament data
         ** Third test update departament
         ** Fourth test delete departament
        """
        departament_data={
            'name': 'TEST DEPARTAMENT',
            'code': '98',
            'cities': [

            ],
            'isDeleted': 0,
            'countryId': 1
        }

        response = self.request_post(departament_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("departmentId", response.json)
        self.departmentId = response.json['departmentId']

        response = self.request_get("", "/" + str(self.departmentId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('name', response.json)
        self.assertIn('countryId', response.json)

        # *********************UPDATE*************************
        departament_copy = copy.deepcopy(departament_data)
        departament_copy['name'] = "TEST DEPARTAMENT UPDATE"
        departament_copy['code'] = "99"
        departament_copy['departmentId'] = self.departmentId

        response = self.request_put(departament_copy, "/" + str(self.departmentId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.departmentId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(departament_copy['name'], response.json['name'])
        self.assertEqual(departament_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.departmentId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)