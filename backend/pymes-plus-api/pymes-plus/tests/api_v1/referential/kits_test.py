#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import Flask
import unittest
import json
import time
import logging


from app import create_app
from app.api_v1 import api
import copy

"""
This module shows several methods and function by allow
handled BusinessAgentsTest
"""
class KitsTest(unittest.TestCase):
    """
    This Class is a  Test Case for Brands Api class
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
        """Sent get request to #/api/v1/kits# with kits data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/kits'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/kits# with kits data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/kits'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/kits# with kits data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/kits'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/kits# with kits data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/kits'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_kits(self):
        """
        This function test get all kits
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("", "/")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.kit = response.json['data'][0]

        # envio la peticion al sevidor
        response = self.request_get("", "/search?search=&company_id=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.kit = response.json['data'][0]
        #
        self.assertIn("nameItem", self.kit)
        self.assertIn("code", self.kit)
        self.assertIn("name", self.kit)
        self.assertIn("itemId", self.kit)
        self.assertIn("companyId", self.kit)
        #
        # envio la peticion al sevidor
        response = self.request_get("", "/"+str(9999))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        print(">> ",self.kit)
        # # envio la peticion al sevidor
        response = self.request_get("", "/"+str(self.kit['itemId']))
        # # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.kit = response.json

        self.assertIn("kitId", self.kit)
        self.assertIn("kitStages", self.kit)
        self.assertIn("kitAssets", self.kit['kitStages'][0])
        self.assertIn("kitLabors", self.kit['kitStages'][0])
        self.assertIn("kitItems", self.kit['kitStages'][0])
        #
        response = self.request_get("", "/search?company_id=1&search=")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        #
        # envio la peticion al sevidor
        response = self.request_get("", "/kit/" + str(self.kit['kitId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        self.kit = response.json
        self.assertIn("kitId", self.kit)
        self.assertIn("kitStages", self.kit)
        self.assertIn("kitAssets", self.kit['kitStages'][0])
        self.assertIn("kitLabors", self.kit['kitStages'][0])
        self.assertIn("kitItems", self.kit['kitStages'][0])


    def test_post_put_delete_kits(self):
        """
        This function test get a kit according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        kit = {
          "itemId": 4,
          "kitStages": [
            {
              "comments": "PRUEBA POSTMAN1",
              "kitAssets": [],
              "kitItems": [
                {
                  "articleId": 233,
                  "code": "ANI374",
                  "measurementUnitCode": "SB ",
                  "name": "PRB ITEM CREATE",
                  "quantity": 100
                }
              ],
              "kitLabors": [],
              "name": "ETP POSTMAN1",
              "stageId": 14
            },
            {
              "comments": "PRB POSTMAN2",
              "kitAssets": [
                {
                  "Name": "MONTAPRUEBA",
                  "assetId": 27,
                  "code": "prb001",
                  "quantity": 10
                }
              ],
              "kitItems": [
                {
                  "articleId": 243,
                  "code": "PRB002",
                  "measurementUnitCode": "SB ",
                  "name": "PRBBB",
                  "quantity": 8
                }
              ],
              "kitLabors": [],
              "name": "EPT POSTMAN2",
              "stageId": 15
            }
          ]
        }
        response = self.request_post(kit)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("kitId", response.json)
        self.kitId = response.json['kitId']
        self.itemId = kit['itemId']

        response = self.request_get("", "/" + str(self.itemId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.kit = response.json

        self.assertIn("kitId", self.kit)
        self.assertIn("kitStages", self.kit)
        self.assertIn("kitAssets", self.kit['kitStages'][0])
        self.assertIn("kitLabors", self.kit['kitStages'][0])
        self.assertIn("kitItems", self.kit['kitStages'][0])

        # *********************UPDATE*************************
        kit_copy = copy.deepcopy(kit)
        kit_copy['kitStages'] = []
        kit_copy['kitId'] = self.kitId

        response = self.request_post(kit_copy)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        response = self.request_put(kit_copy, "/" + str(9999))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        response = self.request_put(kit_copy, "/" + str(self.kitId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        kit_copy['kitStages'] = [
            {
              "comments": "PRUEBA POSTMAN1",
              "kitAssets": [],
              "kitItems": [
                {
                  "articleId": 233,
                  "code": "ANI374",
                  "measurementUnitCode": "SB ",
                  "name": "PRB ITEM CREATE",
                  "quantity": 100
                }
              ],
              "kitLabors": [],
              "name": "ETP POSTMAN1",
              "stageId": 14
            },
            {
              "comments": "PRB POSTMAN2",
              "kitAssets": [
                {
                  "Name": "MONTAPRUEBA",
                  "assetId": 27,
                  "code": "prb001",
                  "quantity": 10
                }
              ],
              "kitItems": [
                {
                  "articleId": 243,
                  "code": "PRB002",
                  "measurementUnitCode": "SB ",
                  "name": "PRBBB",
                  "quantity": 8
                }
              ],
              "kitLabors": [],
              "name": "EPT POSTMAN2",
              "stageId": 15
            }
          ]
        response = self.request_put(kit_copy, "/" + str(self.kitId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)


        response = self.request_get("", "/" + str(self.itemId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # self.assertEqual(kit_copy['description'], response.json['description'])
        # self.assertEqual(kit_copy['comments'], response.json['comments'])

        kit_copy['kitId'] = 9999
        response = self.request_put(kit_copy, "/" + str(9999))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(9999))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertIn("message", response.json)

        print(">>", self.kitId)
        response = self.request_delete("", "/" + str(self.kitId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object


