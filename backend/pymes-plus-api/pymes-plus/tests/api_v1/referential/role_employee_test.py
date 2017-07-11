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
This module shows several methods and function by allow
handled BusinessAgentsTest
"""
class RoleEmployeesTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/role_employees# with role_employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/role_employees'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/role_employees# with role_employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/role_employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/role_employees# with role_employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/role_employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/role_employees# with role_employees data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/role_employees'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_role_employees(self):
        """
        This function test get all role_employees
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("", "/search?simple=1&companyId=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.role = response.json['data'][0]

        self.assertIn("name", self.role)
        self.assertIn("roleEmployeeId", self.role)

        # envio la peticion al sevidor
        response = self.request_get("", "/"+str(self.role['roleEmployeeId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("creationDate", response.json)
        self.assertIn("code", response.json)
        self.assertIn("baseSalary", response.json)
        self.assertIn("roleEmployeeId", response.json)
        self.assertIn("companyId", response.json)


    def test_post_put_delete_role_employees(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("", "/search?branch=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        # El contenido debe ser vacia
        self.assertEqual(response.json['data'], [])

        # envio la peticion al sevidor
        response = self.request_get("", "/search?simple=1&companyId=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.role = response.json['data'][0]

        self.assertIn("name", self.role)
        self.assertIn("roleEmployeeId", self.role)

        role =    {
          "baseSalary": 500000,
          "code": "00099",
          "companyId": 1,
          "isDeleted": 0,
          "name": "PRUEBA"
        }

        response = self.request_post(role)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("roleEmployeeId", response.json)
        self.roleEmployeeId = response.json['roleEmployeeId']

        response = self.request_get("", "/" + str(self.roleEmployeeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("creationDate", response.json)
        self.assertIn("code", response.json)
        self.assertIn("baseSalary", response.json)
        self.assertIn("roleEmployeeId", response.json)
        self.assertIn("companyId", response.json)

        # *********************UPDATE*************************
        role_copy = copy.deepcopy(role)
        role_copy['baseSalary'] = 4000000
        role_copy['name'] = "PRUEBA UP"
        role_copy['roleEmployeeId'] = self.roleEmployeeId

        response = self.request_put(role_copy, "/" + str(self.roleEmployeeId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.roleEmployeeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(role_copy['baseSalary'], response.json['baseSalary'])
        self.assertEqual(role_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.roleEmployeeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
