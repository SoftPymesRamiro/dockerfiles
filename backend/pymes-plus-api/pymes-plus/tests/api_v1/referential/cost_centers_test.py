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
import copy
import logging


from app import create_app
from app.api_v1 import api

"""
This module shows various methods and function by allow
handled Cost Center
"""
class CostCenterTest(unittest.TestCase):
    """
    This Class is a Test Case for Cost Center API class
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
        """Sent get request to #/api/v1/costCenters# with costCenters data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/costCenters'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/costCenters# with costCenters data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/costCenters'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/costCenters# with costCenters data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/costCenters'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/costCenters# with costCenters data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/costCenters'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_cost_centers(self):
        """
        This function test get all cost centers
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

    def test_get_cost_center_branch(self):
        """
        This function test get a color according to branch identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/branch/14")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json, 'incorrect response by correct request')

        response = self.request_get("", "/branch/9148974")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 404, 'Not Found')
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')




    def test_get_cost_center(self):
        """
        This function test get a color according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/9")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("code" in response.json, 'incorrect response by correct request')
        self.assertTrue("divisions" in response.json, 'incorrect response by correct request')
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request')
        self.assertTrue("name" in response.json, 'incorrect response by correct request')

        response = self.request_get("", "/9148974")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 404, 'Not Found')

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a cost_Centers
         ** First test create with bad cost-center data
         ** Second test create with correct cost-center data
         ** Third test update cost-center
         ** Fourth test delete cost-center
        """
        cost_center_data={
            'branchId': 4,
            'divisions': [
                {
                    'isDeleted': 0,
                    'sections': [
                        {
                            'divisionId': 6,
                            'isDeleted': 0,
                            'sectionId': 6,
                            'dependencies': [
                                {
                                    'pucId': None,
                                    'code': '00001',
                                    'dependencyId': 2,
                                    'puc': None,
                                    'name': 'TEST DEP',
                                    'isDeleted': 0,
                                }
                            ],
                            'pucId': None,
                            'code': '00001',
                            'name': 'ASDA',
                            'puc': None
                        }
                    ],
                    'pucId': 21211,
                    'code': '00001',
                    'name': 'CENTRO',
                    'puc': {
                        'percentage': 0.0,
                        'account': '510000000 GASTOS - OPERACIONALES DE ADMINISTRACION',
                        'pucId': 21211
                    }
                }
            ],
            'code': '0099',
            'name': 'TEST COSTCENTER',
            'isDeleted': 0
        }

        response = self.request_post(cost_center_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("costCenterId", response.json)
        self.costCenterId = response.json['costCenterId']

        response = self.request_get("", "/" + str(self.costCenterId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('code', response.json)
        self.assertIn('name', response.json)
        self.assertIn('branchId', response.json)

        # *********************UPDATE*************************
        brand_copy = copy.deepcopy(cost_center_data)
        brand_copy['code'] = "9999"
        brand_copy['isDeleted'] = 1
        brand_copy['name'] = "TEST COSTCENTER UPDATE"
        brand_copy['costCenterId'] = self.costCenterId
        brand_copy['updateDate'] = response.json['updateDate']

        response = self.request_put(brand_copy, "/" + str(self.costCenterId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.costCenterId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(brand_copy['name'], response.json['name'])
        self.assertEqual(brand_copy['code'], response.json['code'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.costCenterId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)