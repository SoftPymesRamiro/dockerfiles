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
handled invoice_asset
"""


class CustomerNoteTest(unittest.TestCase):
    """
    This Class is a  Test Case for invoice_asset API class
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
        """Sent get request to #/api/v1/invoice_asset# with invoice_asset data values

        :param data: invoice_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/customer_notes' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/invoice_asset# with invoice_asset data values

        :param data: invoice_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/customer_notes' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/invoice_asset# with invoice_asset data values

        :param data: invoice_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/customer_notes' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/invoice_asset# with invoice_asset data values

        :param data: invoice_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/customer_notes' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_customer_note(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        # prueba de consulta general
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&'+
                                        'limitDate=2017-06-30&documentNumber=null&controlNumber=null&search=null'+
                                        '&filterBy=None&initTotal=null&endTotal=null&shortWord=NC',
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

    def test_get_customer_note_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=1&short_word=NC")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400, "Failed with invalid params")
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=1&short_word=NC&document_number=0000000018')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        invoice_asset = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=1&short_word=XXXX&document_number=' + invoice_asset[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "Failed in search with invalid short word")
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=1&short_word=NC&document_number=' + invoice_asset['documentNumber'])
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
        response = self.request_get("", "/" + str(invoice_asset['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(invoice_asset['documentHeaderId']) + "/preview?format=P")
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
        customer_note = {"sourceDocumentHeaderId": 5928, "documentNumber": "0000000024", "annuled": None,
                         "controlPrefix": None,
                         "paymentTermId": 2, "documentDate": "2017-06-15T14:53:09.000Z", "controlNumber": None,
                         "sourceDocumentOrigin": "FC",
                         "termDays": 0, "dateTo": None, "costCenter": None, "costCenterId": 1, "divisionId": 1,
                         "sectionId": 1,
                         "exchangeRate": 1, "dependencyId": None, "shortWord": "NC", "sourceShortWord": "NC",
                         "currencyId": 4,
                         "documentDetails": [{"accountNumber": None, "amount": 0, "asset": None, "assetId": None,
                                              "authorizationNumber": None,
                                              "availableStock": 0, "balance": 3, "bankAccountId": None,
                                              "bankCode": None, "bankName": None,
                                              "baseValue": 100, "businessAgentId": None, "cashRegisterId": None,
                                              "checkNumber": None,
                                              "comments": None, "consumptionTaxBase": 0, "consumptionTaxPUC": None,
                                              "consumptionTaxPUCId": None,
                                              "consumptionTaxPercent": 0, "consumptionTaxValue": 0,
                                              "conversionFactor": 0, "cost": 500000,
                                              "costCenterId": None, "createdBy": "Administrador del Sistema",
                                              "creationDate": "Tue, 13 Jun 2017 15:43:24 GMT",
                                              "crossDocumentHeaderId": None,
                                              "customerId": None, "dependencyId": None,
                                              "detailDate": "Tue, 13 Jun 2017 15:25:12 GMT",
                                              "detailDocument": "54321", "detailDocumentTypeId": 42,
                                              "detailPrefix": None,
                                              "detailWarehouseId": None, "disccount": 0, "divisionId": None,
                                              "documentDetailId": 13340,
                                              "documentHeaderId": 5928, "dueDate": None, "employeeId": None,
                                              "finalDate": None,
                                              "financialEntityId": None, "globalTax": 0, "icaPercent": 0,
                                              "importConceptId": None,
                                              "initialDate": None, "interest": 0, "isDeleted": 0, "iva": None,
                                              "ivaCustomer": None,
                                              "ivaPUC": None, "ivaPUCId": None, "kitAssetId": None, "kitItemId": None,
                                              "kitLaborId": None,
                                              "listSerials": [], "mainUnitValue": 0, "measurementUnitId": None,
                                              "otherThirdId": None,
                                              "overCost": 0, "partnerId": None, "payrollConceptId": None,
                                              "payrollEntityId": None,
                                              "percentCost": 0, "physicalLocation": None, "pieceId": None,
                                              "providerId": None, "pucId": 6109,
                                              "quantity": 1, "quantityRefund": 0,
                                              "quoteNumber": None, "reteICA": None, "reteICAPercent": 0, "search": None,
                                              "sectionId": None,
                                              "selected": False, "sourceDocumentDetailId": 13340,
                                              "sourceDocumentNumber": None,
                                              "sourceDocumentPrefix": None, "surcharge": 0,
                                              "thirdId": 181,
                                              "unitValue": 0, "units": 0, "updateBy": "Administrador del Sistema",
                                              "updateDate": "Tue, 13 Jun 2017 15:43:24 GMT", "value": 100,
                                              "withholdingTax": None,
                                              "withholdingTaxPUC": None, "withholdingTaxPUCId": None,
                                              "withholdingValue": 0, "badgeValue": 0,
                                              "valueBefore": 1000000, "consumptionTax": None}], "provider": None,
                         "providerId": None,
                         "disccount": 0, "disccount2": 0, "disccount2TaxBase": 0, "disccount2Value": 0, "ivaValue": 0,
                         "withholdingTaxValue": 0,
                         "subtotal": 100, "retentionValue": 0, "retentionPercent": 0, "retentionPUCId": None,
                         "reteICAValue": 0,
                         "reteICAPercent": 0, "reteIVAValue": 0, "reteIVAPercent": 0, "overCost": 0,
                         "consumptionTaxValue": 0, "valueCREE": 0.4,
                         "applyCree": True, "reteICABase": 0, "reteIVABase": 0, "total": 100, "payment": 100,
                         "percentageCREE": 0.4,
                         "pucId": 6097, "comments": None, "paymentReceipt": {}, "documentAffecting": [],
                         "reference": "0000001043",
                         "sourceDocumentTypeId": 46,
                         "customer": " CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA",
                         "customerId": 1, "shipTo": " CASAÑAS MAYA JULIO CESAR", "shipAddress": "CR 37 10 303",
                         "shipCity": "CALI ",
                         "shipDepartment": " VALLE DEL CAUCA ", "shipCountry": " COLOMBIA", "shipZipCode": "",
                         "shipPhone": "",
                         "selectedSalesMan": "JULIO CESAR CASAÑAS MAYA", "businessAgentId": 2,
                         "sourceDocumentHeader": {"documentDetails": [
                             {"accountNumber": None, "amount": 0, "asset": None, "assetId": None,
                              "authorizationNumber": None,
                              "availableStock": 0, "balance": 3, "bankAccountId": None, "bankCode": None,
                              "bankName": None, "baseValue": 1000000,
                              "businessAgentId": None, "cashRegisterId": None, "checkNumber": None, "comments": None,
                              "consumptionTaxBase": 0,
                              "consumptionTaxPUC": None, "consumptionTaxPUCId": None, "consumptionTaxPercent": 0,
                              "consumptionTaxValue": 0,
                              "conversionFactor": 0, "cost": 500000, "costCenterId": None,
                              "createdBy": "Administrador del Sistema",
                              "creationDate": "Tue, 13 Jun 2017 15:43:24 GMT", "crossDocumentHeaderId": None,
                              "customerId": None,
                              "dependencyId": None, "detailDate": "Tue, 13 Jun 2017 15:25:12 GMT",
                              "detailDocument": "54321",
                              "detailDocumentTypeId": 42, "detailPrefix": None, "detailWarehouseId": None,
                              "disccount": 0, "divisionId": None,
                              "documentDetailId": 13340, "documentHeaderId": 5928, "dueDate": None, "employeeId": None,
                              "finalDate": None,
                              "financialEntityId": None, "globalTax": 0, "icaPercent": 0, "importConceptId": None,
                              "initialDate": None,
                              "interest": 0, "isDeleted": 0, "iva": 0, "ivaCustomer": None, "ivaPUC": None,
                              "ivaPUCId": None, "kitAssetId": None,
                              "kitItemId": None, "kitLaborId": None, "listSerials": [], "mainUnitValue": 0,
                              "measurementUnitId": None,
                              "otherThirdId": None, "overCost": 0, "partnerId": None, "payrollConceptId": None,
                              "payrollEntityId": None,
                              "percentCost": 0, "physicalLocation": None, "pieceId": None, "providerId": None,
                              "pucId": 6109, "quantity": 1, "quantityRefund": 0, "quoteNumber": None, "reteICA": None,
                              "reteICAPercent": 0, "search": None, "sectionId": None, "selected": None,
                              "sourceDocumentDetailId": None,
                              "sourceDocumentNumber": None, "sourceDocumentPrefix": None, "surcharge": 0,
                              "thirdId": 181, "unitValue": 0,
                              "units": 0, "updateBy": "Administrador del Sistema",
                              "updateDate": "Tue, 13 Jun 2017 15:43:24 GMT",
                              "value": 1000000, "withholdingTax": 0, "withholdingTaxPUC": None,
                              "withholdingTaxPUCId": None,
                              "withholdingValue": 0}]}, "branchId": 1}

        # Envio la creacion del avance sin short word
        customer_note["shortWord"] = None
        response = self.request_post(customer_note)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        customer_note["shortWord"] = "XY"
        response = self.request_post(customer_note)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        customer_note["shortWord"] = "NC"
        # # Crea un compra de item con un peso de diferencia en el credit
        # customer_note['documentDetails'][0]['value'] = 9000000
        response = self.request_post(customer_note)
        response.json = json.loads(response.data.decode("utf-8"))

        if "documentNumber" in response.json:
            # Obtengo los datos para despues eliminar
            self.assertIn("documentNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number0 = response.json['documentNumber']
            self.id = response.json['id']

            # Consulta el compra de item
            response = self.request_get('',
                                        '/search?branch_id=1&short_word=NC&document_number=' + self.document_number0)
            self.assertEquals(response.status_code, 200)
            response.json = json.loads(response.data.decode("utf-8"))
            self.assertNotEquals(response.json, {})
            # Verifico algunos de las claves de la respuesta
            self.assertIn("dateFrom", response.json)
            self.assertIn("total", response.json)
            self.assertIn("documentNumber", response.json)
            self.assertIn("disccount2Value", response.json)
            self.assertIn("comments", response.json)

            customer_note2 = response.json
            response = self.request_put("", "/" + str(self.id) + "/preview")
            # *********************UPDATE*************************
            #  Realizo una copia del compra de item consultado
            note_copy = copy.deepcopy(customer_note2)
            # Cambio el total
            note_copy['documentDetails'][0]['value'] = 1000
            # Envio a actulizar el compra de item
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertEquals(response.status_code, 500)
            self.assertIn("message", response.json)
            self.assertIn("Descuadre", response.json['message'])

            # Establece un cambio
            note_copy['documentDetails'][0]['value'] = 100
            note_copy['documentDetails'][0]['comments'] = 'comentarios'
            # Realiza un cambio del comentario
            note_copy['comments'] = "Este es el test"
            # Peticion de actualizado para este avance
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertIn("ok", response.json)

            # Cambio el estado del documento
            note_copy['annuled'] = 1
            # Envio a actualizar
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertIn("ok", response.json)

            # *********************DELETE*************************
            # TODO ESTE METODO NO DEBERIA USARSE DESDE LA VISTA
            # TODO SE AGREGA PARA MANTENER LA COHERENCIA DE LA BD EN PRUEBAS

            response = self.request_delete("", "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta de eliminacion
            self.assertIn("message", response.json)

            response = self.request_delete("", "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            self.assertEquals(response.status_code, 404)

        else:
            self.assertNotEquals(response.json, {})
            self.assertIn("error", response.json)
            self.assertIn("message", response.json)

        # CREACION DE NOTA DEBITO
        response = None
        self.id = None
        customer_note["shortWord"] = "ND"
        response = self.request_post(customer_note)
        response.json = json.loads(response.data.decode("utf-8"))

        if "documentNumber" in response.json:
            # Obtengo los datos para despues eliminar
            self.assertIn("documentNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number0 = response.json['documentNumber']
            self.id = response.json['id']

            # Consulta el compra de item
            response = self.request_get('',
                                        '/search?branch_id=1&short_word=ND&document_number=' + self.document_number0)
            self.assertEquals(response.status_code, 200)
            response.json = json.loads(response.data.decode("utf-8"))
            self.assertNotEquals(response.json, {})
            # Verifico algunos de las claves de la respuesta
            self.assertIn("dateFrom", response.json)
            self.assertIn("total", response.json)
            self.assertIn("documentNumber", response.json)
            self.assertIn("disccount2Value", response.json)
            self.assertIn("comments", response.json)

            customer_note2 = response.json
            # response = self.request_put("", "/" + str(self.id) + "/preview")
            # *********************UPDATE*************************
            #  Realizo una copia del compra de item consultado
            note_copy = None
            note_copy = copy.deepcopy(customer_note2)
            # Cambio el total
            note_copy['documentDetails'][0]['value'] = 1000
            # Envio a actulizar el compra de item
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertEquals(response.status_code, 500)
            self.assertIn("message", response.json)
            self.assertIn("Descuadre", response.json['message'])

            # Establece un cambio
            note_copy['documentDetails'][0]['value'] = 100
            note_copy['documentDetails'][0]['comments'] = 'comentarios'
            # Realiza un cambio del comentario
            note_copy['comments'] = "Este es el test"
            # Peticion de actualizado para este avance
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertIn("ok", response.json)

            # Cambio el estado del documento
            note_copy['annuled'] = 1
            # Envio a actualizar
            response = self.request_put(note_copy, "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta
            self.assertIn("ok", response.json)

            # *********************DELETE*************************
            # TODO ESTE METODO NO DEBERIA USARSE DESDE LA VISTA
            # TODO SE AGREGA PARA MANTENER LA COHERENCIA DE LA BD EN PRUEBAS

            response = self.request_delete("", "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            # Respuesta de eliminacion
            self.assertIn("message", response.json)

            response = self.request_delete("", "/" + str(self.id))
            response.json = json.loads(response.data.decode("utf-8"))
            self.assertEquals(response.status_code, 404)

        else:
            self.assertNotEquals(response.json, {})
            self.assertIn("error", response.json)
            self.assertIn("message", response.json)

