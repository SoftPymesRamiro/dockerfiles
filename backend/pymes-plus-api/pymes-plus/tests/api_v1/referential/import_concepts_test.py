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
from copy import copy

"""
This module shows various methods and function by allow
handled import_concept
"""
class ImportConceptTest(unittest.TestCase):
    """
    This Class is a  Test Case for Import Api class
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
        """Sent get request to #/api/v1/import_concept# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/import_concepts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/import_concept# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/import_concepts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/import_concept# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/import_concepts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/import_concept# with branch data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/import_concepts'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_import_concept_bycompany(self):
        """
        This function test get a import concept according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/company/1")  # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertTrue("data" in response.json)  # valido la clave data
        self.assertIsNotNone(response.json['data'])  # el contenido no debe ser vacio
        self._import_concept = response.json['data'][0]

        # print("_import_concept.json ", self._import_concept)

        response = self.request_get("", "/" + str(self._import_concept['importConceptId']))  # envio el request al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convierto a json object

        # validate keys in response
        self.assertTrue("updateDate" in response.json, 'incorrect response by correct request')
        self.assertTrue("companyId" in response.json, 'incorrect response by correct request')
        self.assertTrue("name" in response.json, 'incorrect response by correct request')
        self.assertTrue("code" in response.json, 'incorrect response by correct request')
        self.assertTrue("importConceptId" in response.json, 'incorrect response by correct request')

        response = self.request_get("", "/company/5465665")  # envio el request al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convierto a json object

        self.assertEquals(response.json['data'], [])

        response = self.request_get("", "/521465665")  # envio el request al servidor
        response.json = json.loads(response.data.decode("utf-8"))  # convierto a json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_search_import_concept(self):
        """
        This function test get a import concept according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?search=A&companyId=1") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertTrue("data" in response.json) # valido la clave data
        self.assertIsNotNone(response.json['data']) # el contenido no debe ser vacio
        self._import_concept = response.json['data'][0]

        response = self.request_get("", "/"+str(self._import_concept['importConceptId'])) # envio el request al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convierto a json object

        # validate keys in response
        self.assertTrue("updateDate" in response.json, 'incorrect response by correct request')
        self.assertTrue("companyId" in response.json, 'incorrect response by correct request')
        self.assertTrue("name" in response.json, 'incorrect response by correct request')
        self.assertTrue("code" in response.json, 'incorrect response by correct request')
        self.assertTrue("importConceptId" in response.json, 'incorrect response by correct request')

        response = self.request_get("",  "/search?search=A&companyId=14654646") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertTrue("data" in response.json)
        self.assertEquals(response.json['data'], [])

        response = self.request_get("",  "/search?search=A") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')

    def test_post_put_and_delete(self):
        """
        This function allow create, update and delete a import_concept
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        _import_concept = {
          'name': 'TEST IMPORT CONCEPT',
          'isDeleted': 0,
          'code': '099',
          'companyId': 1,
        }
        #
        response = self.request_post(_import_concept)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("importConceptId", response.json)
        self.importConceptId = response.json['importConceptId']

        response = self.request_get("", "/search?code=099&companyId=1") # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.concept = response.json

        # validate keys in response
        self.assertTrue("updateDate" in self.concept, 'incorrect response by correct request')
        self.assertTrue("companyId" in self.concept, 'incorrect response by correct request')
        self.assertTrue("name" in self.concept, 'incorrect response by correct request')
        self.assertTrue("code" in self.concept, 'incorrect response by correct request')
        self.assertTrue("importConceptId" in self.concept, 'incorrect response by correct request')

        # # *********************UPDATE*************************
        import_concept_copy = copy(_import_concept)
        import_concept_copy['name'] = "TEST IMPORT CONCEPT UPDATE"
        import_concept_copy['importConceptId'] = self.importConceptId
        #
        response = self.request_put(import_concept_copy,"/"+str(self.importConceptId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/search?code=099&companyId=1")  # envio peticion al servidor
        response.json = json.loads(response.data.decode("utf-8")) # convert to json object

        self.concept = response.json

        # validate keys in response
        self.assertTrue("updateDate" in self.concept, 'incorrect response by correct request')
        self.assertTrue("companyId" in self.concept, 'incorrect response by correct request')
        self.assertTrue("name" in self.concept, 'incorrect response by correct request')
        self.assertTrue("code" in self.concept, 'incorrect response by correct request')
        self.assertTrue("importConceptId" in self.concept, 'incorrect response by correct request')
        self.assertEqual(self.concept['code'], "099")
        self.assertNotEqual(self.concept['name'], 'TEST IMPORT CONCEPT')
        self.assertEqual(self.concept['name'], 'TEST IMPORT CONCEPT UPDATE')

        import_concept_copy['importConceptId'] = 100

        response = self.request_put(import_concept_copy, "/"+str(self.importConceptId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual('BAD REQUEST', response.json['error'].upper(), 'incorrect response by bad request')

        import_concept_copy['importConceptId'] = 100

        response = self.request_put(import_concept_copy, "/1079878970")
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual('BAD REQUEST', response.json['error'].upper(), 'incorrect response by bad request')

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(self.importConceptId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)

        response = self.request_delete("", "/45646546")  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'incorrect response by bad request')
