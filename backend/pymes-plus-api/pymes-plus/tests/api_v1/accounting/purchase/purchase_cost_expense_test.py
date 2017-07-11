#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 26-12-2016
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
handled purchase_cost_and_expense
"""
class CostExpensesTest(unittest.TestCase):
    """
    This Class is a  Test Case for purchase_cost_and_expense API class
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
        """Sent get request to #/api/v1/purchase_cost_and_expense# with purchase_cost_and_expense data values

        :param data: purchase_cost_and_expense data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/purchase_cost_expenses' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/purchase_cost_and_expense# with purchase_cost_and_expense data values

        :param data: purchase_cost_and_expense data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/purchase_cost_expenses' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/purchase_cost_and_expense# with purchase_cost_and_expense data values

        :param data: purchase_cost_and_expense data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/purchase_cost_expenses' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/purchase_cost_and_expense# with purchase_cost_and_expense data values

        :param data: purchase_cost_and_expense data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/purchase_cost_expenses' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_purchaseItem(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.request_get('', '/117302')  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentTypeId" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentTermId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_purchase_cost_and_expense_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=FP")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FP&document_number=0000002852')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        purchase_cost_and_expense = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + purchase_cost_and_expense[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FP&document_number=' + purchase_cost_and_expense['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(purchase_cost_and_expense['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(purchase_cost_and_expense['documentHeaderId']) + "/preview?format=P")
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
        purchase_cost_and_expense = {'reteICAValue': 300, 'divisionId': 13, 'documentDate': '2017-03-30T09:02:57.000Z', 'providerId': 532, 'disccount2Value': 0, 'comments': 'ESTE ES UNA FACTURA PRUEBA', 'overCost': 0, 'pucId': 85598, 'documentAffecting': [], 'payment': 109720, 'shortWord': 'FP', 'total': 109720, 'valueCREE': 0, 'reteIVAValue': 480, 'disccount': 0, 'reteICAPercent': '3.00', 'documentDetails': [{'withholdingTax': 3.5, 'quantity': 0, 'iva': 16, 'otr': '', 'withholdingTaxPUCId': 85670, 'pucId': 89488, 'badgeValue': 0, 'dependencyId': None, 'baseValue': 100000, 'sectionId': 7, 'ivaPUCId': 85806, 'baseValueIVA': 100000, 'indexItem': 0, 'puc': {'name': 'SUELDOS', 'pucId': 89488, 'percentage': 0, 'quantity': False, 'pucAccount': '740506005', 'dueDate': False}, 'unitValue': 0, 'value': 100000, 'units': 0, 'disccount': 0, 'detailDate': '2017-03-30T09:02:57.000Z', 'consultItem': True, 'divisionId': 13, 'costCenterId': 4}], 'provider': {'name': ' PENA TORRES JEFFERSON AMADO (56403) - ASESORES JPT', 'thirdPartyId': 2394, 'isWithholdingCREE': 0, 'providerId': 532, 'branch': '789'}, 'subtotal': 100000, 'retentionPUCId': 85829, 'sourceDocumentHeaderId': None, 'withholdingTaxValue': 3500, 'dependencyId': None, 'paymentTermId': 2, 'retentionPercent': '2.00', 'costCenterId': 4, 'branchId': 14, 'dateTo': '2017-03-30T16:45:05.282Z', 'reteIVAPercent': '3.00', 'termDays': 0, 'reteICABase': 0, 'percentageCREE': 0, 'consumptionTaxValue': 0, 'documentNumber': '0000003098', 'controlNumber': '9999', 'controlPrefix': 'TEST', 'reteIVABase': 16000, 'overCostTaxBase': 0, 'retentionValue': 2000, 'sectionId': 7, 'ivaValue': 16000, 'baseCREE': 0, 'costCenter': None, 'sourceShortWord': 'FPC', 'currencyId': 4, 'puc': {'name': 'A CONTRATISTAS', 'pucId': 85598, 'percentage': 0, 'quantity': False, 'pucAccount': '232005005', 'dueDate': False}, 'disccount2': 0, 'exchangeRate': 1, 'paymentReceipt': {}, 'disccount2TaxBase': 0, 'annuled': None, 'applyCree': None}
        # Envio la creacion del avance sin short word
        purchase_cost_and_expense["shortWord"] = None
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        purchase_cost_and_expense["shortWord"] = "XY"
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        purchase_cost_and_expense["shortWord"] = "FP"
        # Crea un compra de item con un peso de diferencia en el credit
        purchase_cost_and_expense['documentDetails'][0]['value'] = 100000.1
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        purchase_cost_and_expense['documentDetails'][0]['value'] = 100000
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        purchase_cost_and_expense['documentDetails'][0]['value'] = 100000
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']

        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currencyId = purchase_cost_and_expense['currencyId']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        purchase_cost_and_expense["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(purchase_cost_and_expense)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        purchase_cost_and_expense["currencyId"] = currencyId

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=FP&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        purchase_cost_and_expense2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(purchase_cost_and_expense2)
        # Cambio el total
        purchase_copy['documentDetails'][0]['value'] = 1000
        # Envio a actulizar el compra de item
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)

        # Espero un error por descuadre...
        # FIXME: deberia establecer un error particular para este caso
        self.assertEquals(response.status_code, 500)
        self.assertIn("message", response.json)
        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 102000.98
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 100000
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
        purchase_copy['documentDetails'][0]['value'] = 100000
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

        self.assertEqual('PURCHASE ITEM NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')