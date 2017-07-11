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
from copy import deepcopy
from app import create_app
from app.api_v1 import api
import random


"""
This module shows several methods and function by allow
handled BusinessAgentsTest
"""
class BusinessAgentsTest(unittest.TestCase):
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
        """Sent get request to #/api/v1/business_agents# with business_agents data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/business_agents'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/business_agents# with business_agents data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/business_agents'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/business_agents# with business_agents data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/business_agents'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/business_agents# with business_agents data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/business_agents'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_business_agents(self):
        """
        This function test get all business_agents
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
        for business_agent in response.json['data'][:8]:
            self.assertIn("businessAgentId", business_agent) # businessAgentId debe existir
            self.assertIn("name", business_agent)
            self.assertIn("billAddress1", business_agent)
            self.assertIn("billCityId", business_agent)
            self.assertIn("billCityId", business_agent)
            self.assertIn("billCity", business_agent)
            self.assertIn("paymentTermId", business_agent)

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



    def test_get_business_agent(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data es la clave principal de este response
        self.assertTrue("data" in response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        # para el resto de la prueba tomo un ID
        self.businessAgentId = response.json['data'][3]["businessAgentId"]
        # envio la peticion al sevidor
        response = self.request_get("","/"+str(self.businessAgentId))
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)

        business_agent = response.json

        # debe haberme traido el mismo id
        self.assertEqual(business_agent["businessAgentId"], self.businessAgentId)

        self.assertIn("businessAgentId", business_agent)  # businessAgentId debe existir
        self.assertIn("name", business_agent)
        self.assertIn("billAddress1", business_agent)
        self.assertIn("billCityId", business_agent)
        self.assertIn("billCityId", business_agent)
        self.assertIn("billCity", business_agent)
        self.assertIn("paymentTermId", business_agent)

        # envio la peticion al sevidor
        response = self.request_get("","/None")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/L")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/10L")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        # envio la peticion al sevidor
        response = self.request_get("", "/8888888")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')


    def test_search_business_agents(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # envio la peticion al sevidor
        response = self.request_get("")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data es la clave principal de este response
        self.assertTrue("data" in response.json)

        # El contenido de esta clave no puede ser vacia
        self.assertIsNotNone(response.json['data'])

        # para el resto de la prueba extraigo los datos
        self.thirdPartyId = response.json['data'][2]["thirdPartyId"]
        self.branchId = response.json['data'][2]["branchId"]

        # envio la peticion al sevidor
        response = self.request_get("","/search?ThirdPartyId="+
                                    str(self.thirdPartyId)+"&BranchId="+str(self.branchId))

        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        # REVISAR -- varios puede conllevar a un error de DB
        self.assertTrue("data" in response.json)

        business_agent = response.json['data'][0]

        # debe haberme traido el mismo id
        self.assertEqual(business_agent["thirdPartyId"], self.thirdPartyId)
        self.assertEqual(business_agent["branchId"], self.branchId)

        self.assertIn("businessAgentId", business_agent)  # businessAgentId debe existir
        self.assertIn("name", business_agent)
        self.assertIn("billAddress1", business_agent)
        self.assertIn("billCityId", business_agent)
        self.assertIn("billCityId", business_agent)
        self.assertIn("billCity", business_agent)
        self.assertIn("paymentTermId", business_agent)


        # envio la peticion al sevidor
        # en la practica esto no deberia dar error
        # el query string no indica un orden
        response = self.request_get("","/search?BranchId="+
                                    str(self.branchId)+"&ThirdPartyId="+str(self.thirdPartyId))

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        # REVISAR -- varios puede conllevar a un error de DB
        self.assertTrue("data" in response.json)


        # envio la peticion al sevidor
        # en la practica esto no deberia dar error
        # el query string no indica un orden
        response = self.request_get("","/search?BranchId="+str(self.branchId))

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("data" in response.json)

        # evaluo los primeros ocho elementos con las claves obligatorias
        # ademas el tipo debe ser 'BusinessAgent'
        for business_agent in response.json['data'][:2]:
            self.assertIn("name", business_agent)
            self.assertIn("id", business_agent)
            self.assertIn("type", business_agent)
            self.assertEqual(business_agent["type"], 'BusinessAgent')


        # envio la peticion al sevidor
        response = self.request_get("", "/search?BranchId=None&ThirdPartyId=None")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("data" in response.json)

        # Dado que no debe haber coincidencia con None a esta
        # peticion debe responder con []
        self.assertEqual([],response.json['data'])


        # envio la peticion al sevidor
        response = self.request_get("", "/search?BranchId=None")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("data" in response.json)

        # Dado que no debe haber coincidencia con None a esta
        # peticion debe responder con []
        self.assertEqual([],response.json['data'])

        # envio la peticion al sevidor
        response = self.request_get("", "/search?BranchId=JAPeTo&ThirdPartyId=Q")
        # convierto a json object
        response.json = json.loads( response.data.decode("utf-8") )

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("data" in response.json)

        # Dado que no debe haber coincidencia con None a esta
        # peticion debe responder con []
        self.assertEqual([],response.json['data'])

        # envio la peticion al sevidor
        response = self.request_get("", "/search?BranchId=L")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("data" in response.json)

        # Dado que no debe haber coincidencia con None a esta
        # peticion debe responder con []
        self.assertEqual([], response.json['data'])

        # envio la peticion al sevidor
        response = self.request_get("", "/search?ThirdPartyId="+str(self.thirdPartyId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')



    def test_post_put_business_agent(self):
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

        # para el resto de la prueba creo una copia de uno existente.
        # se deberia construir uno nuevo con todos los datos.
        self.business_agent_copy = response.json['data'][2]

        if 'createdBy' in self.business_agent_copy:
            del self.business_agent_copy['updateBy']
        if 'createdBy' in self.business_agent_copy:
            del self.business_agent_copy['creationDate']
        if 'updateBy' in self.business_agent_copy:
            del self.business_agent_copy['updateDate']
        if 'creationDate' in self.business_agent_copy:
            del self.business_agent_copy['updateDate']
        if 'updateDate' in self.business_agent_copy:
            del self.business_agent_copy['billCity']
        if 'updateDate' in self.business_agent_copy:
            del self.business_agent_copy['shipCity']
        if 'billCity' in self.business_agent_copy:
            del self.business_agent_copy['shipCity']
        if 'createdBy' in self.business_agent_copy:
            del self.business_agent_copy['createdBy']

        if 'businessAgentId' in self.business_agent_copy:
            # envio la peticion al sevidor
            response = self.request_post(self.business_agent_copy)
            # convierto a json object
            response.json = json.loads(response.data.decode("utf-8"))

            # Como el id del agente comercial ya existe
            # no debe ingresar el agente
            # self.assertEqual('METHOD NOT ALLOWED', response.json['error'].upper(),
            #                  'Method Not Allowed is correct response')

            del self.business_agent_copy['businessAgentId']

        if 'contactList' in self.business_agent_copy:
            # # envio la peticion al sevidor
            # response = self.request_post(self.business_agent_copy)
            # # convierto a json object
            # response.json = json.loads(response.data.decode("utf-8"))
            #
            # # El servidor no debe enviar nada para este caso
            # self.assertEqual('BAD REQUEST', response.json['error'].upper(), 'Bad Request is correct response')

            del self.business_agent_copy['contactList']

        self.business_agent_copy['isMain'] = True
        self.business_agent_copy['branchBusinessAgent'] = str(random.randint(200, 999))

        # envio la peticion al sevidor
        # esta debe permitir la creacion de un
        # agente comercial
        response = self.request_post(self.business_agent_copy)

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("businessAgentId" in response.json)

        BusinessAgentsTest.businessAgentId = response.json['businessAgentId']

        # *************************************************************************
        # envio la peticion al sevidor
        response = self.request_get("", "/-10")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # El servidor no debe enviar nada para este caso
        self.assertEqual('NOT FOUND', response.json['error'].upper(), 'Not Found is correct response')

        #*************************************************************************
        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)

        self.businessAgentId = BusinessAgentsTest.businessAgentId

        # envio la peticion al sevidor
        response = self.request_get("", "/" + str(self.businessAgentId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)

        self.business_agent = response.json
        self.business_agent_copy = deepcopy(self.business_agent)

        # debe haberme traido el mismo id
        self.assertEqual(self.business_agent["businessAgentId"], self.businessAgentId)

        self.assertIn("businessAgentId", self.business_agent)  # businessAgentId debe existir
        self.assertIn("name", self.business_agent)
        self.assertIn("billAddress1", self.business_agent)
        self.assertIn("billCityId", self.business_agent)
        self.assertIn("billCityId", self.business_agent)
        self.assertIn("billCity", self.business_agent)
        self.assertIn("paymentTermId", self.business_agent)

        self.business_agent_copy['name']= "japetoTest"
        self.business_agent_copy["billAddress1"] = "direccion up"
        self.business_agent_copy["shipAddress"] = "direccion up"
        self.business_agent_copy["phone"] = "31232323"
        self.business_agent_copy["fax"] = "989-454554"
        self.business_agent_copy["creditCapacity"] = "877"

        #*****************************************************
        # envio la peticion al sevidor
        # esta debe permitir la actualizacion de un
        # agente comercial
        response = self.request_put(self.business_agent_copy, "/"+str(self.businessAgentId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        # ok es el resultado de la actualizacion
        self.assertTrue("ok" in response.json)

        # *****************************************************
        # envio la peticion al sevidor
        # para obtener nuevamente a quien se le hizo cambios
        response = self.request_get("", "/" + str(self.businessAgentId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data no puede ser la calve de este response
        # se pide uno y solo uno con esta peticion
        self.assertFalse("data" in response.json)
        business_agent = response.json

        # debe haberme traido el mismo id
        self.assertEqual(business_agent["businessAgentId"], self.businessAgentId)

        self.assertEqual(business_agent["businessAgentId"], self.business_agent["businessAgentId"])
        self.assertNotEqual(business_agent["name"], self.business_agent["name"])
        self.assertNotEqual(business_agent["billAddress1"], self.business_agent["billAddress1"])
        self.assertNotEqual(business_agent["shipAddress"], self.business_agent["shipAddress"])
        self.assertNotEqual(business_agent["phone"], self.business_agent["phone"])
        self.assertNotEqual(business_agent["creditCapacity"], self.business_agent["creditCapacity"])


        #*****************************************************
        # envio la peticion al sevidor
        # esta debe permitir la eliminacion de un
        # agente comercial
        response = self.request_delete("", "/"+str(self.businessAgentId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("message" in response.json)


        # *****************************************************
        # envio la peticion al sevidor
        # esta debe permitir la eliminacion de un
        # agente comercial
        response = self.request_delete("", "/None")
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        # data debe puede ser la calve para este response
        # pueden exitir varios que coincidan para una busqueda
        self.assertTrue("message" in response.json)
