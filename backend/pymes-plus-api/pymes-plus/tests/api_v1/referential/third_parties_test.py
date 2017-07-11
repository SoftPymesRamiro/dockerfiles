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
import copy


from app import create_app
from app.api_v1 import api



"""
This Class is a Test Case for ThirdParties API class
"""
class ThirdPartiesTest(unittest.TestCase):
    """
    This Class is a Test Case for ThirdParties API class
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
        """Sent get request to #/api/v1/third_parties# with third_parties data values

        :param data: third_parties data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/third_parties'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent get request to #/api/v1/third_parties# with third_parties data values

        :param data: third_parties data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/third_parties'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent get request to #/api/v1/third_parties# with third_parties data values

        :param data: third_parties data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/third_parties'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent get request to #/api/v1/third_parties# with third_parties data values

        :param data: third_parties data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/third_parties'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_third_parties(self):
        """
        This function test get all third_parties
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

    def test_get_third_parties_by_id(self):
        """
        This function test get a size according to company identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/2")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("thirdType" in response.json)
        self.assertTrue("identificationTypeId" in response.json)
        self.assertTrue("tradeName" in response.json)
        self.assertTrue("creationDate" in response.json)
        self.assertTrue("retirementDate" in response.json)
        self.assertTrue("isSelfRetainer" in response.json)
        self.assertIsNotNone(response.json['identificationType'])

        response = self.request_get("", "/11111111111111")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 404, 'Not Found')

        self.assertTrue("error" in response.json)
        self.assertEqual("Not Found", response.json['error'])

    def test_get_third_party_by_search(self):
        """
        ** /api/v1/third_parties/search?identification_number=1143838715
        Returns: Returns direct identification Number
        """

        response = self.request_get("", "/search?identification_number=1143838715")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("thirdPartyId" in response.json)
        self.assertEqual(195, response.json['thirdPartyId'])
        self.assertIn("identificationType", response.json)

        response = self.request_get("", "/search?identification_number=1111111111")
        # response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.data, b'')
        self.assertEqual(response.status_code, 200, 'Not Found')

        # With company_id and branch_id
        response = self.request_get("", "/search?identification_number=1143838715&branch_id=14&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("thirdPartyId" in response.json)
        self.assertEqual(195, response.json['thirdPartyId'])
        self.assertIn("identificationType", response.json)
        self.assertIn('typeThird', response.json)

        # Only Search
        # search?search=RAMIRO

        response = self.request_get("", "/search?search=ramirooooo")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)
        self.assertCountEqual(response.json['data'], [])

        # Dont Search Nothing
        response = self.request_get("", "/search")
        # response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.data, b'')
        self.assertEqual(response.status_code, 200, 'Not Found')


    def test_create_update_delete_third_parties(self):
        """
        Returns: This function will create a row, updated and deleted.
        """

        data = {
          "state": "A",
          "identificationTypeId": 1,
          "extranger": [
            {
              "code": "C",
              "createdBy": "Migracion",
              "creationDate": "Fri, 17 Aug 2012 10:34:53 GMT",
              "identificationTypeDian": "13",
              "identificationTypeId": 1,
              "isDeleted": 0,
              "name": "Cedula de Ciudadania",
              "updateBy": "Migracion"
            }
          ],
          "identificationNumber": "1143838788",
          "identificationDV": "0",
          "thirdType": "N",
          "lastName": "APELLIDO",
          "maidenName": "APPELIDO2",
          "firstName": "NOMBRES",
          "webPage": "paginaweb.com",
          "ivaTypeId": 1,
          "economicSimple": {
            "code": "0111",
            "economicActivityId": 2,
            "name": "CULTIVO DE CEREALES (EXCEPTO ARROZ), LEGUMBRES Y SEMILLAS OLEAGINOSAS 0.30"
          },
          "isSelfRetainer": True,
          "isSelfRetainerICA": True,
          "isWithholdingCREE": True,
          "comments": "ASDFASDFASDF",
          "economicActivityId": 2
        }

        # *********************** POST *************************
        # Test Normal Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id for the rest of the TESTs
        self.assertEqual(response.status_code, 200, 'Guardado')
        self.assertIn("id", response.json)
        self.thirdPartyId = response.json['id']

        # Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'ThirdParty code already exist')

        # ********************* GET **************************

        response = self.request_get('', '/' + str(self.thirdPartyId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("identificationNumber" in response.json)
        self.assertEqual(data['identificationNumber'], response.json['identificationNumber'])

        data_2 = copy.deepcopy(response.json)

        # Send To POST Again
        response = self.request_post(response.json, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'ThirdParty code already exist')

        # ********************* PUT **************************

        data_2['firstName'] = 'CHAO'
        response = self.request_put(data_2, '/' + str(data_2['thirdPartyId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("id", response.json)
        self.assertEqual(response.json['id'], data_2['thirdPartyId'])

        self.assertIn("response", response.json)
        self.assertEqual(response.json['response'], 'Tercero actualizado correctamente')

        # Don't Match Id
        response = self.request_put(data_2, '/10000')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)

        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.thirdPartyId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertNotIn("message", response.json)
        self.assertEquals(response.status_code, 200)

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)
