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
This Class is a Test Case for MeasurementUnits Test API class
"""
class MeasurementUnits(unittest.TestCase):
    """
    This Class is a Test Case for MeasurementUnits API class
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
        """Sent get request to #/api/v1/measurement_units# with measurement_units data values

        :param data: measurement_units data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/measurement_units'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/measurement_units# with measurement_units data values

        :param data: measurement_units data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/measurement_units'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/measurement_units# with measurement_units data values

        :param data: measurement_units data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/measurement_units'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/measurement_units# with measurement_units data values

        :param data: measurement_units data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/measurement_units'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_measurement_units(self):
        """
        This function test get all economic activities
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

    def test_get_measurement_unit(self):
        """
        This function test get a items according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        measurement_units = response.json['data'][0]

        response = self.request_get("", "/"+str(measurement_units['measurementUnitId']))

        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("updateBy" in response.json)
        self.assertTrue("factor" in response.json)
        self.assertIsNotNone(response.json['name'])


    def test_search_measurement_units(self):
        """
        This function test search a measurement_units according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?simple=1")
        response.json = json.loads(response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        self.assertIn("code", response.json['data'][0])
        self.assertIn("name", response.json['data'][0])

        response = self.request_get("", "/search?to_search=1&search='CAJ'")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertEqual([], response.json['data'])


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a measurement_units
         ** First test create with bad measurement_units data
         ** Second test create with correct measurement_units data
         ** Third test update measurement_units
         ** Fourth test delete measurement_units
        """
        measurement_units = {
          'code': '098',
          'isDeleted': 0,
          'name': 'TEST PRODUCT',
          'factor': 8989.0,
          'weight': False,
        }
        response = self.request_post(measurement_units)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("measurementUnitId", response.json)
        self.measurementUnitId = response.json['measurementUnitId']

        response = self.request_get("", "/" + str(self.measurementUnitId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('creationDate', response.json)
        self.assertIn('isDeleted', response.json)
        self.assertIn('createdBy', response.json)

        # *********************UPDATE*************************
        measurement_copy = copy.deepcopy(measurement_units)
        measurement_copy['creationDate'] = ""
        measurement_copy['isDeleted'] = 1
        measurement_copy['code'] = '099'
        measurement_copy['name'] = 'TEST PRODUCT UPDATE'
        measurement_copy['measurementUnitId'] = self.measurementUnitId

        response = self.request_put(measurement_copy, "/" + str(self.measurementUnitId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.measurementUnitId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertNotEqual(measurement_copy['creationDate'], response.json['creationDate'])
        self.assertEqual(measurement_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(measurement_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.measurementUnitId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

