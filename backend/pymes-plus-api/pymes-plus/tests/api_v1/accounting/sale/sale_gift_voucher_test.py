#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 06-06-2017
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
This module shows various methods and function by allow
handled sale_gift_voucher
"""
class SaleGiftVoucherTest(unittest.TestCase):
    """
    This Class is a  Test Case for sale_gift_voucher API class
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
    def request_get(self, data, path="/"):
        """Sent get request to #/api/v1/sale_gift_voucher# with sale_gift_voucher data values

        :param data: sale_gift_voucher data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sale_gift_voucher' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/sale_gift_voucher# with sale_gift_voucher data values

        :param data: sale_gift_voucher data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sale_gift_voucher' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/sale_gift_voucher# with sale_gift_voucher data values

        :param data: sale_gift_voucher data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sale_gift_voucher' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/sale_gift_voucher# with sale_gift_voucher data values

        :param data: sale_gift_voucher data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sale_gift_voucher' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_gift_voucher(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # prueba de consulta general
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2000-01-01'+
                                        '&limitDate=2017-06-30&documentNumber=null&controlNumber=null&'+
                                        'search=null&filterBy=None&initTotal=null&endTotal=null&shortWord=TBR',
                                    data=json.dumps(''),
                                    content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("data", response.json)
        documentHeaderId = response.json['data'][0]['documentHeaderId']
        # Busqueda por identificador
        response = self.request_get('', '/'+str(documentHeaderId))  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentTypeId" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentTermId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_gift_voucher_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=1&short_word=FC&billing_resolution_id=1")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=1&short_word=FC&document_number=0000099999')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&limitDate=2017-06-30&documentNumber=null&controlNumber=null&search=null&filterBy=None&initTotal=null&endTotal=null&shortWord=AU',
                                    data=json.dumps(''),
                                    content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("data", response.json)
        gift_voucher = response.json['data'][0]
        documentNumber = gift_voucher['documentNumber']
        documentHeaderId = gift_voucher['documentHeaderId']
        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=1&short_word=XXXX&document_number=' + str(documentNumber))

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=1&short_word=FC&billing_resolution_id=1'
                                    '&document_number=' + str(documentNumber))
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {'error': 'bad request', 'message': 'Invalid params', 'status': 400})

        # ################## GET
        response = self.request_get("", "/"+str(documentHeaderId))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(gift_voucher['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/" + str(gift_voucher['documentHeaderId']) + "/preview?format=P")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("data", response.json)

    ##################################################################################
    def test_post_put_delete(self):
        """
        This function allow create, update and delete a purchase item
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        gift_voucher = {'divisionId': 1, 'comments': None, 'annuled': None, 'documentAffecting': [], 'sourceDocumentOrigin': 'TBR', 'documentNumber': '0000000010', 'shortWord': 'TBR', 'customer': {'branch': '51', 'name': ' GONZALEZ IDROBO ANA MILENA (31448797) - ANA MILENA GONZALES', 'customerId': 5}, 'dateTo': '2017-06-12T08:21:54.000Z', 'documentDetails': None, 'businessAgentId': None, 'customerId': 5, 'dependencyId': None, 'exchangeRate': 0, 'subtotal': 0, 'thirdId': None, 'sectionId': 1, 'sourceShortWord': 'TBR', 'paymentReceipt': {'total': 900000, 'paymentDetails': [{'bankAccountId': None, 'dueDate': None, 'state': 1, 'finantialEntityId': None, 'authorizationNumber': None, 'bankName': None, 'paymentType': 'EF', 'balance': 0, 'value': 900000, 'quoteNumber': None, 'paymentDetailId': None, 'accountNumber': None, 'cardNumber': None, 'prefixNumber': None, 'paymentReceiptId': None, 'comments': '', 'documentNumber': None, 'paymentMethodId': None, 'bankCheckBookId': None, 'beneficiary': None}], 'bankAccountList': [], 'payment': 900000, 'bondsList': [{'paymentType': 'BN', 'code': '10', 'updateBy': 'Migracion', 'creationDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'paymentMethodId': 9, 'isDeleted': 0, 'puc': None, 'pucId': None, 'name': 'BONO REGALO', 'updateDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'createdBy': 'Migracion'}, {'paymentType': 'BN', 'code': '09', 'updateBy': 'Migracion', 'creationDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'paymentMethodId': 8, 'isDeleted': 0, 'puc': None, 'pucId': None, 'name': 'NOTAS DE CAMBIO', 'updateDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'createdBy': 'Migracion'}], 'paymentMeth': {'cash': [{'paymentType': 'EF', 'balance': 0, 'value': 900000, 'comments': ''}], 'checkBook': [], 'creditCard': [], 'transfer': [], 'debitCard': [], 'bonds': []}, 'cashReceipt': '0000001006', 'financialList': [], 'difference': 0, 'financialPage': 1}, 'sourceDocumentHeaderId': None, 'documentDate': '2017-06-08T08:21:54.000Z', 'paymentTermId': 1, 'costCenter': None, 'costCenterId': 1, 'shortWord2': 'RC', 'controlPrefix': None, 'payment': 900000, 'termDays': 4, 'branchId': 1, 'total': 900000, 'employeeId': None, 'currencyId': 4, 'controlNumber': '0000001006'}
        # Envio la creacion del bono sin short word
        gift_voucher["shortWord"] = None
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del bono con short word erroneo
        gift_voucher["shortWord"] = "XY"
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        gift_voucher["shortWord"] = "FC"
        # Crea un compra de item con un peso de diferencia en el credit
        # gift_voucher['documentDetails'][0]['value'] = 9000000
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del bono
        gift_voucher['documentDetails'][0]['value'] = 9000000
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        gift_voucher['documentDetails'][0]['value'] = 9000000.18
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(gift_voucher)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este bono para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=1&short_word=FC&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("dateFrom", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("disccount2Value", response.json)
        self.assertIn("comments", response.json)

        gift_voucher2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(gift_voucher2)
        # Cambio el total
        purchase_copy['documentDetails'][0]['value'] = 1000
        # Envio a actulizar el compra de item
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        # self.assertIn("ok", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)
        # Espero un error por descuadre...
        self.assertEquals(response.status_code, 500)
        self.assertIn("message", response.json)
        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 9000000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este bono
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 9000000.18
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este bono
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # Cambio el valor total del bono
        purchase_copy['documentDetails'][0]['value'] = 9000000.18
        purchase_copy['comments'] = "Este es el test"
        # Actualizo nuevamente
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Cambio el estado del documento
        purchase_copy['annuled'] = 1
        # Envio a actualizar
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # *********************DELETE*************************
        # TODO ESTE METODO NO DEBERIA USARSE DESDE LA VISTA
        # TODO SE AGREGA PARA MANTENER LA COHERENCIA DE LA BD EN PRUEBAS
        response = self.request_delete("", "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id0a))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id2))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('INVALID RESOURCE URI', response.json['message'].upper(), 'incorrect response by bad request')