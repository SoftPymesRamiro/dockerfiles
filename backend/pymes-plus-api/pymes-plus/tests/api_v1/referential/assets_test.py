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
handled asset
"""
class AssetTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/asset# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/assets'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/asset# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/assets'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/asset# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/assets'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/asset# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/assets'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_asset(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?search=A&branch_id=14") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self.asset = response.json['data'][0]

        response = self.request_get("", "/"+str(self.asset['assetId'])) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        # validate keys in response
        self.assertTrue("puc" in response.json, 'incorrect response by correct request' )
        self.assertTrue("address" in response.json, 'incorrect response by correct request' )
        self.assertTrue("name" in response.json, 'incorrect response by correct request' )
        self.assertTrue("state" in response.json, 'incorrect response by correct request' )
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request' )

        response = self.request_get("","/9148974")# envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_get_asset_search(self):
        """
        This function allow search asset
         ** First test
         ** Second test
        """
        response = self.request_get("", "/search?search=A&branch_id=14") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio

        self.code = response.json['data'][0]['code']

        response = self.request_get("", "/search?search=A&branch_id=14877787")
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertEqual(response.json['data'], [], 'incorrect')

        response = self.request_get("", "/search?simple=1&branch_id=14")
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate keys in response
        self.assertTrue("puc" in response.json, 'incorrect response by correct request')
        self.assertTrue("address" in response.json, 'incorrect response by correct request')
        self.assertTrue("name" in response.json, 'incorrect response by correct request')
        self.assertTrue("state" in response.json, 'incorrect response by correct request')
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request')

        response = self.request_get("", "/search?simple=1&branch_id=14445")
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_get("", "/search?simple=1&branch_id=14&code="+self.code)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate keys in response
        self.assertTrue("puc" in response.json, 'incorrect response by correct request')
        self.assertTrue("address" in response.json, 'incorrect response by correct request')
        self.assertTrue("name" in response.json, 'incorrect response by correct request')
        self.assertTrue("state" in response.json, 'incorrect response by correct request')
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request')

        response = self.request_get("", "/search?simple=1&branch_id=14&code=775")
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_get("", "/search?search=A")
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')



    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a asset
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        asset={
            'dependencyId': None,
            'notarialDocument': None,
            'netValueNIIF': None,
            'imageId': 197,
            'purchaseDate': 'Mon, 22 Aug 2016 22:50:23 GMT',
            'landArea': None,
            'isDeleted': None,
            'builtArea': None,
            'code': '0099',
            'puc': {
                'account': '105505005',
                'pucId': 84769,
                'name': 'URBANOS'
            },
            'divisionId': 13,
            'updateBy': 'ADMINISTRADORAA del Sistema',
            'state': 'A',
            'sectionId': None,
            'rentable': False,
            'name': 'TEST ASSET',
            'line': None,
            'pucId': 84769,
            'dateNotarialDocument': 'Mon, 22 Aug 2016 22:50:23 GMT',
            'costHour': None,
            'comments': 'PRBACT.FIXED\nPRBACT.FIXED',
            'cityId': 146,
            'depreciationYearNIIF': 0,
            'createdBy': 'ADMINISTRADORAA del Sistema',
            # 'assetId': 36,
            'plate': None,
            'responsible': None,
            'branchId': 14,
            'chassisSerial': None,
            'depreciationMonthNIIF': 0,
            'model': None,
            'propertyNumber': None,
            'notary': None,
            'percentageSaving': 0.0,
            'creationDate': 'Mon, 22 Aug 2016 17:50:50 GMT',
            'assetGroupId': None,
            'costCenterId': 4,
            'city': {
                'cityId': 146,
                'department': {
                    'departmentId': 4,
                    'name': 'BOLIVAR',
                    'code': '13',
                    'country': {
                        'indicative': '57',
                        'countryId': 2
                    }
                },
                'name': 'CALAMAR - BOLIVAR - COLOMBIA',
                'indicative': '5',
                'code': '140'
            },
            'address': 'PRBACT.FIXED 46546',
            'updateDate': 'Mon, 22 Aug 2016 17:50:50 GMT',
            'logoConvert': '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',
            'engineSerial': None,
            'percentageResidual': 0.0,
            'depreciationMonth': 0,
            'depreciationYear': 0,
            'typeAsset': 'I'
        }
        #
        response = self.request_post(asset)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("assetId", response.json)
        self.assetId = response.json['assetId']

        response = self.request_get("", "/"+str(self.assetId)) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("puc" in response.json, 'incorrect response by correct request' )
        self.assertTrue("address" in response.json, 'incorrect response by correct request' )
        self.assertTrue("name" in response.json, 'incorrect response by correct request' )
        self.assertTrue("state" in response.json, 'incorrect response by correct request' )
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request' )
        self.assertEqual(response.json['code'], "0099")
        self.assertEqual(response.json['name'], 'TEST ASSET')

        # *********************UPDATE*************************
        asset_copy = copy.deepcopy(asset)
        asset_copy['name'] = "TEST ASSET UPDATE"
        asset_copy['assetId'] = self.assetId

        response = self.request_post(asset_copy)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_put(asset_copy,"/"+str(self.assetId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/"+str(self.assetId)) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertTrue("puc" in response.json, 'incorrect response by correct request' )
        self.assertTrue("address" in response.json, 'incorrect response by correct request' )
        self.assertTrue("name" in response.json, 'incorrect response by correct request' )
        self.assertTrue("state" in response.json, 'incorrect response by correct request' )
        self.assertTrue("branchId" in response.json, 'incorrect response by correct request' )
        self.assertEqual(response.json['code'], "0099")
        self.assertNotEqual(response.json['name'], 'TEST ASSET')
        self.assertEqual(response.json['name'], 'TEST ASSET UPDATE')
        #
        # *********************DELETE*************************
        response = self.request_delete("", "/9999")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.assetId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
