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
class SaleAssetTest(unittest.TestCase):
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
        return self.test_client.get('/api/v1/sale_invoice_assets' + path,
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
        return self.test_client.post('/api/v1/sale_invoice_assets' + path,
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
        return self.test_client.put('/api/v1/sale_invoice_assets' + path,
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
        return self.test_client.delete('/api/v1/sale_invoice_assets' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_purchase_aiu(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        # prueba de consulta general
        response = self.test_client.get('/api/v1/document_headers/search?branchId=1&startDate=2017-06-01&'+
                                        'limitDate=2017-06-30&documentNumber=null&controlNumber=null&search=null'+
                                        '&filterBy=None&initTotal=null&endTotal=null&shortWord=FA',
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

    def test_get_invoice_asset_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=1&short_word=FC")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=1&short_word=FC&document_number=0000000042')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        invoice_asset = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=1&short_word=XXXX&document_number=' + invoice_asset[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=1&short_word=FC&document_number=' + invoice_asset['documentNumber'])
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
        invoice_asset = {'branchId': 1, 'exchangeRate': 1, 'dependencyId': None, 'reteIVABase': 0, 'consumptionTaxPercent': 0, 'divisionId': 1, 'ivaValue': 0, 'withholdingTaxPUCId': None, 'customer': {'branch': '110', 'customerId': 1, 'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA'}, 'ivaBase': 9000000, 'employeeId': None, 'reteICABase': 0, 'dateTo': None, 'shipCountry': ' COLOMBIA', 'thirdId': None, 'disccount2': 0, 'customerId': 1, 'withholdingTaxValue': 0, 'disccount2Value': 0, 'overCost': 0, 'retentionPUCId': None, 'withholdingTaxBase': 9000000, 'documentAffecting': [], 'total': 9000000, 'controlNumber': None, 'ivaPUC': None, 'annuled': None, 'controlPrefix': None, 'withholdingTaxPUC': None, 'selectedSalesMan': {'id': 2, 'name': ' CASAÑAS MAYA JULIO CESAR (94391607) - JULIO CESAR CASAÑAS MAYA(AC)', 'type': 'BusinessAgent'}, 'shipAddress': 'CR 37 10 303', 'documentDetails': [{'withholdingTax': 0, 'icaPercent': 0, 'assetId': 28, 'iva': 0, 'detailDate': '2017-06-12T08:33:28.000Z', 'consultItem': True, 'unitValue': 0, 'baseValue': 9000000, 'quantity': 1, 'value': 9000000, 'badgeValue': 0, 'indexItem': 0, 'units': 0, 'disccount': 0, 'asset': {'branchId': 1, 'percentageResidual': 0, 'dependencyId': None, 'assetGroupId': None, 'isDeleted': 0, 'assetId': 28, 'divisionId': 7, 'chassisSerial': None, 'model': None, 'landArea': 0, 'propertyNumber': None, 'city': {'department': {'departmentId': 24, 'country': {'countryId': 1, 'indicative': '57'}, 'name': 'VALLE DEL CAUCA', 'code': '76'}, 'name': 'CALI - VALLE DEL CAUCA - COLOMBIA', 'cityId': 824, 'indicative': '2', 'code': '001'}, 'puc': {'pucId': 6714, 'name': 'URBANOS', 'account': '150405005'}, 'typeAsset': 'I', 'depreciationMonth': 2, 'purchaseDate': 'Wed, 24 May 2017 20:58:27 GMT', 'updateDate': 'Wed, 24 May 2017 15:59:57 GMT', 'updateBy': 'Administrador del Sistema', 'depreciationYear': 11, 'plate': None, 'depreciationYearNIIF': 0, 'engineSerial': None, 'logoConvert': '', 'depreciationMonthNIIF': 0, 'notary': None, 'percentageSaving': 0, 'name': 'ACTIVO 001', 'state': 'A', 'cityId': 824, 'address': None, 'creationDate': 'Wed, 24 May 2017 15:59:09 GMT', 'dateNotarialDocument': 'Wed, 24 May 2017 20:58:27 GMT', 'comments': None, 'builtArea': 0, 'notarialDocument': None, 'costCenterId': 4, 'costHour': 0, 'sectionId': 7, 'imageId': None, 'code': 'AF001', 'netValueNIIF': 0, 'pucId': 6714, 'line': None, 'createdBy': 'Administrador del Sistema', 'rentable': False}}], 'payment': 9000000, 'disccount': 0, 'ivaPUCId': None, 'billingResolutionId': 1, 'shipTo': ' CASAÑAS MAYA JULIO CESAR', 'reteIVAPercent': 0, 'paymentTermId': 2, 'applyCree': True, 'reteIVAValue': 0, 'costCenterId': 1, 'shipZipCode': '', 'documentDate': '2017-06-12T08:33:28.000Z', 'withholdingTaxPercent': 0, 'valueCREE': 36000, 'shipPhone': '', 'comments': None, 'freight': 0, 'retentionPercent': 0, 'ivaPercent': 0, 'sourceDocumentHeaderId': None, 'currencyId': 4, 'paymentReceipt': {}, 'reteICAValue': 0, 'reteICAPercent': 0, 'sectionId': 1, 'sourceDocumentOrigin': 'FA', 'sourceShortWord': 'FA', 'disccount2TaxBase': 0, 'consumptionTaxValue': 0, 'subtotal': 9000000, 'shortWord': 'FC', 'costCenter': None, 'percentageCREE': 0.4, 'documentNumber': '0000001017', 'baseCREE': 0, 'businessAgentId': 2, 'overCostTaxBase': 0, 'shipCity': 'CALI ', 'retentionValue': 0, 'termDays': 0, 'shipDepartment': ' VALLE DEL CAUCA '}
        # Envio la creacion del avance sin short word
        invoice_asset["shortWord"] = None
        response = self.request_post(invoice_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        invoice_asset["shortWord"] = "XY"
        response = self.request_post(invoice_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        invoice_asset["shortWord"] = "FC"
        # Crea un compra de item con un peso de diferencia en el credit
        invoice_asset['documentDetails'][0]['value'] = 9000000
        response = self.request_post(invoice_asset)
        response.json = json.loads(response.data.decode("utf-8"))

        print(">>>>>> ",invoice_asset)
        if "controlNumber" in response.json:
            # Obtengo los datos para despues eliminar
            self.assertIn("controlNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number0 = response.json['documentNumber']
            self.id0 = response.json['id']

            # Restaura el valor del avance
            invoice_asset['documentDetails'][0]['value'] = 9000000
            # Crea un compra de item con un peso de diferencia en el debit
            response = self.request_post(invoice_asset)
            response.json = json.loads(response.data.decode("utf-8"))
            # Obtengo los datos para despues eliminar
            self.assertIn("documentNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number0a = response.json['documentNumber']
            self.id0a = response.json['id']

            # Crea un compra de item correcto con valor exacto
            invoice_asset['documentDetails'][0]['value'] = 9000000.18
            response = self.request_post(invoice_asset)
            response.json = json.loads(response.data.decode("utf-8"))

            self.assertIn("documentNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number = response.json['documentNumber']
            self.id = response.json['id']
            # TODO: la moneda por defecto podria no ser el peso
            # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
            currency = invoice_asset['currency']
            # FIXME: podria consultar las monedas y obtener una
            # Establece una moneda distinta
            currency2 = {"code": "USD",
                          "currencyId": 2,
                          "isDeleted": 0,
                          "name": "DÓLAR AMERICANO",
                          "symbol": "$"}

            invoice_asset["currency"] = currency2
            invoice_asset["currencyId"] = 2
            # Crea el compra de item con una moneda extranjera
            response = self.request_post(invoice_asset)
            response.json = json.loads(response.data.decode("utf-8"))
            # Guarda los datos de este avance para la posterior eliminacion
            self.assertIn("documentNumber", response.json)
            self.assertIn("id", response.json)
            self.document_number2 = response.json['documentNumber']
            self.id2 = response.json['id']
            # Reestablece la moneda actual
            invoice_asset["currency"] = currency
            invoice_asset["currencyId"] = 4

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

            invoice_asset2 = response.json
            response = self.request_put("", "/"+str(self.id)+"/preview")
            # *********************UPDATE*************************
            #  Realizo una copia del compra de item consultado
            purchase_copy = copy.deepcopy(invoice_asset2)
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

            self.assertEqual('SALE ITEM NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')

        else:
            self.assertNotEquals(response.json, {})
            self.assertIn("error", response.json)
            self.assertIn("message", response.json)
