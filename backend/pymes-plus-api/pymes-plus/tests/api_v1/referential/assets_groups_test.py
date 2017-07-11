#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
# app
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
import copy
import time
import logging


from app import create_app
from app.api_v1 import api
from datetime import datetime

"""
This module shows various methods and function by allow
handled assets group
"""
class AssetGroupTest(unittest.TestCase):
    """
    This Class is a  Test Case for Asset Group Api class
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
        """Sent get request to #/api/v1/assets group# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/asset_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/assets group# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/asset_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/assets group# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/asset_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/assets group# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/asset_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_asset_group_search(self):
        """
        This function allow search assets group
         ** First test
         ** Second test
        """
        response = self.request_get("", "/search?search=A&branch_id=14") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio

        response = self.request_get("", "/search?search=A&branch_id=188744")
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertEqual(response.json['data'], [], 'incorrect')

        response = self.request_get("", "/search?simple=1&code=995&branch_id=14")  # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_get("", "/search?simple=1&branch_id=14")  # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio

        response = self.request_get("", "/search?simple=1")  # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a assets group
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        asset_group={
            'branchId': 14,
            'name': 'TEST ASSET GROUP',
            'code': '099',
            'isDeleted': 0,
            'companyId': 1
        }
        #
        response = self.request_post(asset_group)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("assetGroupId", response.json)
        self.assetGroupId = response.json['assetGroupId']

        response = self.request_get("", "/search?simple=1&code=099&branch_id=14") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("updateDate" in response.json)
        self.assertTrue("branchId" in response.json)
        self.assertTrue("assetGroupId" in response.json)
        self.assertTrue("name" in response.json)
        self.assertTrue("code" in response.json)
        self.assertEqual(response.json['code'], "099")
        self.assertEqual(response.json['name'], 'TEST ASSET GROUP')

        # *********************UPDATE*************************
        asset_group_copy = copy.deepcopy(asset_group)
        asset_group_copy['name'] = "TEST ASSET GROUP UPDATE"
        asset_group_copy['assetGroupId'] = self.assetGroupId

        response = self.request_post(asset_group_copy)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_put(asset_group_copy,"/"+str(self.assetGroupId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/search?simple=1&code=099&branch_id=14") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("updateDate" in response.json)
        self.assertTrue("branchId" in response.json)
        self.assertTrue("assetGroupId" in response.json)
        self.assertTrue("name" in response.json)
        self.assertTrue("code" in response.json)
        self.assertEqual(response.json['code'], "099")
        self.assertNotEqual(response.json['name'], 'TEST ASSET GROUP')
        self.assertEqual(response.json['name'], 'TEST ASSET GROUP UPDATE')

        # *********************DELETE*************************
        response = self.request_delete("", "/9999")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_delete("", "/" + str(self.assetGroupId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
