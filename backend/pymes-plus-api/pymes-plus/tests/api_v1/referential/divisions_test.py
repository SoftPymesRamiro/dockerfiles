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
class DivisionsTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/divisions# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/divisions'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/divisions# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/divisions'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/divisions# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/divisions'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/divisions# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/divisions'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_divisions(self):
        """
        This function test get all divisions
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_division(self):
        """
        This function test get a divisions according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/4")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("costCenterId" in response.json)
        self.assertTrue("pucId" in response.json)
        self.assertTrue("updateBy" in response.json)
        self.assertTrue("createdBy" in response.json)
        self.assertTrue("sections" in response.json)
        self.assertTrue("divisionId" in response.json)
        self.assertTrue("isDeleted" in response.json)



    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a divisions
         ** First test create with bad divisions data
         ** Second test create with correct divisions data
         ** Third test update divisions
         ** Fourth test delete divisions
        """
        division_data={
          'puc': {
            'pucId': 87304,
            'percentage': 0.0,
            'account': '510000000 GASTOS - OPERACIONALES DE ADMINISTRACION'
          },
          'costCenterId': 8,
          'sections': [

          ],
          'updateDate': 'Wed, 30 Sep 2015 15:51:30 GMT',
          'name': 'TEST DIVISION',
          'pucId': 87304,
          'code': '00998',
          'isDeleted': 0
        }

        response = self.request_post(division_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("divisionId", response.json)
        self.divisionId = response.json['divisionId']

        response = self.request_get("", "/" + str(self.divisionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('divisionId', response.json)
        self.assertIn('pucId', response.json)
        self.assertIn('costCenterId', response.json)

        # *********************UPDATE*************************
        division_copy = copy.deepcopy(division_data)
        division_copy['name'] = "TEST DIVISION UPDATE"
        division_copy['code'] = "00999"
        division_copy['divisionId'] = self.divisionId

        response = self.request_put(division_copy, "/" + str(self.divisionId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.divisionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(division_copy['name'], response.json['name'])
        self.assertEqual(division_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.divisionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)