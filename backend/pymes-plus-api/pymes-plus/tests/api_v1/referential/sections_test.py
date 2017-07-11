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
This Class is a Test Case for Sections API class
"""
class SectionsTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/sections# with sections data values

        :param data: sections data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sections'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/sections# with sections data values

        :param data: sections data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sections'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/sections# with sections data values

        :param data: sections data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sections'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/sections# with sections data values

        :param data: sections data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sections'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_sections(self):
        """
        This function test get all sections
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        
    def test_get_section(self):
        """
        This function test get a section according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        section = response.json['data'][1]

        response = self.request_get("", "/"+str(section['sectionId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("pucId" in response.json)
        self.assertTrue("dependencies" in response.json)
        self.assertTrue("divisionId" in response.json)
        self.assertTrue("name" in response.json)
        self.assertIsNotNone(response.json['dependencies'])
        
    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a sections
         ** First test create with bad sections data
         ** Second test create with correct sections data
         ** Third test update sections
         ** Fourth test delete sections
        """
        section_data = {
          'code': '00098',
          'divisionId': 19,
          'isDeleted': 0,
          'pucId': 105708,
          'name': 'TEST SECTION',
          'puc': {
            'percentage': 0.0,
            'pucId': 105708,
            'account': '520000000 GASTOS - OPERACIONALES DE VENTAS'
          }
        }

        response = self.request_post(section_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("sectionId", response.json)
        self.sectionId = response.json['sectionId']

        response = self.request_get("", "/" + str(self.sectionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("pucId", response.json)
        self.assertIn("dependencies", response.json)
        self.assertIn("divisionId", response.json)
        self.assertIn("name", response.json)

        # *********************UPDATE*************************
        section_copy = copy.deepcopy(section_data)
        section_copy['name'] = "TEST SECTION UPDATE"
        section_copy['code'] = "00099"
        section_copy['sectionId'] = self.sectionId

        response = self.request_put(section_copy, "/" + str(self.sectionId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.sectionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(section_copy['name'], response.json['name'])
        self.assertEqual(section_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(section_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.sectionId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)