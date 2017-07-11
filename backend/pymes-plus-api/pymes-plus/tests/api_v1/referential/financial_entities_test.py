#!/usr/bin/env python
# -*- coding: utf-8 -*
###################################################
# TEST Referential
#
# Date: 11-08-2016
####################################################
__author__ = 'Softpymes'
__credits__ = [""]
__version__ = "1.0.1"

from flask import Flask
import unittest
import json
from copy import *
from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for financial_entities API class
"""

class FinancialEntityTest(unittest.TestCase):
    """
    This Class is a Test Case for FinancialEntity API class
    """

    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
            password='Admin*2')  # valid data by access to SoftPymes plus

        app = Flask(__name__)  # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self)  # test client
        self.test_client.testing = False  # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                                              data=json.dumps(self.userdata),
                                              content_type='application/json')
        # User token
        self.token = json.loads(self.response.data.decode("utf-8"))['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """sent get request to #/api/v1/financial_entities# with financial_entities data values

        :param data:  financial_entities data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/financial_entities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers) # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/financial_entities# with financial_entities data values

        :param data: financial_entities data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict
        """
        return self.test_client.post('/api/v1/financial_entities' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)

    def request_put(self,data,path="/"):
        """Sent post request to #/api/v1/financial_entities# with financial_entities data values

        :param data: financial_entities data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict
        """
        return self.test_client.put('/api/v1/financial_entities'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)

    def request_delete(self,data,path='/'):
        """Sent post request to #/api/v1/financial_entities# with financial_entities data values

        :param data: financial_entities data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/financial_entities'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)

    ############################################################################################################
    def test_get_financial_entities(self):
        """
        This function test get all financial entitites
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertTrue("data" in response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

    def test_get_financial_entityId(self):
        """
        This function test get all financial_entities
        ** First validate that contains the data key and content
        ** validate main fields
        """

        response = self.request_get("", "/1")
        response.json = json.loads( response.data.decode("utf-8"))

        self.assertTrue('address1' in response.json)
        self.assertTrue('createdBy' in response.json)
        self.assertTrue('creationDate' in response.json)
        self.assertTrue('nationalCode' in response.json)
        self.assertTrue('thirdPartyId' in response.json)

        self.assertIsNotNone(response.json['thirdPartyId'])
        self.assertIsNotNone(response.json['nationalCode'])

    # def test_get_financial_entity_by_search(self):
    #     """
    #     This function test get search a financialEntity according to identifier
    #     **first test is correct identifier
    #     **second test is incorrect and validate
    #     """
    #
    #     response = self.request_get("", "/search?simple=1&")
    #     response.json = json.loads( response.data.decode("utf-8"))
    #
    #     self.assertTrue('data' in response.json)
    #     self.assertIsNotNone(response.json['data'])

    def test_post_financial_entity(self):
        """
        This function test will create a financialEntity
        ** First test is correct identifier
        ** second test is incorrect identifier and validate data
        """
        data = {
                "entityType": 1,
                "contactList": [
                    {
                        "name": "ASD",
                        "lastName": "ASD",
                        "phone1": "13",
                        "extension1": "12",
                        "phone2": "12",
                        "email1": ""
                    }
                ],
                "withholdingBase": 0,
                "withholdingICA": 0,
                "comissionPercentage": 0,
                "withholdingTax": 0,
                "withholdingIVA": 0,
                "state": "A",
                "office": "4439",
                "nationalCode": "999",
                "name": "9999",
                "address1": "999",
                "citySimple": {
                    "cityId": 61,
                    "cityIndicative": "4",
                    "code": "678",
                    "countryIndicative": "57",
                    "name": "SAN CARLOS - CÓRDOBA - COLOMBIA"
                },
                "zipCode": "999999",
                "cityId": 61,
                "thirdPartyId": 200,
                "branchId": 14
            }
        #################POST######################################
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id for hte rest of the TESTS
        self.assertEqual(response.status_code, 200, 'OK')
        self.financialEntityId = response.json['financialEntityId']

        data_copy = copy(data)
        data_copy['financialEntityId'] = self.financialEntityId
        data_copy['name'] = 'pachito el che'
        data_copy['zipCode'] = '88888'

        #Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'Office code already exits')

        ############################PUT##################################
        # Capture the data with last financialEntityId
        #data_copy it's contain to want that update
        response = self.request_put(data_copy, '/' + str(self.financialEntityId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("ok" in response.json)


        ############################GET####################################
        # Again have the financialEntityId that so created
        response = self.request_get('', '/' + str(self.financialEntityId))
        response.json = json.loads(response.data.decode('utf-8'))
        # validate the following data
        self.assertIn("contactList", response.json)
        self.assertEqual(response.json['financialEntityId'], self.financialEntityId)
        self.assertEqual(response.json['name'], data_copy['name'])
        self.assertEqual(response.json['zipCode'], data_copy['zipCode'])



        ##########################DELETE##################################
        self.assertEqual(data_copy['financialEntityId'], response.json['financialEntityId'])
        self.assertEqual(data_copy['office'], response.json['office'])

        response = self.request_delete(data_copy, '/' + str(self.financialEntityId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')
        #
        # # Test with invalid id
        # response = self.request_delete('', '/0')
        # self.assertEquals(response.status_code, 404)



