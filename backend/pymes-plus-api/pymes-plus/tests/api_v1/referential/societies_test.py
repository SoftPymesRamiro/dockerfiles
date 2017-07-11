#!/usr/bin/env python
# -*- coding: utf-8 -*
# ########################################################
# TEST Referential
#
# Date: 19-08-2016
# ########################################################
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
This Class is a Test Case for Society API class
"""
class SocietyTest(unittest.TestCase):
    """
    This Class is a Test Case for Society API class
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
        self.token = json.loads(self.response.data.decode("utf-8"))['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/societies# with societies data values

        :param data: societies data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/societies'+path,
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers=self.headers)

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/societies# with societies data values

        :param data: societies data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/societies'+path,
                                     data=json.dumps(data),
                                     content_type='application/json',
                                     headers=self.headers)

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/societies# with societies data values

        :param data: societies data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/societies'+path,
                                    data=json.dumps(data),
                                    content_type='application/json',
                                    headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/societies# with societies data values

        :param data: societies data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/societies'+path,
                                       data=json.dumps(data),
                                       content_type='application/json',
                                       headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_societies(self):
        """
        This function test get all societies
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        self.assertEqual(response.status_code, 405, 'OK')

    def test_get_society(self):
        """
        This function test get a societies according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?simple=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn('data', response.json)

        self.society = response.json["data"][0]

        response = self.request_get("", "/"+str(self.society['societyId']))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertNotIn('data', response.json)
        self.assertIn("code", response.json)
        self.assertIn("name", response.json)
        self.assertIn("createdBy", response.json)
        self.assertIn('puc', response.json)

        response = self.request_get("", "/9877745")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 404, 'OK')
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_search_societies(self):
        """
        This function test search a societies according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?simple=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn('data', response.json)

        self.assertIn("code", response.json['data'][0])
        self.assertIn("name", response.json['data'][0])
        self.assertIn("societyId", response.json['data'][0])

        # No Parameters, should return all!
        response = self.request_get("", "/search")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200, 'OK')
        self.assertIn('data', response.json)

        self.assertIn("code", response.json['data'][0])
        self.assertIn("name", response.json['data'][0])
        self.assertIn("societyId", response.json['data'][0])
        self.assertIn('puc', response.json['data'][0])

        # ?search=ANONIMA
        # No Parameters
        response = self.request_get("", "/search?search=anonima")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200, 'OK')

        self.assertIn('data', response.json)
        self.assertIn("puc", response.json['data'][0])

        # No Parameters
        response = self.request_get("", "/search?search=aaaaaaaaaaaaaaaaaa")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 404, 'Dont Found')

    def test_create_update_delete_societies(self):
        """

        Returns: This function will create a row, find it , updated and deleted

        """
        data = {
            "puc": {
                "account": "311505005 CUOTAS O PARTES DE INTERES SOCIAL",
                "name": "CUOTAS O PARTES DE INTERES SOCIAL",
                "percentage": 0,
                "pucId": 1977
            },
            "code": "AD",
            "name": "TEST",
            "pucId": 1977
        }

        # *********************** POST *************************
        # Test new Provider Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        # Assign the Id of saved object.
        self.assertEqual(response.status_code, 200, 'OK')
        self.assertIn('societyId', response.json)
        self.societyId = response.json['societyId']

        # Test save POST again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'Code already exist')

        # ********************* GET **************************

        response = self.request_get('', '/' + str(self.societyId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("code" in response.json)
        self.assertEqual(data['code'], response.json['code'])

        # ********************* PUT **************************

        data_2 = copy.deepcopy(response.json)
        data_2['name'] = 'I'

        response = self.request_put(data_2, '/' + str(data_2['societyId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Don't Match Id
        response = self.request_put(data_2, '/10000')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)

        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.societyId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)


