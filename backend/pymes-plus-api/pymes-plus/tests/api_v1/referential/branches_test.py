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

"""
This module shows various methods and function by allow
handled branches
"""
class BranchesTest(unittest.TestCase):
    """
    This Class is a  Test Case for Branch Api class
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
        """Sent get request to #/api/v1/branches# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/branches'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/branches# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/branches'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/branches# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/branches'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/branches# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/branches'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_branches(self):
        """
        This function test get all branches
        ** first validate that contains the data key and content
        """
        response = self.request_get("") # request to server
        response.json = json.loads( response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio



    def test_get_branch(self):
        """
        This function test get a branch according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/22") # envio el request al server
        response.json = json.loads( response.data.decode("utf-8") ) # convert to json object
        # validate keys in response
        self.assertTrue("cityId" in response.json, 'incorrect response by correct request' )


        response = self.request_get("","/9148974") # envio el request al server
        response.json = json.loads( response.data.decode("utf-8") ) # convert to json object
        # validate No found response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

        response = self.request_get("", "/dasdasd") # envio el request al server
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object
        # validate keys in response
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')



    def test_get_branch_search(self):
        """
        This function allow search branches
         ** First test
         ** Second test
         ** Third test
         ** Fourth test
        """
        response = self.request_get("","/search?branch_id=22&to_purchase=1") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertTrue("branchId" in response.json, 'incorrect response by correct request' )
        self.assertTrue("zipCode" in response.json, 'incorrect response by correct request' )
        self.assertTrue("cityName" in response.json, 'incorrect response by correct request' )


        response = self.request_get("", "/search?branch_id=4542") ## OJO SI SE ACTIVA PURSHASE IGUAL RETORNA
        response.json = json.loads(response.data.decode("utf-8") ) # convert to json object

        self.assertEqual(response.json['data'], [], 'incorrect')


        response = self.request_get("","/search?branch_id=4542&to_purchase=1") ## OJO SI SE ACTIVA PURSHASE IGUAL RETORNA
        response.json = json.loads( response.data.decode("utf-8") ) # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')


    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a branches
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        branch_data ={
            'companyId': 4,
            'phone2': None,
            'address1': 'Cra 32 # 90-67',
            'icaRate4': 0.0,
            'isDeleted': 0,
            'icaActivity2': None,
            'phone3': None,
            'icaRate5': 0.0,
            'name': 'SUCURSAL TEST',
            'icaActivity1': None,
            'company': {
                'identificationNumber': '1144077005',
                'companyId': 4,
                'identificationDV': '1',
                'name': 'YEFFCOMPANY',
                'code': '004'
            },
            'email': 'branchtest@branchtest.com',
            'fax': None,
            'icaActivity5': None,
            'code': '001',
            'zipCode': '321654',
            'icaRate3': 0.0,
            'cityId': 822,
            'icaActivity4': None,
            'icaRate1': 0.0,
            'phone1': '3214758',
            'icaRate2': 0.0,
            'economicActivityId': 10,
            'icaActivity3': None,
            'withholdingCREEPUCId': 102582,
            'address2': None,
            'motionDate': '2015-07-07'
        }

        response = self.request_post(branch_data)
        print(">>>>> ", response)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("branchId", response.json)
        self.branchId = response.json['branchId']

        response = self.request_get("", "/"+str(self.branchId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('address1', response.json)
        self.assertIn('phone3', response.json)
        self.assertIn('phone2', response.json)
        self.assertIn('phone1', response.json)
        self.assertIn('zipCode', response.json)
        self.assertIn('fax', response.json)

        # *********************UPDATE*************************
        branchdata_copy = copy.deepcopy(branch_data)
        branchdata_copy['address1'] = "Cra 123-123"
        branchdata_copy['phone3'] = "(057) 5555-89778"
        branchdata_copy['phone2'] = "(520) 888 444-555"
        branchdata_copy['phone1'] = "(032) 888 4998"
        branchdata_copy['zipCode'] = "760589"
        branchdata_copy['fax'] = "12323-44432144-78"
        branchdata_copy['branchId'] = self.branchId

        response = self.request_put(branchdata_copy,"/"+str(self.branchId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/"+str(self.branchId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(branchdata_copy['address1'], response.json['address1'])
        self.assertEqual(branchdata_copy['phone3'], response.json['phone3'])
        self.assertEqual(branchdata_copy['phone2'], response.json['phone2'])
        self.assertEqual(branchdata_copy['phone1'], response.json['phone1'])
        self.assertEqual(branchdata_copy['zipCode'], response.json['zipCode'])
        self.assertEqual(branchdata_copy['fax'], response.json['fax'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.branchId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
