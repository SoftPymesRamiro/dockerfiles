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
handled invoice_sale_aiu
"""
class SaleAIUTest(unittest.TestCase):
    """
    This Class is a  Test Case for invoice_sale_aiu API class
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
        """Sent get request to #/api/v1/invoice_sale_aiu# with invoice_sale_aiu data values

        :param data: invoice_sale_aiu data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/invoice_sale_aiu' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/invoice_sale_aiu# with invoice_sale_aiu data values

        :param data: invoice_sale_aiu data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/invoice_sale_aiu' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/invoice_sale_aiu# with invoice_sale_aiu data values

        :param data: invoice_sale_aiu data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/invoice_sale_aiu' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/invoice_sale_aiu# with invoice_sale_aiu data values

        :param data: invoice_sale_aiu data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/invoice_sale_aiu' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_invoice_sale_aiu(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # prueba de consulta general
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&limitDate=2017-06-30&documentNumber=null&controlNumber=null&search=null&filterBy=None&initTotal=null&endTotal=null&shortWord=AU',
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

    def test_get_invoice_sale_aiu_search(self):
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
        invoice_sale_aiu = response.json['data'][0]
        documentNumber = invoice_sale_aiu['documentNumber']
        documentHeaderId = invoice_sale_aiu['documentHeaderId']
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
        response = self.request_get("", "/" + str(invoice_sale_aiu['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/" + str(invoice_sale_aiu['documentHeaderId']) + "/preview?format=P")
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
        invoice_sale_aiu = {'consumptionTaxValue': 0, 'retentionValue': 0, 'overCostTaxBase': 0, 'percentageCREE': 0, 'reteIVAPercent': 0, 'currencyId': 4, 'shipTo': ' CASAÑAS MAYA JULIO CESAR', 'thirdId': None, 'baseCREE': 0, 'disccount': 270000, 'sourceDocumentOrigin': 'AU', 'withholdingTaxValue': 305550, 'payment': 10126800, 'dependencyId': None, 'documentDate': '2017-06-08T08:21:54.000Z', 'retentionPUCId': None, 'reteICAValue': 0, 'sectionId': 1, 'total': 10126800, 'customer': {'customerId': 1, 'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA', 'branch': '110'}, 'valueCREE': 0, 'divisionId': 1, 'documentNumber': '0000000970', 'shipCountry': ' COLOMBIA', 'retentionPercent': 0, 'reteIVABase': 0, 'costCenter': None, 'employeeId': None, 'customerId': 1, 'costCenterId': 1, 'reteICAPercent': 0, 'sourceShortWord': 'AU', 'dateTo': None, 'reteIVAValue': 0, 'shipCity': 'CALI ', 'overCost': 0, 'shipDepartment': ' VALLE DEL CAUCA ', 'termDays': 0, 'documentAffecting': [], 'paymentReceipt': {}, 'branchId': 1, 'comments': 'NINGUNA', 'paymentTermId': 2, 'disccount2': 0, 'orderNumber': '323232', 'annuled': None, 'controlPrefix': None, 'shipAddress': 'CR 37 10 303', 'subtotal': 9000000, 'documentDetails': [{'pucId': 8290, 'quantity': 1, 'icaPercent': 0, 'consultItem': True, 'puc': {'pucId': 8290, 'percentage': 0, 'quantity': True, 'name': 'CULTIVO DE FLORES', 'pucAccount': '410525005', 'dueDate': False}, 'withholdingTax': 3.5, 'indexItem': 0, 'baseValue': 8730000, 'badgeValue': 0, 'iva': 16, 'unitValue': 0, 'ivaPUCId': 7721, 'comments': 'DASDJKASDJKASDK JSAJKDKJASJKDASD', 'disccount': 3, 'withholdingTaxPUCId': 6459, 'detailDate': '2017-06-08T08:21:54.000Z', 'value': 9000000, 'units': 0}], 'disccount2TaxBase': 0, 'shipZipCode': '', 'selectedSalesMan': {'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)', 'type': 'BusinessAgent', 'id': 2}, 'shipPhone': '', 'billingResolutionId': 1, 'sourceDocumentHeaderId': None, 'disccount2Value': 0, 'controlNumber': None, 'ivaValue': 1396800, 'exchangeRate': 1, 'reteICABase': 0, 'shortWord': 'FC', 'applyCree': False, 'businessAgentId': 2}
        # Envio la creacion del avance sin short word
        invoice_sale_aiu["shortWord"] = None
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        invoice_sale_aiu["shortWord"] = "XY"
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        invoice_sale_aiu["shortWord"] = "FC"
        # Crea un compra de item con un peso de diferencia en el credit
        # invoice_sale_aiu['documentDetails'][0]['value'] = 9000000
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        invoice_sale_aiu['documentDetails'][0]['value'] = 9000000
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        invoice_sale_aiu['documentDetails'][0]['value'] = 9000000.18
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(invoice_sale_aiu)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
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

        invoice_sale_aiu2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(invoice_sale_aiu2)
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
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 9000000.18
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # Cambio el valor total del avance
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