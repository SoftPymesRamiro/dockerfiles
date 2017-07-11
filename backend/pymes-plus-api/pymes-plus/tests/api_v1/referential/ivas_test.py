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


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for Iva Test API class
"""
class IvasTest(unittest.TestCase):
    """
    This Class is a Test Case for Iva API class
    """

    def setUp(self):
        """
        initial conf data
        """
        self.userdata = dict(username='administrador',
            password='Admin*2')

        app = Flask(__name__) ## aplication Flask
        self.app = create_app(app)  ## pymes-plus-api
        self.test_client = self.app.test_client(self) ## test client
        self.test_client.testing = True
        # app.config['SQLALCHEMY_ECHO'] = False

        self.response = self.test_client.post('/oauth/token',
                    data=json.dumps(self.userdata),
                        content_type='application/json')

        self.token = json.loads( self.response.data.decode("utf-8") )['token']

        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

        self.response = None

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        return self.test_client.get('/api/v1/iva'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        return self.test_client.post('/api/v1/iva'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        return self.test_client.put('/api/v1/iva'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        return self.test_client.delete('/api/v1/iva'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_iva(self):
        """
        This function test get all items
        """
        response = self.request_get("")
        response.json = json.loads( response.data.decode("utf-8") )

        # self.assertTrue("iva" in response.json)
        # self.assertIsNotNone(response.json['iva'])
        # print("#"*10, response.json)
        

    def test_search_iva(self):
        """
        This function test get all items
        """
        response = self.request_get("","/search?to_items=1")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("saleIVA" in response.json)
        self.assertTrue("purchaseIVA" in response.json)

        # print("#"*10, response.json)


    ##################################################################################
    # FALTAN POST, PUT AND DELETE
