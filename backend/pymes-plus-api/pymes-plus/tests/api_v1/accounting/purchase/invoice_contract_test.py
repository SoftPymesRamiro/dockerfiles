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
import uuid

from app import create_app
from app.api_v1 import api

import copy

"""
This module shows various methods and function by allow
handled invoice_contract
"""
class InvoiceContractTest(unittest.TestCase):
    """
    This Class is a  Test Case for invoice_contract API class
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
        """Sent get request to #/api/v1/invoice_contract# with invoice_contract data values

        :param data: invoice_contract data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/invoice_contract' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/invoice_contract# with invoice_contract data values

        :param data: invoice_contract data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/invoice_contract' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/invoice_contract# with invoice_contract data values

        :param data: invoice_contract data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/invoice_contract' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/invoice_contract# with invoice_contract data values

        :param data: invoice_contract data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/invoice_contract' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_invoiceImport(self):
        """
        This function test get a invoice contract according to identifier
        ** First test is correct identifier
        ** Second test is incorrect identifier and validate data
        """
        response = self.request_get('', '/117317')  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        print(">>>> ", response.json)
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')
        self.assertTrue("puc" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentReceiptId" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_invoice_contract_search(self):
        """
        This function test get
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=FT")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")
        self.assertTrue("error" in response.json, 'incorrect response by correct request')
        self.assertTrue("message" in response.json, 'incorrect response by correct request')

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")
        self.assertTrue("error" in response.json, 'incorrect response by correct request')
        self.assertTrue("message" in response.json, 'incorrect response by correct request')

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FT&document_number=0000000003')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        invoice_contract = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + invoice_contract[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FT&document_number=' + invoice_contract['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")
        self.assertTrue("error" in response.json, 'incorrect response by correct request')
        self.assertTrue("message" in response.json, 'incorrect response by correct request')

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404, "")
        self.assertTrue("error" in response.json, 'incorrect response by correct request')
        self.assertTrue("message" in response.json, 'incorrect response by correct request')

        # Peticion correcta
        response = self.request_get("", "/" + str(invoice_contract['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(invoice_contract['documentHeaderId']) + "/preview?format=P")
        # response.json = json.loads(response.data.decode("utf-8"))
        # self.assertEquals(response.status_code, 200)
        # self.assertNotEquals(response, {})
        # self.assertIn("data", response.json)

    ##################################################################################
    def test_post_put_delete(self):
        """
        This function allow create, update and delete a invoice contract
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        contracts = {
            'budget': 90000000.0,
            'isDeleted': 0,
            'costCenterId': 6,
            'creationDate': 'Wed, 16 Sep 2015 09:54:32 GMT',
            'comments': 'TEST AGREEMENT',
            'sectionId': 8,
            'state': True,
            'puc': {
                'percentage': 0.0,
                'name': 'VIAS DE COMUNICACION',
                'companyId': 1,
                'account': '115515005',
                'pucId': 84789
            },
            'providerId': None,
            'pucId': 84789,
            'code': str(uuid.uuid4())[:8],
            'divisionId': 17,
            'description': 'TEST AGREEMENT',
            'dependencyId': None,
            'branchId': 14
        }
        response = self.test_client.post('/api/v1/contracts/',
                                     data=json.dumps(contracts),
                                     content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertIn("contractId", response.json)
        self.contractId = response.json['contractId']

        invoice_contract = {
          "branchId": 14,
          "controlNumber": "0000009999",
          "controlPrefix": "UTST",
          "documentDate": "Thu, 24 Apr 2016 00:00:00 GMT",
          "provider": {
            "address1": "BOGOTA",
            "address2": "",
            "branch": "001",
            "cellPhone": None,
            "city": {
              "cityId": 418,
              "code": "001",
              "department": {
                "code": "11",
                "country": {
                  "countryId": 2,
                  "indicative": "57"
                },
                "departmentId": 3,
                "name": "D.C."
              },
              "indicative": "1",
              "name": "BOGOTA - D.C. - COLOMBIA"
            },
            "cityId": 418,
            "companyId": 1,
            "contactList": [],
            "creditCapacity": 0,
            "fax": None,
            "isDeleted": 0,
            "isLaw1527": False,
            "isMain": True,
            "name": "PRINCIPAL",
            "phone": "5601515",
            "providerId": 286,
            "state": "A",
            "term": 0,
            "thirdPartyId": 1704,
            "zipCode": ""
          },
          "providerId": 286,
          "contractId": self.contractId,
          "paymentTerm": {
            "code": "01",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "interestRate": 0.01,
            "isDeleted": 0,
            "name": "Contado",
            "needTermDays": 0,
            "paymentTermId": 1,
            "promptPayment": 0,
            "quota": 0,
            "quotaNumbers": 0,
            "termDays": 0,
            "updateBy": "ADRIAN",
            "updateDate": "Mon, 05 Sep 2016 11:33:21 GMT"
          },
          "paymentTermId": 1,
          "costCenter": {
            "branchId": 14,
            "code": "00001",
            "costCenterId": 4,
            "divisions": [
              {
                "code": "00001",
                "costCenterId": 4,
                "divisionId": 13,
                "isDeleted": 0,
                "name": "ADMINISTRACION",
                "puc": {
                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                  "percentage": 0,
                  "pucId": 87304
                },
                "pucId": 87304,
                "sections": [
                  {
                    "code": "00043",
                    "dependencies": [],
                    "divisionId": 13,
                    "isDeleted": 0,
                    "name": "F",
                    "puc": None,
                    "pucId": None,
                    "sectionId": 7
                  }
                ]
              },
              {
                "code": "00002",
                "costCenterId": 4,
                "divisionId": 14,
                "isDeleted": 0,
                "name": "VENTAS",
                "puc": {
                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                  "percentage": 0,
                  "pucId": 89100
                },
                "pucId": 89100,
                "sections": []
              }
            ],
            "isDeleted": 0,
            "name": "LEGAQUIMICOS"
          },
          "costCenterId": 4,
          "currency": {
            "code": "USD",
            "currencyId": 2,
            "isDeleted": 0,
            "name": "DÓLAR AMERICANO",
            "symbol": "$"
          },
          "currencyId": 2,
          "exchangeRate": 1,
          "comments": "Esta es una prueba",
          "paymentReceipt": {
            "paymentDetails": [{
                "balance": 15568990.11,
                "paymentType": "EF",
                "state": 1,
                "value": 1160000
              }]
          },
          "pucId": 1462,
          "retentionBase": 1,
          "withholdingTaxBase": 1,
          "withholdingTaxValue": 1,
          "directIVA": 0,
          "directIVAPercent": 0,
          "disccount": 0,
          "disccount2": 0,
          "disccount2Mode": 0,
          "disccount2TaxBase": 0,
          "disccount2Value": 0,
          "disccountPercent": 0,
          "iva": 16,
          "ivaCustomer": 0,
          "ivaPUCId": 85796,
          "documentTypeId":57,
          "shortWord":"FT",
          "accountsBackward": 0,
          "ivaValue": 160000,
          "subtotal":1000000,
          "total":1160000
        }

        # Envio la creacion del avance sin short word
        invoice_contract["shortWord"] = None
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        invoice_contract["shortWord"] = "XY"
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        invoice_contract["shortWord"] = "FT"
        # Crea un compra de item con un peso de diferencia en el credito
        invoice_contract['total'] = 1160000.1
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        invoice_contract['total'] = 1160000
        invoice_contract['paymentReceipt']['paymentDetails'][0]['value'] = 1160000.1
        # Crea un compra de item con un peso de diferencia en el debito
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        invoice_contract['total'] = 1160000
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = invoice_contract['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                     "currencyId": 2,
                     "isDeleted": 0,
                     "name": "DÓLAR AMERICANO",
                     "symbol": "$"}

        invoice_contract["currency"] = currency2
        invoice_contract["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(invoice_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        invoice_contract["currency"] = currency
        invoice_contract["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FT&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        invoice_contract2 = response.json
        response = self.request_put("", "/" + str(self.id) + "/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        invoice_copy = copy.deepcopy(invoice_contract2)
        # Cambio el total
        invoice_copy['total'] = 10
        # Envio a actulizar el compra de item
        response = self.request_put(invoice_copy, "/" + str(self.id))
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
        invoice_copy['total'] = 1160000
        # Realiza un cambio del comentario
        invoice_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(invoice_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Copio el ultimo de los detalles de pago
        payment_detail = invoice_copy['paymentReceipt']['paymentDetails'][0]
        # Elimino esta posicion del arreglo
        del invoice_copy['paymentReceipt']['paymentDetails'][0]
        # Cambio el valor total del avance
        invoice_copy['total'] = 1160000
        # Actualiza el compra de item
        response = self.request_put(invoice_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)

        # Simula un nuevo detalle de pago con base al eliminado
        payment_detail.pop('paymentDetailId', None)
        invoice_copy['paymentReceipt']['paymentDetails'].append(payment_detail)
        # Cambio el valor total del avance
        invoice_copy['total'] = 1160000
        invoice_copy['comments'] = "Este es el test"
        # Actualizo nuevamente
        response = self.request_put(invoice_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Cambio el estado del documento
        invoice_copy['annuled'] = 1
        # Envio a actualizar
        response = self.request_put(invoice_copy, "/" + str(self.id))
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

        self.assertEqual('INVOICE CONTRACT NOT FOUND', response.json['message'].upper(),
                         'incorrect response by bad request')


        response = self.request_delete("", "/" + str(self.contractId))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)