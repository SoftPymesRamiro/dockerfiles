#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 18-10-2016
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
This Class is a Test Case for Dependencies API class
"""
class DianFormTest(unittest.TestCase):
    """
    This Class is a Test Case for Dependencies API class
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
        """Sent get request to #/api/v1/dian_forms# with dian_forms data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/dian_forms'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/dian_forms# with dian_forms data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/dian_forms'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/dian_forms# with dian_forms data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/dian_forms'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/dian_forms# with dian_forms data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/dian_forms'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_dian_forms(self):
        """
        This function test get all dian_forms
        ** First validate that contains the data key and content
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        self.dian_forms = response.json['data'][0]

        response = self.request_get("", "/"+str(self.dian_forms['dianFormId'])) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        self.assertIn('code', response.json)
        self.assertIn('companyId', response.json)
        self.assertIn('dianConcepts', response.json)
        self.assertIn('dianFormId', response.json)
        self.assertIn('name', response.json)
        self.assertIn('version', response.json)

        response = self.request_get("", "/"+str(999999)) # envio el request al servidor
        response.json = json.loads( response.data.decode("utf-8") ) # convierto a json object

        response = self.request_get("","/search?search=&company_id=1")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])

        response = self.request_get("","/search?paginate=True&company_id=1&page_size=10&page_number=1&search=")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("listForms" in response.json)
        self.assertIsNotNone(response.json['listForms'])

        response = self.request_get("","/search?simple=true&code="+str(self.dian_forms['code'])+"&company_id="+str(self.dian_forms['companyId']))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertIn('code', response.json)
        self.assertIn('companyId', response.json)
        self.assertIn('dianConcepts', response.json)
        self.assertIn('dianFormId', response.json)
        self.assertIn('name', response.json)
        self.assertIn('version', response.json)

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a dian_forms
         ** First test create with bad dian_forms data
         ** Second test create with correct dian_forms data
         ** Third test update dian_forms
         ** Fourth test delete dian_forms
        """
        dian_form_data ={
          "code": "0999",
          "companyId": 1,
          "dianConcepts": [
            {
              "code": "0999",
              "dianformconcepts": [
                {
                  "identificationSource": "M",
                  "isDeleted": 0,
                  "pucId": 2779,
                  "value1Source": "C"
                }
              ],
              "isDeleted": 0,
              "minimumValue": 999,
              "name": "PRUEBA POR INTERESES Y RENDIMIENTOS FINANCIEROS"
            }
          ],
          "isDeleted": 0,
          "name": "PRUEBA - CONSORCIOS",
          "version": "7"
        }

        response = self.request_post(dian_form_data)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("dianFormId", response.json)
        self.dianFormId = response.json['dianFormId']

        response = self.request_post(dian_form_data)

        response = self.request_get("", "/" + str(self.dianFormId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn('code', response.json)
        self.assertIn('companyId', response.json)
        self.assertIn('dianConcepts', response.json)
        self.assertIn('dianFormId', response.json)
        self.assertIn('name', response.json)
        self.assertIn('version', response.json)

        # *********************UPDATE*************************
        dian_form_copy = copy.deepcopy(dian_form_data)
        dian_form_copy['name'] = "PRUEBA CONSORCIOS UPDate"
        dian_form_copy['dianFormId'] = 9999
        response = self.request_put(dian_form_copy, "/" + str(self.dianFormId))

        response = self.request_put(dian_form_copy, "/" + str(9999))

        dian_form_copy['dianFormId'] = self.dianFormId

        response = self.request_put(dian_form_copy, "/" + str(self.dianFormId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        dian_form_copy['code'] = str(9999)
        response = self.request_put(dian_form_copy, "/" + str(self.dianFormId))


        response = self.request_get("", "/" + str(self.dianFormId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(dian_form_copy['name'], response.json['name'])

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.dianFormId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(9999999))  # envio el request al server