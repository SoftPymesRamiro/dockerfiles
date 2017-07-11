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
handled intern_consumption
"""
class InternConsumptionTest(unittest.TestCase):
    """
    This Class is a  Test Case for intern_consumption API class
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
        """Sent get request to #/api/v1/intern_consumption# with intern_consumption data values

        :param data: intern_consumption data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/intern_consumption' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/intern_consumption# with intern_consumption data values

        :param data: intern_consumption data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/intern_consumption' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/intern_consumption# with intern_consumption data values

        :param data: intern_consumption data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/intern_consumption' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/intern_consumption# with intern_consumption data values

        :param data: intern_consumption data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/intern_consumption' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_purchase_aiu(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&limitDate=2017-06-30&documentNumber=null&controlNumber=null&search=null&filterBy=None&initTotal=null&endTotal=null&shortWord=AC',
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

    def test_get_intern_consumption_search(self):
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
        response = self.request_get('', '/search?branch_id=1&short_word=CI&document_number=9999999999')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&'+
                                        'limitDate=2017-06-30&documentNumber=null&controlNumber=null&search'+
                                        '=null&filterBy=None&initTotal=null&endTotal=null&shortWord=AU',
                                    data=json.dumps(''),
                                    content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("data", response.json)
        intern_consumption = response.json['data'][0]
        documentNumber = intern_consumption['documentNumber']
        documentHeaderId = intern_consumption['documentHeaderId']

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=1&short_word=XXXX&document_number=' + str(documentNumber))

        response.json = json.loads(response.data.decode("utf-8"))
        print(">>>>>>> ",response.json)
        self.assertEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=1&short_word=FC&document_number=' + str(documentNumber))
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {'error': 'bad request', 'message': 'Invalid params', 'status': 400})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(intern_consumption['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(intern_consumption['documentHeaderId']) + "/preview?format=P")
        # response.json = json.loads(response.data.decode("utf-8"))
        # self.assertEquals(response.status_code, 200)
        # self.assertNotEquals(response, {})
        # self.assertIn("data", response.json)

    ##################################################################################
    def test_post_put_delete(self):
        """
        This function allow create, update and delete a purchase item
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        intern_consumption = {'documentDetails': None, 'comments': None, 'disccount2': None, 'sourceDocumentHeaderId': None, 'paymentReceipt': {'bondsList': [{'isDeleted': 0, 'updateBy': 'Migracion', 'name': 'BONO REGALO', 'pucId': None, 'creationDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'paymentType': 'BN', 'updateDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'code': '10', 'createdBy': 'Migracion', 'paymentMethodId': 9, 'puc': None}, {'isDeleted': 0, 'updateBy': 'Migracion', 'name': 'NOTAS DE CAMBIO', 'pucId': None, 'creationDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'paymentType': 'BN', 'updateDate': 'Fri, 17 Aug 2012 10:35:28 GMT', 'code': '09', 'createdBy': 'Migracion', 'paymentMethodId': 8, 'puc': None}], 'payment': 1940000, 'bankAccountList': [], 'paymentMeth': {'cash': [{'paymentType': 'EF', 'value': 1940000, 'comments': '', 'balance': 0}], 'bonds': [], 'creditCard': [], 'checkBook': [], 'debitCard': [], 'transfer': []}, 'difference': 0, 'cashReceipt': '0000001005', 'financialList': [], 'paymentDetails': [{'paymentDetailId': None, 'state': 1, 'documentNumber': None, 'bankName': None, 'beneficiary': None, 'accountNumber': None, 'authorizationNumber': None, 'dueDate': None, 'prefixNumber': None, 'paymentMethodId': None, 'paymentReceiptId': None, 'bankCheckBookId': None, 'value': 1940000, 'bankAccountId': None, 'finantialEntityId': None, 'comments': '', 'quoteNumber': None, 'paymentType': 'EF', 'balance': 0, 'cardNumber': None}], 'total': 1940000, 'financialPage': 1}, 'costCenter': None, 'sourceShortWord': 'AC', 'shortWord2': 'RC', 'disccount': None, 'costCenterId': 1, 'reteICABase': 0, 'ivaValue': 0, 'withholdingTaxPUCId': 6458, 'currencyId': 4, 'withholdingTaxPercent': 0, 'reteIVAPercent': 0, 'thirdId': None, 'total': 1940000, 'subtotal': 2000000, 'retentionValue': 0, 'controlNumber': None, 'disccount2TaxBase': None, 'paymentTermId': 1, 'retentionPercent': 0, 'documentAffecting': [], 'dependencyId': None, 'disccount2Value': None, 'reteICAPercent': 3, 'documentDate': '2017-06-07T15:27:12.000Z', 'pucId': 7969, 'employeeId': None, 'withholdingTaxBase': 2000000, 'branchId': 1, 'customerId': 1, 'exchangeRate': 1, 'reteICAValue': 60000, 'termDays': 0, 'divisionId': 1, 'documentNumber': '0000000058', 'puc': {'loansMembersConcepts': False, 'asset': False, 'name': 'DE CLIENTES', 'percentage': 0, 'pucId': 7969, 'baseValue': False, 'mainDocument': True, 'provider': False, 'dueDate': True, 'employee': False, 'pucAccount': '280505005', 'customer': True, 'third': False, 'thirdRequiredDCNB': False, 'quantity': False, 'partner': False, 'needCashRegister': False, 'article': False, 'payrollEntity': False, 'foreignCurrencyAccountsReceivable': False, 'alternateDoc': False}, 'retentionPUCId': None, 'businessAgentId': 2, 'withholdingTaxValue': 0, 'payment': 1940000, 'dateTo': None, 'reteIVAValue': 0, 'sectionId': 1, 'selectedSalesMan': {'id': 2, 'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)', 'type': 'BusinessAgent'}, 'sourceDocumentOrigin': 'AC', 'reteIVABase': 0, 'customer': {'customerId': 1, 'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA', 'branch': '110'}, 'divisas': 0, 'percentageCREE': 0, 'annuled': None, 'withholdingTax': {'percentage': 0, 'quantity': False, 'pucId': 6458, 'name': 'RETENCION EN LA FUENTE - EXENTA', 'dueDate': False, 'pucAccount': '135515005'}, 'shortWord': 'AC', 'controlPrefix': None}
        # Envio la creacion del avance sin short word
        intern_consumption["shortWord"] = None
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        intern_consumption["shortWord"] = "XY"
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        intern_consumption["shortWord"] = "FP"
        # Crea un compra de item con un peso de diferencia en el credit
        intern_consumption['documentDetails'][0]['value'] = 550627
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        intern_consumption['documentDetails'][0]['value'] = 550627
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        intern_consumption['documentDetails'][0]['value'] = 550627.18
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = intern_consumption['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                      "currencyId": 2,
                      "isDeleted": 0,
                      "name": "DÓLAR AMERICANO",
                      "symbol": "$"}

        intern_consumption["currency"] = currency2
        intern_consumption["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(intern_consumption)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        intern_consumption["currency"] = currency
        intern_consumption["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=1&short_word=FP&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("dateFrom", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("disccount2Value", response.json)
        self.assertIn("comments", response.json)

        intern_consumption2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(intern_consumption2)
        # Cambio el total
        purchase_copy['documentDetails'][0]['value'] = 1000
        # Envio a actulizar el compra de item
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)
        # self.assertIn("error", response.json)
        # self.assertIn("status", response.json)

        # Espero un error por descuadre...
        # FIXME: deberia establecer un error particular para este caso
        # self.assertEquals(response.status_code, 500)
        # self.assertIn("message", response.json)
        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 500000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 550627.18
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # Copio el ultimo de los detalles de pago
        # payment_detail = purchase_copy['paymentReceipt']['paymentDetails'][1]
        # Elimino esta posicion del arreglo
        # del purchase_copy['paymentReceipt']['paymentDetails'][1]
        # Cambio el valor total del avance
        # purchase_copy['documentDetails'][0]['value'] = 300000
        # Actualiza el compra de item
        # response = self.request_put(purchase_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        # self.assertIn("ok", response.json)

        # Simula un nuevo detalle de pago con base al eliminado
        # payment_detail.pop('paymentDetailId', None)
        # purchase_copy['paymentReceipt']['paymentDetails'].append(payment_detail)
        # Cambio el valor total del avance
        purchase_copy['documentDetails'][0]['value'] = 550627.18
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

        self.assertEqual('SALE ITEM NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')