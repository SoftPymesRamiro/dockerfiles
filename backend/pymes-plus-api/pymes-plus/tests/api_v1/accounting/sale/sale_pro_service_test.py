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
handled sale_professional_services
"""
class SaleProfessionalServicesTest(unittest.TestCase):
    """
    This Class is a  Test Case for sale_professional_services API class
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
        """Sent get request to #/api/v1/sale_professional_services# with sale_professional_services data values

        :param data: sale_professional_services data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sale_professional_services' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/sale_professional_services# with sale_professional_services data values

        :param data: sale_professional_services data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sale_professional_services' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/sale_professional_services# with sale_professional_services data values

        :param data: sale_professional_services data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sale_professional_services' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/sale_professional_services# with sale_professional_services data values

        :param data: sale_professional_services data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sale_professional_services' + path,
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

    def test_get_sale_professional_services_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=CZ")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=CZ&document_number=0000000088')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        sale_professional_services = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + sale_professional_services[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=CZ&document_number=' + sale_professional_services['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("creationDate", response.json)
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
        response = self.request_get("", "/" + str(sale_professional_services['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("creationDate", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(sale_professional_services['documentHeaderId']) + "/preview?format=P")
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
        sale_professional_services = {'documentDetails': [{'baseValue': 539614.46, 'badgeValue': 0, 'name': '', 'withholdingTax': 3.5, 'code': '', 'detailDate': '2017-05-02T09:16:05.000Z', 'icaPercent': 0, 'disccount': '2.00', 'iva': 16, 'consultItem': True, 'units': 0, 'comments': 'ARADO DE CULTIVO', 'value': 550627, 'withholdingTaxPUCId': 84534, 'otr': '', 'quantity': 100, 'unitValue': '5506.27', 'ivaPUCId': 85778, 'balance': '100.00', 'indexItem': 0}], 'reteICABase': 0, 'currencyId': 4, 'sectionId': 7, 'branchId': 14, 'dependencyId': None, 'total': 603396.88, 'applyCree': True, 'controlNumber': None, 'disccount2': 0, 'thirdId': None, 'costCenterId': 4, 'reteICAValue': 1079.23, 'paymentTermId': 1, 'reteIVAPercent': '3.00', 'documentAffecting': [], 'reteICAPercent': '2.00', 'consumptionTaxValue': 0, 'businessAgentId': None, 'documentNumber': '0000000076', 'disccount2Value': 0, 'shipDepartment': ' VALLE DEL CAUCA ', 'overCost': 0, 'costCenter': None, 'withholdingTaxValue': 18886.51, 'ivaValue': 86338.31, 'overCostTaxBase': 0, 'percentageCREE': 0.3, 'documentDate': '2017-05-02T09:16:05.000Z', 'shipZipCode': None, 'retentionPercent': 0, 'customer': {'branch': '787', 'customerId': 1999, 'name': ' PEÑA TORRES AMADO (1234567891) - PEÑA'}, 'selectedSalesMan': {'name': ' PEÑA TORRES AMADO (1234567891) - PEÑA(AC)', 'type': 'BusinessAgent', 'id': 199}, 'payment': 603396.88, 'reteIVAValue': 2590.15, 'disccount2TaxBase': 0, 'sourceDocumentOrigin': 'CZ', 'valueCREE': 1651.88, 'employeeId': None, 'sourceShortWord': 'CZ', 'dateTo': '2017-05-03T09:16:05.000Z', 'divisionId': 13, 'controlPrefix': None, 'shipAddress': 'CRA 34 # 121- 223', 'shipTo': ' PEÑA TORRES AMADO', 'pucId': 86302, 'shipPhone': None, 'puc': {'name': 'CULTIVO DE CEREALES', 'pucAccount': '410505005', 'quantity': True, 'dueDate': False, 'percentage': 0, 'pucId': 86302}, 'comments': 'ninguno', 'sourceDocumentHeaderId': None, 'baseCREE': 0, 'disccount': 11012.54, 'shipCity': 'CALI ', 'subtotal': 550627, 'reteIVABase': 86338.31, 'retentionPUCId': None, 'termDays': 1, 'shortWord': 'CZ', 'paymentReceipt': {}, 'retentionValue': 0, 'customerId': 1999, 'exchangeRate': 1, 'shipCountry': ' COLOMBIA', 'annuled': None}

        # Envio la creacion del avance sin short word
        sale_professional_services["shortWord"] = None
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        sale_professional_services["shortWord"] = "XY"
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        sale_professional_services["shortWord"] = "CZ"
        # Crea un compra de item con un peso de diferencia en el credit
        sale_professional_services['documentDetails'][0]['value'] = 550627.20
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        sale_professional_services['documentDetails'][0]['value'] = 550627.18
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        sale_professional_services['documentDetails'][0]['value'] = 550627.18
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        # currency = sale_professional_services['currency']
        # # FIXME: podria consultar las monedas y obtener una
        # # Establece una moneda distinta
        # currency2 = {"code": "USD",
        #               "currencyId": 2,
        #               "isDeleted": 0,
        #               "name": "DÓLAR AMERICANO",
        #               "symbol": "$"}
        #
        # sale_professional_services["currency"] = currency2
        # sale_professional_services["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(sale_professional_services)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        # sale_professional_services["currency"] = currency
        # sale_professional_services["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=CZ&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("destinyBranchId", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("puc", response.json)

        sale_professional_services2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(sale_professional_services2)
        print(">>>>> ", purchase_copy['documentDetails'][0]['value'])
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
        self.assertEquals(response.status_code, 201)
        self.assertIn("ok", response.json)
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
        purchase_copy['documentDetails'][0]['value'] = 550627
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # Copio el ultimo de los detalles de pago
        # payment_detail = purchase_copy['withholdingTaxBase']['paymentDetails'][1]
        # Elimino esta posicion del arreglo
        # del purchase_copy['withholdingTaxBase']['paymentDetails'][1]
        # Cambio el valor total del avance
        # purchase_copy['documentDetails'][0]['value'] = 300000
        # Actualiza el compra de item
        # response = self.request_put(purchase_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        # self.assertIn("ok", response.json)

        # Simula un nuevo detalle de pago con base al eliminado
        # payment_detail.pop('paymentDetailId', None)
        # purchase_copy['withholdingTaxBase']['paymentDetails'].append(payment_detail)
        # Cambio el valor total del avance
        purchase_copy['documentDetails'][0]['value'] = 550627
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