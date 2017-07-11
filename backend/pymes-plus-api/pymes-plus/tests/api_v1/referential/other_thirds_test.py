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
This module shows several methods and function by allow
handled BusinessAgentsTest
"""
class OtherThirds(unittest.TestCase):
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
        """Sent get request to #/api/v1/other_thirds# with other_thirds data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/other_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/other_thirds# with other_thirds data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/other_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/other_thirds# with other_thirds data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/other_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/other_thirds# with other_thirds data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/other_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_other_thirds(self):
        """
        This function test get all other_thirds
        ** First validate that contains the data key and content
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data es la clave principal de este response
        self.assertTrue("data" in response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        # evaluo los primeros ocho elementos con las claves obligatorias
        for other_third in response.json['data'][:8]:
            self.assertIn("otherThirdId", other_third) # otherThirdId debe existir
            self.assertIn("name", other_third)
            self.assertIn("thirdPartyId", other_third)

        # envio la peticion al sevidor
        # No importa el el contenido del request.
        # Esta peticion no depende del contenido del get
        response = self.request_get(None)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal
        self.assertTrue("data" in response.json)
        # el contenido no puede ser vacio
        self.assertIsNotNone(response.json['data'])

        # esta peticion debe ser unica para y depende
        # del query string (cadena de consulta)
        response = self.request_get("","/$%$%65465563424ojsdsad%")

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')


    def test_get_other_third(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertTrue("data" in response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        # para el resto de la prueba tomo un ID
        self.otherThirdId = response.json['data'][3]["otherThirdId"]
        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(self.otherThirdId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)

        other_third = response.json

        # debe haberme traido el mismo id
        self.assertEqual(other_third["otherThirdId"], self.otherThirdId)

        self.assertIn("otherThirdId", other_third)  # otherThirdId debe existir
        self.assertIn("name", other_third)
        self.assertIn("thirdPartyId", other_third)


        # envio la peticion al sevidor
        response = self.request_get("", "/None")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/L")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/10L")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/999999999")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')



    def test_search_other_thirds(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        other_third = response.json['data'][2]

        self.assertIn("thirdPartyId", other_third)
        self.assertIn("companyId", other_third)

        # envio la peticion al sevidor
        response = self.request_get("", "/search?simple=1&thirdPartyId=" +
                                    str(other_third['thirdPartyId']) + "&CompanyId=" + str(other_third['companyId']))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data es la clave principal de este response
        self.assertIn("data", response.json)


        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        other_third = response.json['data'][0]

        self.assertIn("otherThirdId", other_third)  # other_thirdId debe existir
        self.assertIn("name", other_third)
        self.assertIn("contactList", other_third)
        self.assertIn("address1", other_third)
        self.assertIn("billCity", other_third)

    def test_post_put_delete_other_thirds(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        other_third= {
                'billCity': {
                    'cityId': 61,
                    'name': 'SAN CARLOS - CÓRDOBA - COLOMBIA',
                    'department': {
                        'country': {
                            'countryId': 2,
                            'indicative': '57'
                        },
                        'departmentId': 10,
                        'name': 'CÓRDOBA',
                        'code': '23'
                    },
                    'indicative': '4',
                    'code': '678'
                },
                'thirdPartyId': 2296,
                'isDeleted': 0,
                'branch': '14',
                'cityId': 61,
                'fax': '22222222',
                'address1': 'CRA 32 # 90-58',
                'phone': '3333333333',
                'billCitySimple': {
                    'cityId': 61,
                    'name': 'SAN CARLOS - CÓRDOBA - COLOMBIA',
                    'department': {
                        'country': {
                            'countryId': 2,
                            'indicative': '57'
                        },
                        'departmentId': 10,
                        'name': 'CÓRDOBA',
                        'code': '23'
                    },
                    'indicative': '4',
                    'code': '678'
                },
                'contactList': [

                ],
                'zipCode': '324324',
                'address2': None,
                'name': 'TEST',
                'companyId': 1,
                'state': 'A'
            }


        # envio la peticion al sevidor
        response = self.request_post(other_third)

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))


        # data es la clave principal de este response
        self.assertIn("otherThirdId", response.json)

        self.otherThirdId = response.json['otherThirdId']


        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(self.otherThirdId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        other_third2 = response.json

        self.assertIn("otherThirdId", other_third2)  # otherThirdId debe existir
        self.assertIn("name", other_third2)
        self.assertIn("address2", other_third2)
        self.assertIn("thirdPartyId", other_third2)
        self.assertIn("companyId", other_third2)


        # **********************************************************
        other_third2['address1'] = 'Cra 23 # 65 -52'
        other_third2['phone'] = "(052) 359-455"
        other_third2['fax'] = "(058) 359-455-45456"

        # envio la peticion al sevidor
        response = self.request_put(other_third2, "/" + str(self.otherThirdId))

        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(self.otherThirdId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        other_third2 = response.json

        self.assertNotEqual(other_third2['address1'], other_third['address1'])
        self.assertNotEqual(other_third2['phone'], other_third['phone'])
        self.assertNotEqual(other_third2['fax'], other_third['fax'])

        # **********************************************************
        # envio la peticion al sevidor
        response = self.request_delete("", "/" + str(self.otherThirdId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("message", response.json)
