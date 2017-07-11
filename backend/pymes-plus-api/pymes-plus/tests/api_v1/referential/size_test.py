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
This Class is a Test Case for Size API class
"""
class SizeTest(unittest.TestCase):
    """
    This Class is a Test Case for Sections API class
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
        """Sent get request to #/api/v1/sizes# with sizes data values

        :param data: sizes data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sizes'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/sizes# with sizes data values

        :param data: sizes data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sizes'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/sizes# with sizes data values

        :param data: sizes data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sizes'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/sizes# with sizes data values

        :param data: sizes data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sizes'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_sizes(self):
        """
        This function test get all size
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_size_company(self):
        """
        This function test get a size according to company identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        size = response.json['data'][0]

        response = self.request_get("","/company/"+str(size['companyId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


  
    def test_get_size(self):
        """
        This function test get a size according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        size = response.json['data'][0]
        response = self.request_get("","/"+str(size['sizeId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("sizeId" in response.json)
        self.assertTrue("companyId" in response.json)
        self.assertTrue("updateBy" in response.json)
        self.assertIsNotNone(response.json['creationDate'])
        

    def test_search_sizes(self):
        """
        This function test search size according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        size = response.json['data'][0]

        response = self.request_get("","/search?search=1234&companyId="+str(size['companyId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        size_response = response.json['data'][0]

        self.assertTrue("sizeId" in size_response)
        self.assertTrue("companyId" in size_response)
        self.assertTrue("updateBy" in size_response)
        self.assertIsNotNone(size_response['creationDate'])

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a size
         ** First test create with bad size data
         ** Second test create with correct size data
         ** Third test update size
         ** Fourth test delete size
        """
        size_data = {
          'companyId': 1,
          'isDeleted': 0,
          'code': 'TSTSIZE'
        }

        response = self.request_post(size_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("sizeId", response.json)
        self.sizeId = response.json['sizeId']

        response = self.request_get("", "/" + str(self.sizeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("companyId", response.json)
        self.assertIn("isDeleted", response.json)
        self.assertIn("sizeId", response.json)
        self.assertIn("code", response.json)

        # *********************UPDATE*************************
        size_copy = copy.deepcopy(size_data)
        size_copy['code'] = "TSTUP"
        size_copy['sizeId'] = self.sizeId

        response = self.request_put(size_copy, "/" + str(self.sizeId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.sizeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(size_copy['companyId'], response.json['companyId'])
        self.assertEqual(size_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(size_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.sizeId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)