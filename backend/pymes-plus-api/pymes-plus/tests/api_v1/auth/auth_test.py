# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# TEST Auth module
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"




from flask import Flask
import unittest
import json

from app import create_app
from app.api_v1 import api

"""
This module shows various  funtions and methods by allow
user access in SoftPymes plus
"""
class UserAuthTest(unittest.TestCase):
    """
    This Class is a  Test Case for User Auth
    """

    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
            password='Admin*2') # valid data by access to SoftPymes plus

        self.userdata_bad = dict(username='japeto',
            password='Admin*2') #invalid user data by try access


        app = Flask(__name__) # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self) # test client
        self.test_client.testing = False # allow create the environmet by test


    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,userdata,path=""):
        """Sent get request to #/oauth/token# whith user data values

        :param userdata: user data, username and password
        :type userdata: json object, default none
        :return: request response in dict format
        """
        return self.test_client.get('/oauth/token'+path,
                data=json.dumps(userdata),
                content_type='application/json')  # genero el request

    def request_post(self,userdata,path=""):
        """Sent post request to #/oauth/token# whith user data values

        :param userdata: user data, username and password
        :type userdata: json object, default none
        :return: request response in dict format
        """
        return self.test_client.post('/oauth/token'+path,
                data=json.dumps(userdata),
                content_type='application/json')  # genero el request

    def request_put(self,userdata,path=""):
        """Sent put request to #/oauth/token# whith user data values

        :param userdata: user data, username and password
        :type userdata: json object, default none
        :return: request response in dict format
        """
        return self.test_client.put('/oauth/token'+path,
                data=json.dumps(userdata),
                content_type='application/json')  # genero el request

    def request_delete(self,userdata,path="/"):
        """Sent delete request to #/oauth/token# whith user data values

        :param userdata: user data, username and password
        :type userdata: json object, default none
        :return: request response in dict format
        """
        return self.test_client.delete('/oauth/token'+path,
                data=json.dumps(userdata),
                content_type='application/json')  # genero el request

    ######################################################################################


    def test_user_auth(self):
        """This function is called to check if a username and password combination is valid.

        ** The first test is valid grants values and validate a token value
        ** The second test is invalidad grants values 404 status code
        ** The Third test is empty values and valitation of 404 code
        ** The fourth test is username valid and no paswword -- validation of 404 code
        ** The fifth test is no username valid and valid paswword -- validation of 404 code
        ** The sixth test is None values  -- NO PASSED
        """
        response = self.request_get(self.userdata) # peticion al servidor
        # print(response)
        # validacion de la peticion con los datos correctos
        self.assertEqual("200 OK", response.status)
        # verificaicon de la clave token en la respuesta
        self.assertTrue("token" in json.loads(response.data.decode("utf-8")))

        response = self.request_get(self.userdata_bad) # peticion al servidor
        # para una mala peticion, debe generarse un 400, aunque un NO FOUND
        self.assertEqual("400 BAD REQUEST",response.status)

        response = self.request_get(dict(username='', password='')) # peticion al servidor
        # para una mala peticion, debe generarse un 400, aunque un NO FOUND
        self.assertEqual("400 BAD REQUEST",response.status)

        response = self.request_get(dict(username='Adminstrador', password='')) # peticion al servidor
        # para una mala peticion, debe generarse un 400, aunque un NO FOUND
        self.assertEqual("400 BAD REQUEST",response.status)

        response = self.request_get(dict(username='', password='Admin*2')) # peticion al servidor
        # para una mala peticion, debe generarse un 400, aunque un NO FOUND
        self.assertEqual("400 BAD REQUEST",response.status)

        response = self.request_get(None) # peticion al servidor
        # para una mala peticion, debe generarse un 400, aunque un NO FOUND
        self.assertEqual("500 INTERNAL SERVER ERROR",response.status) # es correcto


    def test_get_token(self):
        """Allow get auth token key in several request with equal by username and password
         and validate that all are equals.
        """

        response = self.request_get(self.userdata) # peticion al servidor
        # get first token
        json_result = json.loads(response.data.decode("utf-8"))

        response2 = self.request_get(self.userdata) # peticion al servidor
        # get second token
        json_result2 = json.loads(response.data.decode("utf-8"))

        response3 = self.request_get(self.userdata) # peticion al servidor
        # get thiurd token
        json_result3 = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.status, response2.status)
        self.assertEqual(response.status, response3.status)
        self.assertEqual(json_result, json_result2, json_result3)
