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
This Class is a Test Case for Providers API class
"""
class ProvidersTest(unittest.TestCase):
    """
    This Class is a Test Case for Providers API class
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
        """Sent get request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_providers(self):
        """
        This function test get all providers
        ** First validate that contains the data key and content
        """
        response = self.request_get("")

        self.assertEqual("405 METHOD NOT ALLOWED", response.status, " No implementado ")

        # response.json = json.loads( response.data.decode("utf-8") )

        # self.assertTrue("data" in response.json)
        # self.assertIsNotNone(response.json['data'])

    def test_get_provider(self):
        """
        This function test get a providers according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("","/115")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("address1" in response.json)
        self.assertTrue("name" in response.json)
        self.assertTrue("createdBy" in response.json)

        self.assertIsNotNone(response.json['createdBy'])

        response = self.request_get("","/9877745")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertEqual('NOT FOUND', response.json['error'].upper() , 'incorrect response by bad request')

    def test_search_providers(self):
        """
        This function test search a providers according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?simple=1&company_id=1&third_party_id=486")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("branch" in response.json['data'][0])
        self.assertTrue("name" in response.json['data'][0])
        self.assertTrue("state" in response.json['data'][0])

        # self.assertIsNotNone(response.json['data'][0])

    def test_create_update_delete_providers(self):
        """

        Returns: This function will create a row, find it , updated and deleted

        """

        data = {
          "creditCapacity": 1000000,
          "state": "A",
          "term": "12",
          "contactList": [
            {
              "name": "RAMIRO ANDRÉS",
              "lastName": "BEDOYA ESCOBAR",
              "phone1": "3753001",
              "extension1": "123",
              "phone2": "3168316297",
              "email1": "iamramiroo@gmail.com"
            }
          ],
          "changeIsMain": [],
          "branch": "11",
          "isMain": True,
          "name": "NORTE",
          "citySimple": {
            "cityId": 822,
            "cityIndicative": "2",
            "code": "001",
            "countryIndicative": "57",
            "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
          },
          "address1": "CRA 32 # 13 - 50",
          "zipCode": "092",
          "phone": "3173001",
          "cellPhone": "3168316297",
          "cityId": 822,
          "thirdPartyId": 195,
          "companyId": 1
        }

        # *********************** POST *************************
        # Test new Provider Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id of saved object.
        self.assertEqual(response.status_code, 200, 'OK')
        self.assertIn('providerId', response.json)
        self.providerId = response.json['providerId']

        # Test save POST again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'Provider code already exist')

        # Error sending a Contact Already Saved
        fake_data = copy.deepcopy(data)

        fake_data['branch'] = '22'
        fake_data['contactList'].append({
            "contactId": "460",
            "createdBy": "HOLA",
            "creationDate": "Tue, 11 Feb 2014 12:55:33 GMT",
            "email1": "hi@gmail.com",
            "extension1": "1",
            "lastName": "BEDOYA",
            "name": "ANDRES",
            "phone1": "3753001",
            "phone2": "3168316297",
            "updateBy": "USER",
            "updateDate": "Wed, 10 Aug 2016 15:48:41 GMT"
        })
        response = self.request_post(fake_data, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'Bad Request')

        # ********************* GET **************************

        response = self.request_get('', '/' + str(self.providerId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("branch" in response.json)
        self.assertEqual(data['branch'], response.json['branch'])

        # ********************* PUT **************************

        data_2 = copy.deepcopy(response.json)
        data_2['state'] = 'I'
        # IsMain
        data_2['isMain'] = True

        data_2['contactList'].append({
            "createdBy": "HOLA",
            "creationDate": "Tue, 11 Feb 2014 12:55:33 GMT",
            "email1": "hi@gmail.com",
            "extension1": "1",
            "lastName": "BEDOYA",
            "name": "ANDRES",
            "phone1": "3753001",
            "phone2": "3168316297",
            "updateBy": "USER",
            "updateDate": "Wed, 10 Aug 2016 15:48:41 GMT"
        })
        response = self.request_put(data_2, '/' + str(data_2['providerId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Don't Match Id
        response = self.request_put(data_2, '/10000')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)




        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.providerId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)


