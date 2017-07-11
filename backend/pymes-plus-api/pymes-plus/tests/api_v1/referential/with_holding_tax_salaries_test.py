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
This Class is a Test Case for Withholdingtaxsalary API class
"""


class WithholdingtaxsalaryTest(unittest.TestCase):
    """
    This Class is a Test Case for Withholdingtaxsalary API class
    """

    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
                             password='Admin*2')  # valid data by access to SoftPymes plus

        app = Flask(__name__)  # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self)  # test client
        self.test_client.testing = False  # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                                              data=json.dumps(self.userdata),
                                              content_type='application/json')
        # User token
        self.token = json.loads(self.response.data.decode("utf-8"))['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self, data, path="/"):
        """Sent get request to #/api/v1/withholdingtaxsalaries# with Withholdingtaxsalary data values

        :param data: Withholdingtaxsalary data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/withholdingtaxsalaries' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/withholdingtaxsalaries# with Withholdingtaxsalary data values

        :param data: Withholdingtaxsalary data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/withholdingtaxsalaries' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/withholdingtaxsalaries# with Withholdingtaxsalary data values

        :param data: Withholdingtaxsalary data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/withholdingtaxsalaries' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/withholdingtaxsalaries# with Withholdingtaxsalary data values

        :param data: Withholdingtaxsalary data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/withholdingtaxsalaries' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_withholdingtaxsalaries(self):
        """
        This function test get all withholdingtaxsalaries
        ** First validate that contains the data key and content
        """

        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.tax = response.json['data'][0]

        self.assertIn("additionalUVT", self.tax)
        self.assertIn("creationDate", self.tax)
        self.assertIn("finalUVT", self.tax)
        self.assertIn("initialUVT", self.tax)
        self.assertIn("withholdingTaxSalaryId", self.tax)
        self.assertIn("description", self.tax)
        self.assertIn("tableType", self.tax)

        response = self.request_get("", "/"+str(self.tax['withholdingTaxSalaryId']))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("additionalUVT", response.json)
        self.assertIn("creationDate", response.json)
        self.assertIn("finalUVT", response.json)
        self.assertIn("initialUVT", response.json)
        self.assertIn("withholdingTaxSalaryId", response.json)
        self.assertIn("description", response.json)
        self.assertIn("tableType", response.json)

    def test_create_update_delete_withholdingtaxsalaries(self):
        """
        Returns: This function will create a row, updated and deleted.
        """

        data = [
          {
            "finalUVT": 993,
            "tableType": 1,
            "description": "Tabla 1, Desde: 991 Hasta: 993",
            "additionalUVT": "0.38",
            "initialUVT": "991",
            "percentage": "0.25"
          },
          {
            "finalUVT": 996,
            "tableType": 1,
            "description": "Tabla 1, Desde: 994 Hasta: 996",
            "additionalUVT": "0.10",
            "initialUVT": "994",
            "percentage": "0.29"
          },
          {
            "finalUVT": 997,
            "tableType": 1,
            "description": "Tabla 1, Desde: 996 Hasta: 997",
            "additionalUVT": "0.24",
            "initialUVT": "996",
            "percentage": "0.87"
          },
          {
            "finalUVT": "1000",
            "tableType": 2,
            "description": "Tabla 2, Desde: 998 Hasta: 1000",
            "additionalUVT": "0.21",
            "initialUVT": "998",
            "percentage": "0.41"
          }
        ]
        # *********************** POST *************************
        # Test Normal Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id for the rest of the TESTs
        self.assertEqual(response.status_code, 200, 'Guardado')
        self.assertIn("ok", response.json)

        # Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # ********************* PUT **************************
        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.tax_salaries = response.json['data']

        # Test update
        response = self.request_post(self.tax_salaries, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # ********************* DELETE  **********************
        for tax in self.tax_salaries:
            if tax['initialUVT']==998 or tax['initialUVT']==996 or tax['initialUVT']==994 or tax['initialUVT']==991:
                response = self.request_delete('', '/' + str(tax['withholdingTaxSalaryId']))
                response.json = json.loads(response.data.decode('utf-8'))

                self.assertIn("message", response.json)
                self.assertEqual(response.json['message'], 'Eliminado correctamente')

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)
