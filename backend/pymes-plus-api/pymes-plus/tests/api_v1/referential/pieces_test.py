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
class PieceTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/pieces# with pieces data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/pieces'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/pieces# with pieces data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/pieces'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/pieces# with pieces data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/pieces'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/pieces# with pieces data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/pieces'+path,
                data=json.dumps(data),
                content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_pieces(self):
        """
        This function test get all pieces
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("", "/")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)

        # envio la peticion al sevidor
        response = self.request_get("", "/search?search=&companyId=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.piece = response.json['data'][0]

        self.assertIn("name", self.piece)
        self.assertIn("pieceId", self.piece)

        # envio la peticion al sevidor
        response = self.request_get("", "/"+str(self.piece['pieceId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("comments", response.json)
        self.assertIn("code", response.json)
        self.assertIn("state", response.json)
        self.assertIn("pieceId", response.json)
        self.assertIn("companyId", response.json)

        # envio la peticion al sevidor
        response = self.request_get("", "/search?code=" + self.piece['code'] + "&companyId=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("comments", response.json)
        self.assertIn("code", response.json)
        self.assertIn("state", response.json)
        self.assertIn("pieceId", response.json)
        self.assertIn("companyId", response.json)


    def test_post_put_delete_pieces(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("", "/search?branch=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        # El contenido debe ser vacia
        self.assertEqual(response.json['data'], [])

        # envio la peticion al sevidor
        response = self.request_get("", "/"+str(9999))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # envio la peticion al sevidor
        response = self.request_get("", "/search?search=&companyId=1")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # data es la clave principal de este response
        self.assertIn("data", response.json)
        self.assertNotEqual(response.json['data'], [])
        self.piece = response.json['data'][0]

        self.assertIn("name", self.piece)
        self.assertIn("pieceId", self.piece)

        piece =    {
          "code": "999",
          "comments": "PIECE TEST DESCRIPTION",
          "companyId": 1,
          "inventoryPUCId": 84663,
          "isDeleted": 0,
          "measurementUnitId": 4,
          "name": "PIECE TEST",
          "state": 0
        }

        response = self.request_post(piece)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("pieceId", response.json)
        self.pieceId = response.json['pieceId']

        response = self.request_get("", "/" + str(self.pieceId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("comments", response.json)
        self.assertIn("code", response.json)
        self.assertIn("state", response.json)
        self.assertIn("pieceId", response.json)
        self.assertIn("companyId", response.json)

        # *********************UPDATE*************************
        piece_copy = copy.deepcopy(piece)
        piece_copy['comments'] = "TEST UPDATE"
        piece_copy['name'] = "PIECE UP"
        piece_copy['pieceId'] = self.pieceId

        response = self.request_post(piece)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        response = self.request_put(piece_copy, "/" + str(9999))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        response = self.request_put(piece_copy, "/" + str(self.pieceId))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("ok", response.json)

        response = self.request_get("", "/" + str(self.pieceId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertEqual(piece_copy['comments'], response.json['comments'])
        self.assertEqual(piece_copy['name'], response.json['name'])

        piece_copy['pieceId'] = 9999
        response = self.request_put(piece_copy, "/" + str(9999))
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        # *********************DELETE*************************
        response = self.request_delete("", "/" + str(9999))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        response = self.request_delete("", "/" + str(self.pieceId))  # envio el request al server
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object

        self.assertIn("message", response.json)
