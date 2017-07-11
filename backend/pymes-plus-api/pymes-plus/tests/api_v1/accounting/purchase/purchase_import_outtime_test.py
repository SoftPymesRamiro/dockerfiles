#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 03-03-2017
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
handled invoice_imports
"""
class PurchaseImportOutTimeTest(unittest.TestCase):
    """
    This Class is a  Test Case for invoice_imports API class
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
        """Sent get request to #/api/v1/invoice_imports# with invoice_imports data values

        :param data: invoice_imports data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/purchase_import_out_times'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/invoice_imports# with invoice_imports data values

        :param data: invoice_imports data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/purchase_import_out_times'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/invoice_imports# with invoice_imports data values

        :param data: invoice_imports data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/purchase_import_out_times'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/invoice_imports# with invoice_imports data values

        :param data: invoice_imports data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/purchase_import_out_times'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_invoiceImport(self):
        """
        This function test get a Purchase Item according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.request_get('', '/117456')  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        print(">>> ",response.json)
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentReceipt" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentTermId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_purchase_item_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=FM")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FM&document_number=0000000007')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        purchase_item = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + purchase_item[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FM&document_number=' + purchase_item['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("documentDetails", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {})

        # ################## GET
        response = self.request_get("", "/9999999")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)

        # Peticion correcta
        response = self.request_get("", "/" + str(purchase_item['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("documentDetails", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(purchase_item['documentHeaderId']) + "/preview?format=P")
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
        purchase_item = {
          "branchId": 14,
          "importId":8,
          "controlNumber": "0000005640",
          "controlPrefix": "89",
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
          "contractId": 18,
          "contract":{
              "branchId": 14,
              "budget": 500000000,
              "code": "0002",
              "comments": "QUE VIVA LO FREE PARA QUE ESTAS LICENCIAS",
              "contractId": 18,
              "costCenterId": 4,
              "createdBy": "ADMINISTRADORAA del Sistema",
              "creationDate": "Wed, 31 Aug 2016 08:27:14 GMT",
              "dependencyId": None,
              "description": "LICENCIAS DE MICROSOFT",
              "divisionId": 13,
              "isDeleted": None,
              "providerId": None,
              "puc": {
                "account": "115515005",
                "companyId": 1,
                "name": "EQUIPO DE COMPUTACIÓN Y COMUNICACIÓN",
                "percentage": 0,
                "pucId": 84804
              },
              "pucId": 84804,
              "sectionId": 7,
              "state": False,
              "updateBy": "ADMINISTRADORAA del Sistema",
              "updateDate": "Wed, 31 Aug 2016 08:27:14 GMT"
          },
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
          "documentDetails": [
            {
              "unitValue": 1,
              "quantity": 1,
              "units": 1,
              "baseValue": 2,
              "consumptionTaxBase": 1,
              "withholdingTax": 16,
              "value": 1160000,
              "accountNumber": None,
              "amount": 0,
              "assetId": None,
              "authorizationNumber": None,
              "availableStock": 0,
              "balance": 0,
              "bankAccountId": None,
              "bankCode": None,
              "bankName": None,
              "businessAgentId": None,
              "cashRegisterId": None,
              "checkNumber": None,
              "colorId": None,
              "comments": "Este es un comentario para el detalle",
              "consumptionTaxPUCId": None,
              "consumptionTaxPercent": 0,
              "consumptionTaxValue": 0,
              "conversionFactor": 1,
              "cost": 0,
              "costCenterId": 4,
              "createdBy": "DENNY ORJUELA",
              "creationDate": "Tue, 14 Jan 2014 10:55:43 GMT",
              "crossDocumentHeaderId": None,
              "customerId": None,
              "dependencyId": None,
              "detailDate": "Tue, 14 Jan 2014 10:55:43 GMT",
              "detailDocument": None,
              "detailDocumentTypeId": None,
              "detailPrefix": None,
              "detailWarehouseId": 6,
              "disccount": 0,
              "divisionId": 14,
              "dueDate": None,
              "employeeId": None,
              "finalDate": None,
              "financialEntityId": None,
              "globalTax": 0,
              "icaPercent": 0,
              "importConceptId": 19,
              "initialDate": None,
              "interest": 0,
              "isDeleted": 0,
              "item": {
                "addConsumptionToCost": False,
                "addConsumptionToPurchase": False,
                "addIVAtoCost": False,
                "averageCost": 13742.05377,
                "barCode": "",
                "brandId": None,
                "code": "FENA002",
                "color": False,
                "companyCost": 21220.16,
                "companyId": 1,
                "consumptionPUC": None,
                "consumptionPUCId": None,
                "consumptionPercentage": 0,
                "conversionFactor": 0,
                "conversionFactor2": None,
                "costPUC": {
                  "percentage": 0,
                  "pucAccount": "613550005 VENTA DE QUIMICOS",
                  "pucId": 88508
                },
                "costPUCId": 88508,
                "createdBy": "Migracion",
                "creationDate": "Tue, 10 Dec 2013 14:40:46 GMT",
                "description": "",
                "disccountToUnitValue": False,
                "discountPercentage": 0,
                "imageId": None,
                "incomingPUC": {
                  "percentage": 0,
                  "pucAccount": "413550005 VENTA DE QUIMICOS",
                  "pucId": 86636
                },
                "incomingPUCId": 86636,
                "inventoryGroup": {
                  "inventoryGroupId": 3,
                  "name": "FARMACEUTICOS"
                },
                "inventoryGroupId": 3,
                "inventoryPUC": {
                  "percentage": 0,
                  "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                  "pucId": 84706
                },
                "inventoryPUCId": 84706,
                "invimaDueDate": None,
                "invimaRegister": None,
                "isDeleted": False,
                "itemId": 924,
                "ivaPurchasePUC": {
                  "percentage": 16,
                  "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                  "pucId": 85796
                },
                "ivaPurchasePUCId": 85796,
                "ivaSalePUC": {
                  "percentage": 16,
                  "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                  "pucId": 85778
                },
                "ivaSalePUCId": 85778,
                "lastCost": 13800,
                "lastPurchaseDate": "Mon, 13 Jan 2014 00:00:00 GMT",
                "lot": False,
                "measurementUnit": {
                  "code": "KGM",
                  "measurementUnitId": 32,
                  "name": "KILOGRAMOS                    "
                },
                "measurementUnit2": None,
                "measurementUnit2Id": None,
                "measurementUnit3": None,
                "measurementUnit3Id": None,
                "measurementUnitId": 32,
                "minimumStock": 0,
                "name": "FENACETINA OPACA KL",
                "namePOS": "FENACETINA OPACA KL",
                "orderQuantity": 0,
                "packagePrice": 0,
                "percentageICA": 11.04,
                "percentagePurchaseIVA": 16,
                "percentageSaleIVA": 16,
                "photo": None,
                "plu": "",
                "priceList1": 27586.21,
                "priceList10": 0,
                "priceList2": 0,
                "priceList3": 0,
                "priceList4": 0,
                "priceList5": 0,
                "priceList6": 0,
                "priceList7": 0,
                "priceList8": 0,
                "priceList9": 0,
                "priceListA1": 0,
                "priceListA10": 0,
                "priceListA2": 0,
                "priceListA3": 0,
                "priceListA4": 0,
                "priceListA5": 0,
                "priceListA6": 0,
                "priceListA7": 0,
                "priceListA8": 0,
                "priceListA9": 0,
                "priceListB1": None,
                "priceListB10": None,
                "priceListB2": None,
                "priceListB3": None,
                "priceListB4": None,
                "priceListB5": None,
                "priceListB6": None,
                "priceListB7": None,
                "priceListB8": None,
                "priceListB9": None,
                "providerId": None,
                "purchaseIVA": {
                  "code": "G",
                  "ivaId": 2,
                  "name": "GRAVADO"
                },
                "purchaseIVAId": 2,
                "reference": "",
                "saleIVA": {
                  "code": "G",
                  "ivaId": 2,
                  "name": "GRAVADO"
                },
                "saleIVAId": 2,
                "serial": False,
                "size": False,
                "state": "A",
                "subInventoryGroup1Id": None,
                "subInventoryGroup2": None,
                "subInventoryGroup2Id": None,
                "subInventoryGroup3": None,
                "subInventoryGroup3Id": None,
                "subInventoryGroups1": None,
                "typeItem": "A",
                "updateBy": "ADA LUZ LEGUIZAMON FUENTES",
                "updateDate": "Mon, 13 Jan 2014 09:38:31 GMT",
                "weight": 0,
                "withholdingICA": False,
                "withholdingPurchasePercentage": 3.5,
                "withholdingSalePercentage": 0,
                "withholdingTaxPurchasePUC": {
                  "percentage": 3.5,
                  "pucAccount": "236540005 COMPRAS 3.5%",
                  "pucId": 85677
                },
                "withholdingTaxPurchasePUCId": 85677,
                "withholdingTaxSalePUC": {
                  "percentage": 0,
                  "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                  "pucId": 84520
                },
                "withholdingTaxSalePUCId": 84520
              },
              "itemId": 924,
              "iva": 16,
              "ivaCustomer": 0,
              "ivaPUCId": 85796,
              "kitAssetId": None,
              "kitItemId": None,
              "kitLaborId": None,
              "listSerials": [],
              "lot": "",
              "mainUnitValue": 0,
              "measurementUnitId": 32,
              "otherThirdId": None,
              "overCost": 0,
              "partnerId": None,
              "payrollConceptId": None,
              "payrollEntityId": None,
              "percentCost": 0,
              "physicalLocation": "",
              "pieceId": None,
              "providerId": None,
              "pucId": None,
              "quantityRefund": 0,
              "quoteNumber": 0,
              "reteICA": 0,
              "reteICAPercent": 0,
              "sectionId": None,
              "selected": 0,
              "sizeId": None,
              "sourceDocumentDetailId": None,
              "sourceDocumentNumber": None,
              "sourceDocumentPrefix": None,
              "sourceDocumentTypeId": None,
              "surcharge": 0,
              "thirdId": None,
              "updateBy": "DENNY ORJUELA",
              "updateDate": "Tue, 14 Jan 2014 10:55:43 GMT",
              "withholdingTaxPUCId": 85675,
              "withholdingValue": 0
            }
          ],
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
          "overCost": 0,
          "disccount2": 0,
          "disccount2Mode": 0,
          "disccount2TaxBase": 0,
          "disccount2Value": 0,
          "disccountPercent": 0,
          "iva": 16,
          "ivaCustomer": 0,
          "ivaPUCId": 85796,
          "documentTypeId":46,
          "shortWord":"FM",
          "accountsBackward": 0,
          "ivaValue": 160000,
          "subtotal":1000000,
          "total":1160000
        }

        # Envio la creacion del avance sin short word
        purchase_item["shortWord"] = None
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        purchase_item["shortWord"] = "XY"
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        purchase_item["shortWord"] = "FM"
        # Crea un compra de item con un peso de diferencia en el credito
        purchase_item['documentDetails'][0]['value'] = 1160000.1
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))

        print("response.json>> ", response.json)
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        purchase_item['documentDetails'][0]['value'] = 1160000
        purchase_item['paymentReceipt']['paymentDetails'][0]['value'] = 1160000.1
        # Crea un compra de item con un peso de diferencia en el debito
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        purchase_item['documentDetails'][0]['value'] = 1160000
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = purchase_item['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                     "currencyId": 2,
                     "isDeleted": 0,
                     "name": "DÓLAR AMERICANO",
                     "symbol": "$"}

        purchase_item["currency"] = currency2
        purchase_item["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(purchase_item)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        purchase_item["currency"] = currency
        purchase_item["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FM&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        purchase_item2 = response.json
        response = self.request_put("", "/" + str(self.id) + "/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(purchase_item2)
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
        purchase_copy['documentDetails'][0]['value'] = 1160000
        purchase_item['paymentReceipt']['paymentDetails'][0]['value'] = 1160000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        purchase_copy['shortWord'] = "FM"
        print(">>> ", purchase_copy)
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Copio el ultimo de los detalles de pago
        payment_detail = purchase_copy['paymentReceipt']['paymentDetails'][0]
        # Elimino esta posicion del arreglo
        del purchase_copy['paymentReceipt']['paymentDetails'][0]
        # Cambio el valor total del avance
        purchase_copy['documentDetails'][0]['value'] = 1000000
        purchase_copy['shortWord']= "FM"
        # Actualiza el compra de item
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertIn("status", response.json)

        # Simula un nuevo detalle de pago con base al eliminado
        payment_detail.pop('paymentDetailId', None)
        purchase_copy['paymentReceipt']['paymentDetails'].append(payment_detail)
        # Cambio el valor total del avance
        purchase_copy['documentDetails'][0]['value'] = 1160000
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

        self.assertEqual('PURCHASE IMPORT OUT TIME NOT FOUND', response.json['message'].upper(),
                         'incorrect response by bad request')