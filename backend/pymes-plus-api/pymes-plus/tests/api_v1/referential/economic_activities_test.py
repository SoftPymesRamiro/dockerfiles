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
from copy import copy
"""
This Class is a Test Case for Economic Activities API class
"""
class EconomicActivitiesTest(unittest.TestCase):
    """
    This Class is a Test Case for Economic acttivities API class
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

    # ############################### REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/economic_activities# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/economic_activities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/economic_activities# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/economic_activities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/economic_activities# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/economic_activities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/economic_activities# with divisions data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/economic_activities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    # #####################################################################################

    def test_get_economic_activities(self):
        """
        This function test get all economic activities
        ** First validate that contains the items key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_economic_activity(self):
        """
        This function test get a economic activity according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/470")
        response.json = json.loads( response.data.decode("utf-8"))

        self.assertIn('name', response.json)
        self.assertEqual(response.json['economicActivityId'], 470)
        self.assertIn('updateBy', response.json)
        self.assertIn('creationDate', response.json)

        response = self.request_get("", "/4748770")
        response.json = json.loads( response.data.decode("utf-8") )

        # print("##"*10, response.json)

    def test_search_economic_activity(self):
        """
        This function test get a economic activity according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?economic_activityid=3&company_id=1")
        response.json = json.loads( response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        self.economic_activity = response.json['data'][0]

        self.assertIn('name', self.economic_activity)
        self.assertIn('puc', self.economic_activity)
        self.assertIn('code', self.economic_activity)

        response = self.request_get("", "/search?search=cultivo")
        response.json = json.loads(response.data.decode("utf-8"))


        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        self.economic_activity = response.json['data'][0]

        self.assertIn('name', self.economic_activity)
        self.assertIn('economicActivityId', self.economic_activity)
        self.assertIn('code', self.economic_activity)

        response = self.request_get("", "/search?simple=1&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn('economicActivities', response.json)
        self.assertIn('totalCount', response.json)
        self.assertIn('totalPages', response.json)
