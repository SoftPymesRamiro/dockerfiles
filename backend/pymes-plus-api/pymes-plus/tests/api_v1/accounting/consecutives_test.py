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
from copy import copy

"""
This module shows various methods and function by allow
handled consecutives
"""
class ConsecutivesTest(unittest.TestCase):
    """
    This Class is a  Test Case for consecutives API class
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
        """Sent get request to #/api/v1/consecutives# with consecutives data values

        :param data: consecutives data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/consecutives'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/consecutives# with consecutives data values

        :param data: consecutives data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/consecutives'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/consecutives# with consecutives data values

        :param data: consecutives data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/consecutives'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/consecutives# with consecutives data values

        :param data: consecutives data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/consecutivess'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_consecutive_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """

        # envio la peticion al sevidor
        response = self.request_get("", "/search?branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        response = self.request_get("", "/search?branch_id=1445445")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertEquals(response.json['data'], [])


        response = self.request_get("", "/search?short_word=RP&branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("billingResolutionId" in response.json)
        self.assertTrue("consecutiveId" in response.json)
        self.assertTrue("isDeleted" in response.json)
        self.assertTrue("updateBy" in response.json)
        self.assertTrue("lastConsecutive" in response.json)
        self.assertTrue("documentTypeId" in response.json)
        self.assertTrue("branchId" in response.json)


    def test_post_consecutive(self):
        """
        This function allow create, update and delete a divisions
         ** First test create with bad divisions data
         ** Second test create with correct divisions data
         ** Third test update divisions
         ** Fourth test delete divisions
        """
        response = self.request_get("", "/search?branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))
        consecutives = response.json['data'][0]

        # del consecutives['consecutiveId']
        del consecutives['createdBy']
        del consecutives['updateBy']
        del consecutives['updateDate']
        del consecutives['creationDate']

        self.value = copy(consecutives['lastConsecutive'])
        # consecutives['lastConsecutive'] = 10

        response = self.request_post([consecutives])
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertTrue("ok" in response.json)

        response = self.request_get("", "/search?short_word=EG&branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("billingResolutionId" in response.json)
        self.assertTrue("consecutiveId" in response.json)
        self.assertTrue("isDeleted" in response.json)
        self.assertTrue("updateBy" in response.json)
        self.assertTrue("lastConsecutive" in response.json)
        self.assertTrue("documentTypeId" in response.json)
        self.assertTrue("branchId" in response.json)
        self.assertTrue("lastConsecutive" in response.json)

        consecutives['lastConsecutive'] = self.value
        response = self.request_post([consecutives])
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertTrue("ok" in response.json)

