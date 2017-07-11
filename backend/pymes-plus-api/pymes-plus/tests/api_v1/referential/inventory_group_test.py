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
This Class is a Test Case for Inventory Group API class
"""
class InventoryGroup(unittest.TestCase):
    """
    This Class is a Test Case for Inventory Group API class
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
        """Sent get request to #/api/v1/inventory_group# with inventory-group data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/inventory_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/inventory_groups# with inventory-group data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/inventory_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/inventory_groups# with inventory-group data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/inventory_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/inventory_groups# with inventory-group data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/inventory_groups'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_inventory_groups(self):
        """
        This function test get all inventory_groups
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])


    def test_get_inventory_group(self):
        """
        This function test get a inventory_groups according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8"))

        inventory_group = response.json['data'][0]
        response = self.request_get("", "/"+str(inventory_group['inventoryGroupId']))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("name" in response.json)
        self.assertTrue("code" in response.json)
        self.assertTrue("createdBy" in response.json)
        self.assertTrue("creationDate" in response.json)
        self.assertTrue("subInventoryGroups1" in response.json)

        response = self.request_get("", "/18777")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')


    def test_search_inventory_group(self):
        """
        This function test search a inventory_groups according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/search?company_id=1")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json, 'incorrect response by correct request' )


        response = self.request_get("", "/search?company_id=34")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a inventory_group
         ** First test create with bad inventory_group data
         ** Second test create with correct inventory_group data
         ** Third test update inventory_group
         ** Fourth test delete inventory_group
        """

        inventory_group = {
          'code': '0098',
          'commission': 0.0,
          'discountPercentage': 0.0,
          'name': 'TEST GROUP',
          'companyId': 4,
          'isDeleted': 0
        }

        response = self.request_post(inventory_group)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("inventoryGroupId", response.json)
        self.inventoryGroupId = response.json['inventoryGroupId']

        response = self.request_get("", "/" + str(self.inventoryGroupId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('name', response.json)
        self.assertIn('inventoryGroupId', response.json)
        self.assertIn('code', response.json)
        self.assertIn('discountPercentage', response.json)
        self.assertIn('commission', response.json)

        # *********************UPDATE*************************
        inventory_copy = copy.deepcopy(inventory_group)
        inventory_copy['name'] = "TEST GROUP UPDATE"
        inventory_copy['code'] = "0099"
        inventory_copy['inventoryGroupId'] = self.inventoryGroupId

        response = self.request_put(inventory_copy, "/" + str(self.inventoryGroupId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.inventoryGroupId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(inventory_copy['name'], response.json['name'])
        self.assertEqual(inventory_copy['isDeleted'], response.json['isDeleted'])
        self.assertEqual(inventory_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.inventoryGroupId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)