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


from app import create_app
from app.api_v1 import api
import copy
"""
This Class is a Test Case for SubInventoryGroups3 API class
"""
class SubInventoryGroups3Test(unittest.TestCase):
    """
    This Class is a Test Case for SubInventoryGroups1 API class
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
        """Sent get request to #/api/v1/subInventoryGroups3# with subInventoryGroups3 data values

        :param data: SubInventory Group data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sub_inventory_groups_3'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/sub_inventory_groups_3# with sub_inventory_groups_3 data values

        :param data: SubInventory Group data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sub_inventory_groups_3'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/sub_inventory_groups_3# with sub_inventory_groups_3 data values

        :param data: SubInventory Group data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sub_inventory_groups_3'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/sub_inventory_groups_3# with sub_inventory_groups_3 data values

        :param data: SubInventory Group data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sub_inventory_groups_3'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_subInventoryGroups3(self):
        """
        This function test get all subInventoryGroups3
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        # print("#"*10, response.json)


    def test_get_size_subInventoryGroup3(self):
        """
        This function test get a subInventoryGroups3 according a identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.sub_inventory = response.json['data'][0]

        response = self.request_get("","/"+str(self.sub_inventory['subInventoryGroup3Id']))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("code" in response.json)
        self.assertTrue("creationDate" in response.json)
        self.assertTrue("commission" in response.json)
        self.assertTrue("discountPercentage" in response.json)

        response = self.request_get("", "/9999")
        response.json = json.loads(response.data.decode("utf-8"))
        
    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a sub inventory group
         ** First test create with bad sub inventory group data
         ** Second test create with correct sub inventory group data
         ** Third test update sub inventory group
         ** Fourth test delete sub inventory group
        """
        sub_inventory_data = {
            'code': '0098',
            'subInventoryGroup2Id': 1,
            'discountPercentage': 0.0,
            'commission': 0.0,
            'name': 'TEST SUB 3',
            'isDeleted': 0
        }

        response = self.request_post(sub_inventory_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("subInventoryGroup3Id", response.json)
        self.subInventoryGroup3Id = response.json['subInventoryGroup3Id']

        response = self.request_get("", "/" + str(self.subInventoryGroup3Id))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('code', response.json)
        self.assertIn('discountPercentage', response.json)
        self.assertIn('commission', response.json)

        # *********************UPDATE*************************
        sub_inventory_copy = copy.deepcopy(sub_inventory_data)
        sub_inventory_copy['name'] = "TEST GROUP2 UPDATE"
        sub_inventory_copy['isDeleted'] = 1
        sub_inventory_copy['code'] = "099"
        sub_inventory_copy['subInventoryGroup3Id'] = self.subInventoryGroup3Id

        response = self.request_put(sub_inventory_copy, "/" + str(self.subInventoryGroup3Id))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.subInventoryGroup3Id))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(sub_inventory_copy['name'], response.json['name'])
        self.assertEqual(sub_inventory_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(sub_inventory_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.subInventoryGroup3Id))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)