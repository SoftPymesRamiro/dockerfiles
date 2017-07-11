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
This Class is a Test Case for Warehouses API class
"""
class WarehousesTest(unittest.TestCase):
    """
    This Class is a Test Case for Warehouses API class
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
        """Sent get request to #/api/v1/warehouses# with Warehouses data values

        :param data: Warehouses data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/warehouses'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/warehouses# with Warehouses data values

        :param data: Warehouses data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/warehouses'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/warehouses# with Warehouses data values

        :param data: Warehouses data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/warehouses'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/warehouses# with Warehouses data values

        :param data: Warehouses data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/warehouses'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_warehouses(self):
        """
        This function test get all warehouses
        ** First validate that contains the data key and content
        """

        response = self.request_get("")

        self.assertEqual("405 METHOD NOT ALLOWED", response.status, " No implementado ")

        response = self.request_get("", "/1")
        response.json = json.loads(response.data.decode("utf-8") )

        self.assertIn("branchId", response.json)
        self.assertIn("code", response.json)

        self.assertIn("customer", response.json)
        self.assertIn("name", response.json)
        self.assertIn("provider", response.json)
        self.assertIn("typeWarehouse", response.json)
        self.assertIn("warehouseId", response.json)

        self.assertEqual(response.json['warehouseId'], 1)

    def test_get_warehouse(self):
        """
        This function test get a size according to company identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/1")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("branchId" in response.json)
        self.assertTrue("typeWarehouse" in response.json)
        self.assertTrue("name" in response.json)
        self.assertTrue("provider" in response.json)
        
        # print("#"*10, response.json)
        

    def test_search_warehouses(self):
        """
        Allow  test search size according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # api/v1/warehouses/search?branch_id=14&simple=True

        response = self.request_get("", "/search?simple=1&branch_id=4")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertTrue("typeWarehouse" in response.json["data"][0])
        self.assertTrue("name" in response.json["data"][0])
        self.assertTrue("code" in response.json["data"][0])
        self.assertNotIn("createdBy", response.json["data"][0])

        # api/v1/warehouses/search?branch_id=14

        response = self.request_get("", "/search?branch_id=4")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertTrue("typeWarehouse" in response.json["data"][0])
        self.assertTrue("name" in response.json["data"][0])
        self.assertTrue("code" in response.json["data"][0])
        self.assertTrue("createdBy" in response.json["data"][0])

        response = self.request_get("", "/search?branch_id=10000")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 404, 'Sin Registros')

        # api/v1/warehouses/search?search=LEGA&branch_id=14
        response = self.request_get("", "/search?search=LEGA&branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertTrue("typeWarehouse" in response.json["data"][0])
        self.assertTrue("name" in response.json["data"][0])
        self.assertTrue("code" in response.json["data"][0])
        self.assertTrue("createdBy" in response.json["data"][0])
        self.assertTrue("002", response.json["data"][0])

    def test_create_update_delete_warehouses(self):
        """
        Returns: This function will create a row, updated and deleted.
        """

        data = {
            "branchId": 14,
            "code": "032",
            "name": "BODEGA DE PRUEBA",
            "typeWarehouse": "P"
        }

        # *********************** POST *************************
        # Test Normal Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id for the rest of the TESTs
        self.assertEqual(response.status_code, 200, 'Guardado')
        self.assertIn("warehouseId", response.json)
        self.warehouseId = response.json['warehouseId']

        # Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'Warehouse code already exist')


        # ********************* GET **************************

        response = self.request_get('', '/' + str(self.warehouseId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("code" in response.json)
        self.assertEqual(data['code'], response.json['code'])

        data_2 = copy.deepcopy(response.json)

        # Send To POST Again
        response = self.request_post(response.json, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'El Valor por defecto ya existe')

        # ********************* PUT **************************

        data_2['name'] = 'CHAO'
        response = self.request_put(data_2, '/' + str(data_2['warehouseId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Don't Match Id
        response = self.request_put(data_2, '/10000')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)

        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.warehouseId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("message", response.json)
        self.assertEqual(response.json['message'], 'Eliminado correctamente')

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)
        