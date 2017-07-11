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
This Class is a Test Case for Dependencies API class
"""
class DependenciesTest(unittest.TestCase):
    """
    This Class is a Test Case for Dependencies API class
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
        """Sent get request to #/api/v1/dependencies# with dependencies data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/dependencies'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/dependencies# with dependencies data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/dependencies'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/dependencies# with dependencies data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/dependencies'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/dependencies# with dependencies data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/dependencies'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_dependencies(self):
        """
        This function test get all dependencies
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        # print("##"*10, response.json)


    def test_get_dependency(self):
        """
        This function test get a dependenciy according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/4")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("sectionId" in response.json)
        self.assertTrue("pucId" in response.json)
        self.assertTrue("dependencyId" in response.json)
        self.assertTrue("name" in response.json)




    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a dependencies
         ** First test create with bad dependencies data
         ** Second test create with correct dependencies data
         ** Third test update dependencies
         ** Fourth test delete dependencies
        """
        dependency_data ={
          'puc': None,
          'code': '0099',
          'name': 'TEST DEPENDENCY',
          'pucId': None,
          'isDeleted': 0,
          'sectionId': 6
        }

        response = self.request_post(dependency_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("dependencyId", response.json)
        self.dependencyId = response.json['dependencyId']

        response = self.request_get("", "/" + str(self.dependencyId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('puc', response.json)
        self.assertIn('code', response.json)
        self.assertIn('dependencyId', response.json)

        # *********************UPDATE*************************
        departament_copy = copy.deepcopy(dependency_data)
        departament_copy['name'] = "TEST DEPENDENCY UPDATE"
        departament_copy['code'] = "098"
        departament_copy['dependencyId'] = self.dependencyId

        response = self.request_put(departament_copy, "/" + str(self.dependencyId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.dependencyId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(departament_copy['name'], response.json['name'])
        self.assertEqual(departament_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.dependencyId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)