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
import os
import sys
import json
import unittest

from app import create_app
from app.api_v1 import api


class RolesSecurityTest(unittest.TestCase):
    """
    This Class is a Test Case for Roles API class
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
    def request_get(self, path="/"):
        """Sent get request to #/api_security/v1/profiles# with roles data values
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        # envio el request
        return self.test_client.get('/api/v1/profiles'+path, content_type='application/json', headers=self.headers)

    def request_post(self,data,path="/"):
        """Sent post request to #/api_security/v1/profiles# with roles data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/profiles'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api_security/v1/profiles# with roles data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/profiles'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self, path="/"):
        """Sent delete request to #/api_security/v1/profiles# with roles data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/profiles'+path,
                content_type='application/json',headers=self.headers)  # envio el request

    def request_custom_get(self, path="/"):
        """Sent get request to #/api_security/v1/profiles# with roles data values
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        # envio el request
        return self.test_client.get('/api/v1' + path, content_type='application/json', headers=self.headers)
    ######################################################################################

    def test_get_roles(self):
        """
        This function test get all identification-types
        ** First validate that contains the items key and content
        """
        data = {
            "name": "TESTUNITARIO",
            "ProfileOptions": [{
                "c": True,
                "childs": None,
                "code": "PYMESModule_Presenters_UserPresenter",
                "d": True,
                "name": "Usuarios",
                "optionId": 271,
                "order": None,
                "parent": 328,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "PYMESModule_Presenters_RolPresenter",
                "d": True,
                "name": "Perfiles",
                "optionId": 292,
                "order": None,
                "parent": 328,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "Administración_y_Seguridad",
                "d": True,
                "name": "Administración y Seguridad",
                "optionId": 328,
                "order": None,
                "parent": 333,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "ESTRUCTURACIÓN",
                "d": True,
                "name": "ESTRUCTURACIÓN",
                "optionId": 333,
                "order": 1,
                "parent": None,
                "r": True,
                "u": True
            }]
        }

        # Test para validar que guarde
        response = self.request_post(data)
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 201)

        # Test para verificar que hay respuesta
        response = self.request_get()
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 200)

        # Valida que se guardo el rol anterior
        response = self.request_get('/?search=TESTUNITARIO')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        print(">>>> ", response.json)
        self.assertEquals(response.json['data'][0]['name'], 'TESTUNITARIO', 'NO EXISTE ESTE ROL')
        rol_id = response.json['data'][0]['rolId']

        # Actualiza el rol
        data = {
            "id": 19,
            "name": "TESTUNITARIOMODIFICADO",
            "ProfileOptions": [{
                "c": True,
                "childs": None,
                "code": "PYMESModule_Presenters_UserPresenter",
                "d": True,
                "name": "Usuarios",
                "optionId": 271,
                "order": None,
                "parent": 328,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "PYMESModule_Presenters_RolPresenter",
                "d": True,
                "name": "Perfiles",
                "optionId": 292,
                "order": None,
                "parent": 328,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "Administración_y_Seguridad",
                "d": True,
                "name": "Administración y Seguridad",
                "optionId": 328,
                "order": None,
                "parent": 333,
                "r": True,
                "u": True
            }, {
                "c": True,
                "childs": None,
                "code": "ESTRUCTURACIÓN",
                "d": True,
                "name": "ESTRUCTURACIÓN",
                "optionId": 333,
                "order": 1,
                "parent": None,
                "r": True,
                "u": True
            }]
        }
        response = self.request_put(data, '/{0}'.format(rol_id))
        self.assertEquals(response.status_code, 200)
        # Valida que este guardado el con el nombre que se modifico
        response = self.request_get('/?search=TESTUNITARIOMODIFICADO')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertGreater(len(response.json['data']), 0)
        self.assertEqual(response.json['data'][0]['name'], 'TESTUNITARIOMODIFICADO')
        # Envio de peticion con id inexistente
        response = self.request_put(data, '/{0}'.format(999999))
        self.assertEqual(response.status_code, 400)

        # Valida el api de obtener por id
        response = self.request_get('/{0}'.format(rol_id))
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        # Valida que devuelva la mismca cantidad de opciones con que se guardaron
        self.assertEqual(len(response.json['data']), 1)

        # Elimina el perfil
        response = self.request_delete('/{0}'.format(rol_id))
        self.assertEquals(response.status_code, 200)
        # Eliminar perfil con usuarios atados
        response = self.request_delete('/{0}'.format(10))
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 400)
        self.assertEqual(response.json['message'],
                         'El perfil no se puede eliminar porque está siendo usado por un usuario')

        # Test al api que genera el arbol de opciones vacias
        response = self.request_custom_get('/options/?all_role_option_tree=1')
        self.assertEqual(response.status_code, 200)

