#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST payroll
#
# Date: 11-08-2016
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
This class is a Test Case from Payroll Entity API Class
"""

class PayrollEntitiesTest(unittest.TestCase):
    """
    This class is a Test Case from Payroll Entity API Class
    """
    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
                             password='Admin*2')  # valid data by access to SoftPymes plus

        app = Flask(__name__)
        self.app = create_app(app)
        self.test_client = self.app.test_client(self)
        self.test_client.testing = False

        # Get token access
        self.response = self.test_client.post('/oauth/token', data=json.dumps(self.userdata),
                                              content_type='application/json')

        # User token
        self.token = json.loads(self.response.data.decode('utf-8'))['token']
        self.headers = {'Authorization': 'bearer {token}'.format(token=self.token)}

        # Get Third Party has Payroll Entity

    # ############################### REQUEST FUNCTIONS ##################################
    def request_get(self, data, path='/'):
        """Sent get request to #/api/v1/payroll_entities# with payroll entity data values

        :param data: payroll_entity data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('api/v1/payroll_entities'+path,
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers=self.headers)

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/payroll_entities# with payroll entity data values

        :param data: Payroll Entity data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/payroll_entities' + path,
                                     data=json.dumps(data),
                                     content_type='application/json',
                                     headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/payroll_entities# with PayrollEntity data values

        :param data: PayrollEntity data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/payroll_entities' + path,
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent put request to #/api/v1/payroll_entities# with PayrollEntity data values

        :param data: PayrollEntity data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/payroll_entities' + path,
                                       data=json.dumps(data),
                                       content_type='application/json',
                                       headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_payroll_entities(self):
        """
        **Validate first row in table
        **Validate main fileds
        **Validate incorrect Index
        **Validate No Numbers Id
        Returns: This Function test get all payrollentities
        """
        response = self.request_get('', '/1')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("address1" in response.json)
        self.assertTrue("arp" in response.json)
        self.assertTrue("ccf" in response.json)
        self.assertTrue("afp" in response.json)
        self.assertTrue("cityId" in response.json)
        self.assertTrue("createdBy" in response.json)
        self.assertTrue("creationDate" in response.json)
        self.assertTrue("eps" in response.json)
        self.assertTrue("nationalCode" in response.json)
        self.assertTrue("thirdPartyId" in response.json)

        self.assertIsNotNone(response.json['thirdPartyId'])
        self.assertIsNotNone(response.json['nationalCode'])
        self.assertIsNotNone(response.json['cityId'])

        response = self.request_get('', '/1000000')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found')
        self.assertEqual('NOT FOUND', response.json['message'].upper(), 'Not Found')

        response = self.request_get('', '/AA')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(404, response.json['status'], 404)
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'NOT FOUND')
        self.assertEqual('invalid resource URI', response.json['message'], 'invalid resource URI')

    def test_search_unique_national_code_payroll_entity(self):
        """
        Returns: Return if the NationalCode already exist on DB by another Third
        """

        data = {'national_code': '01'}
        response = self.request_get('', '/search?national_code=' + str(data['national_code']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'OK')
        self.assertTrue("name" in response.json)
        self.assertTrue("nationalCode" in response.json)
        self.assertTrue("payrollEntityId" in response.json)
        self.assertTrue("thirdPartyId" in response.json)

        self.assertEqual(response.json['nationalCode'], data['national_code'])

    def test_search_by_third_party_payroll_entity(self):
        """
        Returns: Search by ThirdParty related PayrollEntities
        """
        # First Search the first PayrollEntity and get the Third Party
        response = self.request_get('', '/search?national_code=01')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'OK')
        self.thirdPartyId = response.json['thirdPartyId']

        # Get Payroll Entities by thirdPartyId
        response = self.request_get('', '/search?third_party_id=' + str(self.thirdPartyId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'OK')
        self.assertTrue("list_payroll_entities" in response.json)

        # Get Payroll Entities by thirdPartyId
        response = self.request_get('', '/search')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404, 'No Parameters')

    def test_unique_sena_and_icbf_payroll_entities(self):
        """
        **api/v1/payroll_entities/search?by_param=SENA&payrollEntityId=
        Returns: Search payroll entities by params SENA and ICBF, are unique in database
        """
        # *********************** SENA ********************
        response = self.request_get('', '/search?by_param=SENA&payrollEntityId=')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("data", response.json)
        self.assertEqual(len(response.json['data']), 1)
        payrollEntityId = response.json['data'][0]['payrollEntityId']

        # Search except himself
        response = self.request_get('', '/search?by_param=SENA&payrollEntityId=' + str(payrollEntityId))
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertIn('data', response.json)
        self.assertEqual(len(response.json['data']), 0)

        # *********************** ICBF ********************
        response = self.request_get('', '/search?by_param=ICBF&payrollEntityId=')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("data", response.json)
        self.assertEqual(len(response.json['data']), 1)
        payrollEntityId = response.json['data'][0]['payrollEntityId']

        # Search except himself
        response = self.request_get('', '/search?by_param=ICBF&payrollEntityId=' + str(payrollEntityId))
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertIn('data', response.json)
        self.assertEqual(len(response.json['data']), 0)

    def test_create_update_delete_payroll_entities(self):
        """
        **
        Returns: This function will create a row, updated and deleted.
        """

        data = {
          "address1": "CLLE 12 NO. 65-11",
          "afp": False,
          "arp": False,
          "ccf": False,
          "cityId": 418,
          "contactList": [
            {
              "createdBy": "ADA LUZ LEGUIZAMON FUENTES",
              "creationDate": "Tue, 11 Feb 2014 12:55:33 GMT",
              "email1": "iamramiroo@gmail.com",
              "extension1": "1",
              "lastName": "BEDOYA",
              "name": "RAMIRO ANDRES",
              "phone1": "3753001",
              "phone2": "3168316297",
              "updateBy": "USER",
              "updateDate": "Wed, 10 Aug 2016 15:48:41 GMT"
            }
          ],
          "createdBy": "ADA LUZ LEGUIZAMON FUENTES",
          "creationDate": "Tue, 11 Feb 2014 12:55:33 GMT",
          "eps": False,
          "icbf": False,
          "isDeleted": False,
          "layoffFund": True,
          "nationalCode": "115",
          "phone": "4143739",
          "sena": False,
          "state": "A",
          "thirdPartyId": 1761,
          "updateBy": "USER",
          "updateDate": "Wed, 10 Aug 2016 15:48:41 GMT",
          "zipCode": "57"
        }

        # *********************** POST *************************
        # Test Normal Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id for the rest of the TESTs
        self.assertEqual(response.status_code, 200, 'National Code ya existe en la Base de datos')
        self.payrollEntityId = response.json['payrollEntityId']

        # Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'National code already exist')

        # Error sending a Contact Already Saved
        fake_data = copy.deepcopy(data)

        fake_data['nationalCode'] = '436'
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

        response = self.request_get('', '/' + str(self.payrollEntityId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("nationalCode" in response.json)
        self.assertEqual(data['nationalCode'], response.json['nationalCode'])

        # ********************* PUT **************************
        data_2 = copy.deepcopy(response.json)
        data_2['state'] = 'I'
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
        response = self.request_put(data_2, '/' + str(data_2['payrollEntityId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Don't Match Id
        response = self.request_put(data_2, '/10000')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)

        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.payrollEntityId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)










































