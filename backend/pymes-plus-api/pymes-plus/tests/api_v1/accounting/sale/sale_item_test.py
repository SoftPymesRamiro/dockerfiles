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
handled invoice_sale_item
"""
class InvoiceSaleItemTest(unittest.TestCase):
    """
    This Class is a  Test Case for invoice_sale_item API class
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
        """Sent get request to #/api/v1/invoice_sale_item# with invoice_sale_item data values

        :param data: invoice_sale_item data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/invoice_sale_item' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/invoice_sale_item# with invoice_sale_item data values

        :param data: invoice_sale_item data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/invoice_sale_item' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/invoice_sale_item# with invoice_sale_item data values

        :param data: invoice_sale_item data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/invoice_sale_item' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/invoice_sale_item# with invoice_sale_item data values

        :param data: invoice_sale_item data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/invoice_sale_item' + path,
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

    def test_get_invoice_sale_item_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=FC")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FC&document_number=0000000042')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        invoice_sale_item = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + invoice_sale_item[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 404)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FP&document_number=' + invoice_sale_item['documentNumber'])
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
        response = self.request_get("", "/" + str(invoice_sale_item['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("documentNumber", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(invoice_sale_item['documentHeaderId']) + "/preview?format=P")
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
        invoice_sale_item = {
            "thirdId": None,
            "billingResolutionId": None,
            "sourceDocument": None,
            "vacation": 0,
            "bonusDateFrom": None,
            "costCenterId": 4,
            "customerId": None,
            "sourcePrefix": None,
            "retentionBase": None,
            "baseCREE": 0,
            "interest": None,
            "epsValue": None,
            "financialEntityId": None,
            "disccount": 11012.54,
            "consumptionTaxBase": 0,
            "puc": None,
            "checks": None,
            "source": {
              "isDeleted": 0,
              "createdBy": "Migracion",
              "needResolution": 0,
              "isIncomePayment": None,
              "name": "FACTURA DE PROVEEDOR",
              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
              "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
              "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider",
              "updateBy": "011",
              "comments": None,
              "documentTypeId": 49,
              "shortWord": "FP"
            },
            "reteICAValue": 0,
            "assetId": None,
            "employeeId": None,
            "disccountPercent": None,
            "workNumber": None,
            "partner": None,
            "retentionValue": 10468.52,
            "exchangeRate": 1,
            "updateBy": "ADMINISTRADOR UPDATE del Sistema",
            "payrollBasicId": None,
            "directIVAPercent": None,
            "reteICAPercent": 0,
            "reteICABase": 0,
            "divisionId": 13,
            "productionOrderId": None,
            "accountsBackward": 0,
            "consumptionTaxPercent": None,
            "contractId": None,
            "stageCostTotal": None,
            "cash": None,
            "quotaNumbers": 0,
            "revolvingFund": 0,
            "retentionPercent": 2,
            "orderNumber": None,
            "daysPILA": None,
            "freezeBill": 0,
            "finalDate": None,
            "reteIVAPUCId": None,
            "payrollPaymentType": None,
            "cutNumber": None,
            "auxCharacterTwo": None,
            "afpValue": None,
            "controlNumber": "23232323",
            "section": {
              "isDeleted": 0,
              "divisionId": 13,
              "createdBy": "ADMINISTRADOR",
              "dependencies": [],
              "name": "F",
              "updateBy": "ADMINISTRADOR",
              "creationDate": "Fri, 18 Sep 2015 14:44:05 GMT",
              "updateDate": "Fri, 18 Sep 2015 14:44:05 GMT",
              "pucId": None,
              "sectionId": 7,
              "code": "00043",
              "puc": None,
              "expenses": None
            },
            "termDays": 0,
            "daysEnjoy": None,
            "initialDate": None,
            "paymentBy": "0",
            "prefix": None,
            "periodicityQuota": None,
            "third": None,
            "daysNet": None,
            "addToPayroll": None,
            "pucId": None,
            "balance": None,
            "documentDate": "2017-03-29T09:51:35.000Z",
            "ivaPUCId": None,
            "paymentTerm": {
              "needTermDays": 1,
              "isDeleted": 0,
              "createdBy": "Migracion",
              "promptPayment": 0,
              "quota": 0,
              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
              "updateDate": "Mon, 05 Sep 2016 11:33:21 GMT",
              "name": "Credito",
              "termDays": 0,
              "quotaNumbers": 0,
              "updateBy": "ADRIAN",
              "interestRate": 0.01,
              "code": "02",
              "paymentTermId": 2
            },
            "ivaPUC": None,
            "pettyCash": 0,
            "withholdingTaxPUCId": None,
            "provider": {
              "branch": "789",
              "thirdPartyId": 2394,
              "thirdParty": {
                "lastName": "PENA",
                "isDeleted": False,
                "identificationType": {
                  "isDeleted": 0,
                  "createdBy": "Migracion",
                  "updateBy": "Migracion",
                  "name": "Cedula de Ciudadania",
                  "identificationTypeDian": "13",
                  "creationDate": "Fri, 17 Aug 2012 10:34:53 GMT",
                  "code": "C",
                  "identificationTypeId": 1
                },
                "identificationDV": "6",
                "alternateIdentification": None,
                "tradeName": None,
                "economicActivity": {
                  "updateDate": "Mon, 24 Jun 2013 01:02:07 GMT",
                  "createdBy": "CREE",
                  "economicActivityId": 329,
                  "updateBy": "CREE",
                  "name": "Edición de programas de informática (software)",
                  "creationDate": "Mon, 24 Jun 2013 01:02:07 GMT",
                  "code": "5820",
                  "percentage": 0.6
                },
                "ivaTypeId": 1,
                "updateDate": "Tue, 03 Jan 2017 15:37:43 GMT",
                "secondName": None,
                "retirementDate": None,
                "entryDate": "Tue, 03 Jan 2017 15:33:54 GMT",
                "isSelfRetainer": False,
                "image": None,
                "webPage": "jeffersonamado.com.co",
                "thirdPartyId": 2394,
                "identificationNumber": "56403",
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "rut": False,
                "firstName": "JEFFERSON AMADO",
                "isGreatTaxPayer": False,
                "creationDate": "Tue, 03 Jan 2017 15:37:43 GMT",
                "thirdType": "N",
                "isWithholdingCREE": False,
                "isSelfRetainerICA": False,
                "imageId": None,
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "comments": "JAPETO STYLE",
                "economicActivityId": 329,
                "maidenName": "TORRES",
                "state": "A",
                "identificationTypeId": 1
              },
              "name": " PENA TORRES JEFFERSON AMADO (56403) - ASESORES JPT",
              "providerId": 532,
              "isWithholdingCREE": 0
            },
            "subtotal": 550627.18,
            "vacationDateFrom": None,
            "division": {
              "isDeleted": 0,
              "divisionId": 13,
              "createdBy": "DENNY ORJUELA",
              "costCenterId": 4,
              "name": "ADMINISTRACION",
              "pucId": 87304,
              "creationDate": "Wed, 14 Aug 2013 10:42:14 GMT",
              "updateDate": "Fri, 24 Mar 2017 09:45:20 GMT",
              "sections": [
                {
                  "isDeleted": 0,
                  "divisionId": 13,
                  "createdBy": "ADMINISTRADOR",
                  "dependencies": [],
                  "name": "F",
                  "updateBy": "ADMINISTRADOR",
                  "creationDate": "Fri, 18 Sep 2015 14:44:05 GMT",
                  "updateDate": "Fri, 18 Sep 2015 14:44:05 GMT",
                  "pucId": None,
                  "sectionId": 7,
                  "code": "00043",
                  "puc": None,
                  "expenses": None
                }
              ],
              "updateBy": "ADMINISTRADOR UPDATE del Sistema",
              "code": "00001",
              "puc": {
                "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                "pucAccount": "510000000",
                "pucId": 87304,
                "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                "percentage": 0
              },
              "expenses": "Cuenta 51"
            },
            "sourceDocumentType": None,
            "sanction": None,
            "documentHeaderId": None,
            "tipValue": 0,
            "costCenter": {
              "divisions": [
                {
                  "isDeleted": 0,
                  "divisionId": 13,
                  "createdBy": "DENNY ORJUELA",
                  "costCenterId": 4,
                  "name": "ADMINISTRACION",
                  "pucId": 87304,
                  "creationDate": "Wed, 14 Aug 2013 10:42:14 GMT",
                  "updateDate": "Fri, 24 Mar 2017 09:45:20 GMT",
                  "sections": [
                    {
                      "isDeleted": 0,
                      "divisionId": 13,
                      "createdBy": "ADMINISTRADOR",
                      "dependencies": [],
                      "name": "F",
                      "updateBy": "ADMINISTRADOR",
                      "creationDate": "Fri, 18 Sep 2015 14:44:05 GMT",
                      "updateDate": "Fri, 18 Sep 2015 14:44:05 GMT",
                      "pucId": None,
                      "sectionId": 7,
                      "code": "00043",
                      "puc": None,
                      "expenses": None
                    }
                  ],
                  "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                  "code": "00001",
                  "puc": {
                    "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                    "pucAccount": "510000000",
                    "pucId": 87304,
                    "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                    "percentage": 0
                  },
                  "expenses": "Cuenta 51"
                },
                {
                  "isDeleted": 0,
                  "divisionId": 14,
                  "createdBy": "Administrador del Sistema",
                  "costCenterId": 4,
                  "name": "VENTAS",
                  "pucId": 5365,
                  "creationDate": "Fri, 23 Aug 2013 11:39:40 GMT",
                  "updateDate": "Tue, 21 Mar 2017 14:34:12 GMT",
                  "sections": [],
                  "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                  "code": "00002",
                  "puc": {
                    "name": "COSTOS DE PRODUCCIÓN - CONTRATOS DE SERVICIOS",
                    "pucAccount": "740000000",
                    "pucId": 5365,
                    "account": "740000000 COSTOS DE PRODUCCIÓN - CONTRATOS DE SERVICIOS",
                    "percentage": 0
                  },
                  "expenses": "Cuenta 74"
                }
              ],
              "branchId": 14,
              "createdBy": "DENNY ORJUELA",
              "costCenterId": 4,
              "updateBy": "Administrador del Sistema",
              "name": "LEGAQUIMICOS",
              "creationDate": "Wed, 14 Aug 2013 10:41:52 GMT",
              "code": "00001",
              "isDeleted": 0,
              "updateDate": "Fri, 23 Aug 2013 11:37:13 GMT"
            },
            "assumedIVA": 0,
            "dependency": None,
            "otherThirdId": None,
            "shipTo": None,
            "percentageCREE": 0,
            "productionUnits": None,
            "ivaPercent": None,
            "updateDate": "Wed, 29 Mar 2017 10:49:49 GMT",
            "shipPhone": None,
            "documentTypeConsign": None,
            "employee": None,
            "cashRegisterId": None,
            "daysWorked": None,
            "dateFrom": None,
            "inability": 0,
            "month": None,
            "auxCharacterOne": None,
            "createdBy": "ADMINISTRADOR UPDATE del Sistema",
            "total": 627747.6,
            "overCost": 10000,
            "financialEntity": None,
            "dateTo": "2017-03-29T09:51:35.000Z",
            "bonus": 0,
            "retirement": None,
            "realSimulated": None,
            "insurance": None,
            "advanceLayoff": 0,
            "stageId": None,
            "sourceShortWord": "FP",
            "shipAddress": None,
            "ivaBase": None,
            "withholdingTaxValue": 18319.92,
            "printed": 0,
            "sourceDocumentHeaderId": None,
            "baseType": None,
            "auxTimeOne": None,
            "auxTimeTwo": None,
            "sourceDocumentTypeId": None,
            "retentionMode": 0,
            "depositNumber": None,
            "initialQuota": 0,
            "documentType": {
              "isDeleted": 0,
              "createdBy": "Migracion",
              "needResolution": 0,
              "isIncomePayment": None,
              "name": "FACTURA DE PROVEEDOR",
              "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
              "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
              "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider",
              "updateBy": "011",
              "comments": None,
              "documentTypeId": 49,
              "shortWord": "FP"
            },
            "interestPUCId": None,
            "paymentReceipt": {},
            "daysLicensed": None,
            "shipDepartment": None,
            "firtsContractDate": None,
            "shipCountry": None,
            "documentDetails": [
              {
                "thirdId": None,
                "unitValue": 5506.2718,
                "quantityRefund": None,
                "authorizationNumber": None,
                "mainUnitValue": None,
                "customerId": None,
                "lot": None,
                "divisionId": 13,
                "interest": None,
                "selected": None,
                "financialEntityId": None,
                "disccount": 2,
                "pucId": None,
                "measurementUnits": [
                  {
                    "name": "CUARTO DE LIBRA               ",
                    "code": "CTO",
                    "measurementUnitId": 49
                  },
                  {
                    "name": "UNIDADES                      ",
                    "code": "UNI",
                    "measurementUnitId": 36
                  },
                  {
                    "name": "ONZA                          ",
                    "code": "ONZ",
                    "measurementUnitId": 44
                  }
                ],
                "iva": 16,
                "detailDocumentTypeId": 49,
                "puc": None,
                "third": None,
                "documentDetailId": 306749,
                "color": False,
                "assetId": None,
                "employeeId": None,
                "name": "ACEITE DE AGUACATE X 125 GR",
                "reteICA": None,
                "kitAssetId": None,
                "bankAccountId": None,
                "detailPrefix": None,
                "measurementUnitId": 49,
                "reteICAPercent": None,
                "isDeleted": 0,
                "consumptionTaxPUCId": None,
                "payrollConceptId": None,
                "consumptionTaxPercent": 8,
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "quoteNumber": None,
                "size": False,
                "conversionFactor": 1,
                "partnerId": None,
                "consumptionTaxBase": 523426.2000000001,
                "dependencyId": None,
                "listSerials": [],
                "ivaCustomer": None,
                "sizeId": None,
                "finalDate": None,
                "withholdingValue": None,
                "units": 100,
                "kitItemId": None,
                "bankName": None,
                "detailWarehouseId": 6,
                "percentCost": None,
                "cost": None,
                "itemId": 24,
                "accountNumber": None,
                "initialDate": None,
                "sourceDocumentTypeId": None,
                "dueDate": None,
                "value": 550627.2,
                "item": {
                  "addConsumptionToPurchase": True,
                  "priceListA7": 0,
                  "lastCost": 0,
                  "priceList5": 0,
                  "name": "ACEITE DE AGUACATE X 125 GR",
                  "priceListA2": 0,
                  "typeItem": "A",
                  "disccountToUnitValue": False,
                  "priceListA6": 0,
                  "subInventoryGroup2Id": None,
                  "priceListB6": 0,
                  "subInventoryGroup3Id": None,
                  "packagePrice": 0,
                  "priceList8": 0,
                  "creationDate": "Tue, 10 Dec 2013 14:40:27 GMT",
                  "consumptionPUC": {
                    "pucAccount": "246205010 IMPUESTO AL CONSUMO 8%",
                    "pucId": 85858,
                    "percentage": 8
                  },
                  "priceListB3": 0,
                  "measurementUnit3Id": 44,
                  "plu": "123123 1",
                  "measurementUnit3": {
                    "name": "ONZA                          ",
                    "code": "ONZ",
                    "measurementUnitId": 44
                  },
                  "subInventoryGroup3": None,
                  "inventoryGroupId": 9,
                  "priceList6": 0,
                  "percentageICA": 11.04,
                  "priceListA9": 0,
                  "photo": None,
                  "priceListB2": 0,
                  "inventoryGroup": {
                    "name": "COSMETICOS",
                    "inventoryGroupId": 9
                  },
                  "priceList3": 0,
                  "reference": "321321",
                  "priceListA1": 50,
                  "incomingPUC": {
                    "pucAccount": "413550005 VENTA DE QUIMICOS",
                    "pucId": 86636,
                    "percentage": 0
                  },
                  "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                  "consumptionPercentage": 8,
                  "percentageSaleIVA": 16,
                  "inventoryPUC": {
                    "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                    "pucId": 84706,
                    "percentage": 0
                  },
                  "measurementUnitId": 49,
                  "inventoryPUCId": 84706,
                  "isDeleted": False,
                  "ivaSalePUCId": 85778,
                  "priceListB5": 0,
                  "withholdingTaxPurchasePUCId": 85677,
                  "consumptionPUCId": 85858,
                  "priceList4": 0,
                  "size": False,
                  "conversionFactor": 10,
                  "measurementUnit": {
                    "name": "CUARTO DE LIBRA               ",
                    "code": "CTO",
                    "measurementUnitId": 49
                  },
                  "costPUC": {
                    "pucAccount": "613550005 VENTA DE QUIMICOS",
                    "pucId": 88508,
                    "percentage": 0
                  },
                  "incomingPUCId": 86636,
                  "addConsumptionToCost": False,
                  "orderQuantity": 0,
                  "saleIVA": {
                    "name": "GRAVADO",
                    "ivaId": 2,
                    "code": "G"
                  },
                  "purchaseIVA": {
                    "name": "GRAVADO",
                    "ivaId": 2,
                    "code": "G"
                  },
                  "purchaseIVAId": 2,
                  "measurementUnit2": {
                    "name": "UNIDADES                      ",
                    "code": "UNI",
                    "measurementUnitId": 36
                  },
                  "addIVAtoCost": False,
                  "withholdingTaxPurchasePUC": {
                    "pucAccount": "236540005 COMPRAS 3.5%",
                    "pucId": 85677,
                    "percentage": 3.5
                  },
                  "barCode": "123456",
                  "percentagePurchaseIVA": 16,
                  "itemId": 24,
                  "priceList9": 0,
                  "withholdingSalePercentage": 0,
                  "state": "A",
                  "ivaSalePUC": {
                    "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                    "pucId": 85778,
                    "percentage": 16
                  },
                  "conversionFactor2": 506,
                  "withholdingTaxSalePUCId": 84520,
                  "priceList10": 0,
                  "withholdingPurchasePercentage": 3.5,
                  "priceListB4": 0,
                  "priceListB1": 501,
                  "discountPercentage": 0,
                  "priceListA4": 0,
                  "withholdingICA": False,
                  "priceListB10": 0,
                  "code": "AC001",
                  "priceListA8": 0,
                  "invimaRegister": None,
                  "namePOS": "ACEITE DE AGUACATE X 125 GR",
                  "companyId": 1,
                  "averageCost": 5506.271765,
                  "costPUCId": 88508,
                  "minimumStock": 0,
                  "lot": False,
                  "saleIVAId": 2,
                  "priceListB8": 0,
                  "serial": False,
                  "subInventoryGroup2": None,
                  "invimaDueDate": None,
                  "brandId": 8,
                  "priceList1": 120,
                  "measurementUnit2Id": 36,
                  "priceListA10": 0,
                  "ivaPurchasePUCId": 85796,
                  "priceListB9": 0,
                  "updateDate": "Mon, 10 Oct 2016 15:00:59 GMT",
                  "withholdingTaxSalePUC": {
                    "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                    "pucId": 84520,
                    "percentage": 0
                  },
                  "subInventoryGroups1": None,
                  "priceList2": 0,
                  "providerId": None,
                  "color": False,
                  "weight": 0,
                  "createdBy": "Migracion",
                  "lastPurchaseDate": "Sat, 29 Dec 1900 05:00:00 GMT",
                  "companyCost": 5636.6,
                  "imageId": None,
                  "priceList7": 0,
                  "ivaPurchasePUC": {
                    "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                    "pucId": 85796,
                    "percentage": 16
                  },
                  "priceListA3": 0,
                  "description": "",
                  "priceListB7": 0,
                  "subInventoryGroup1Id": None,
                  "priceListA5": 0
                },
                "availableStock": None,
                "sourceDocumentDetail": None,
                "colorId": None,
                "balance": 100,
                "withholdingTax": 3.5,
                "ivaPUCId": 85800,
                "detailDate": "Wed, 29 Mar 2017 09:51:35 GMT",
                "crossDocumentHeaderId": None,
                "withholdingICA": False,
                "code": "AC001",
                "costCenterId": 4,
                "withholdingTaxPUCId": 85677,
                "itemToCompare": {
                  "addConsumptionToPurchase": True,
                  "priceListA7": 0,
                  "lastCost": 0,
                  "priceList5": 0,
                  "name": "ACEITE DE AGUACATE X 125 GR",
                  "priceListA2": 0,
                  "typeItem": "A",
                  "disccountToUnitValue": False,
                  "priceListA6": 0,
                  "subInventoryGroup2Id": None,
                  "priceListB6": 0,
                  "subInventoryGroup3Id": None,
                  "packagePrice": 0,
                  "priceList8": 0,
                  "creationDate": "Tue, 10 Dec 2013 14:40:27 GMT",
                  "consumptionPUC": {
                    "pucAccount": "246205010 IMPUESTO AL CONSUMO 8%",
                    "pucId": 85858,
                    "percentage": 8
                  },
                  "priceListB3": 0,
                  "measurementUnit3Id": 44,
                  "plu": "123123 1",
                  "measurementUnit3": {
                    "name": "ONZA                          ",
                    "code": "ONZ",
                    "measurementUnitId": 44
                  },
                  "subInventoryGroup3": None,
                  "inventoryGroupId": 9,
                  "priceList6": 0,
                  "percentageICA": 11.04,
                  "priceListA9": 0,
                  "photo": None,
                  "priceListB2": 0,
                  "inventoryGroup": {
                    "name": "COSMETICOS",
                    "inventoryGroupId": 9
                  },
                  "priceList3": 0,
                  "reference": "321321",
                  "priceListA1": 50,
                  "incomingPUC": {
                    "pucAccount": "413550005 VENTA DE QUIMICOS",
                    "pucId": 86636,
                    "percentage": 0
                  },
                  "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                  "consumptionPercentage": 8,
                  "percentageSaleIVA": 16,
                  "inventoryPUC": {
                    "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                    "pucId": 84706,
                    "percentage": 0
                  },
                  "measurementUnitId": 49,
                  "inventoryPUCId": 84706,
                  "isDeleted": False,
                  "ivaSalePUCId": 85778,
                  "priceListB5": 0,
                  "withholdingTaxPurchasePUCId": 85677,
                  "consumptionPUCId": 85858,
                  "priceList4": 0,
                  "size": False,
                  "conversionFactor": 10,
                  "measurementUnit": {
                    "name": "CUARTO DE LIBRA               ",
                    "code": "CTO",
                    "measurementUnitId": 49
                  },
                  "costPUC": {
                    "pucAccount": "613550005 VENTA DE QUIMICOS",
                    "pucId": 88508,
                    "percentage": 0
                  },
                  "incomingPUCId": 86636,
                  "addConsumptionToCost": False,
                  "orderQuantity": 0,
                  "saleIVA": {
                    "name": "GRAVADO",
                    "ivaId": 2,
                    "code": "G"
                  },
                  "purchaseIVA": {
                    "name": "GRAVADO",
                    "ivaId": 2,
                    "code": "G"
                  },
                  "purchaseIVAId": 2,
                  "measurementUnit2": {
                    "name": "UNIDADES                      ",
                    "code": "UNI",
                    "measurementUnitId": 36
                  },
                  "addIVAtoCost": False,
                  "withholdingTaxPurchasePUC": {
                    "pucAccount": "236540005 COMPRAS 3.5%",
                    "pucId": 85677,
                    "percentage": 3.5
                  },
                  "barCode": "123456",
                  "percentagePurchaseIVA": 16,
                  "itemId": 24,
                  "priceList9": 0,
                  "withholdingSalePercentage": 0,
                  "state": "A",
                  "ivaSalePUC": {
                    "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                    "pucId": 85778,
                    "percentage": 16
                  },
                  "conversionFactor2": 506,
                  "withholdingTaxSalePUCId": 84520,
                  "priceList10": 0,
                  "withholdingPurchasePercentage": 3.5,
                  "priceListB4": 0,
                  "priceListB1": 501,
                  "discountPercentage": 0,
                  "priceListA4": 0,
                  "withholdingICA": False,
                  "priceListB10": 0,
                  "code": "AC001",
                  "priceListA8": 0,
                  "invimaRegister": None,
                  "namePOS": "ACEITE DE AGUACATE X 125 GR",
                  "companyId": 1,
                  "averageCost": 5506.271765,
                  "costPUCId": 88508,
                  "minimumStock": 0,
                  "lot": False,
                  "saleIVAId": 2,
                  "priceListB8": 0,
                  "serial": False,
                  "subInventoryGroup2": None,
                  "invimaDueDate": None,
                  "brandId": 8,
                  "priceList1": 120,
                  "measurementUnit2Id": 36,
                  "priceListA10": 0,
                  "ivaPurchasePUCId": 85796,
                  "priceListB9": 0,
                  "updateDate": "Mon, 10 Oct 2016 15:00:59 GMT",
                  "withholdingTaxSalePUC": {
                    "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                    "pucId": 84520,
                    "percentage": 0
                  },
                  "subInventoryGroups1": None,
                  "priceList2": 0,
                  "providerId": None,
                  "color": False,
                  "weight": 0,
                  "createdBy": "Migracion",
                  "lastPurchaseDate": "Sat, 29 Dec 1900 05:00:00 GMT",
                  "companyCost": 5636.6,
                  "imageId": None,
                  "priceList7": 0,
                  "ivaPurchasePUC": {
                    "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                    "pucId": 85796,
                    "percentage": 16
                  },
                  "priceListA3": 0,
                  "description": "",
                  "priceListB7": 0,
                  "subInventoryGroup1Id": None,
                  "priceListA5": 0
                },
                "kitLaborId": None,
                "documentHeaderId": None,
                "creationDate": "Wed, 29 Mar 2017 10:49:49 GMT",
                "indexItem": 0,
                "baseValue": 523426.2000000001,
                "asset": None,
                "sourceDocumentNumber": None,
                "quantity": 100,
                "businessAgentId": None,
                "detailDocument": None,
                "search": None,
                "otherThirdId": None,
                "physicalLocation": None,
                "ivaPurchasePUC": {
                  "name": "IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% SERVICIOS",
                  "dueDate": False,
                  "pucId": 85800,
                  "pucAccount": "240820026",
                  "quantity": False,
                  "percentage": 16
                },
                "checkNumber": None,
                "payrollEntityId": None,
                "updateDate": "Wed, 29 Mar 2017 10:49:49 GMT",
                "importConceptId": None,
                "und": {
                  "name": "CUARTO DE LIBRA               ",
                  "code": "CTO",
                  "measurementUnitId": 49
                },
                "cashRegisterId": None,
                "providerId": 532,
                "pieceId": None,
                "icaPercent": None,
                "sectionId": 7,
                "consumptionTaxValue": 41874.1,
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "overCost": 10000,
                "sourceDocumentPrefix": None,
                "withholdingTaxPUC": {
                  "name": "COMPRAS 3.5%",
                  "dueDate": False,
                  "pucId": 85677,
                  "pucAccount": "236540005",
                  "quantity": False,
                  "percentage": 3.5
                },
                "sourceDocumentDetailId": None,
                "globalTax": None,
                "surcharge": None,
                "detailWarehouse": {
                  "name": "LEGAQUIMICOS MODIFICAD",
                  "codeComplete": "Código 002",
                  "warehouseId": 6,
                  "typeWarehouse": "S",
                  "code": "002"
                },
                "bankCode": None,
                "comments": None,
                "amount": None
              }
            ],
            "destinyBranchId": None,
            "reteICAPUCId": None,
            "leadDocumentTo": None,
            "closingType": 0,
            "payment": 627747.6,
            "bankAccountId": None,
            "payrollType": None,
            "isDeleted": 0,
            "baseSalary": None,
            "destinyWarehouseId": None,
            "deductibleRF": None,
            "consumptionTaxPUCId": None,
            "importId": None,
            "reteIVABase": 83748.19,
            "documentAffecting": [],
            "bankAccount": None,
            "typeAccount": 1,
            "partnerId": None,
            "sodicon": None,
            "dependencyId": None,
            "importReplaced": 0,
            "auxNumberTwo": None,
            "directIVA": None,
            "sourceDocumentOrigin": "FP",
            "applyCree": None,
            "disccount2Value": 16188.44,
            "insurancePUCId": None,
            "accounted": 0,
            "isConsignment": 0,
            "comission": None,
            "documentTypeId": 49,
            "state": 1,
            "sourceWarehouseId": None,
            "requisitionNumber": None,
            "importationValue": None,
            "comissionPercent": None,
            "cashierId": None,
            "shipZipCode": None,
            "daysVacation": None,
            "customer": None,
            "withholdingTaxBase": None,
            "controlPrefix": "UTST",
            "fspValue": None,
            "reteIVAPercent": 3,
            "currencyId": 4,
            "freightPUCId": None,
            "ivaValue": 83748.19,
            "sourceDocumentHeader": None,
            "disccount2Mode": 0,
            "kitId": None,
            "auxNumberOne": None,
            "creationDate": "Wed, 29 Mar 2017 10:49:49 GMT",
            "overTax": None,
            "businessAgentId": None,
            "shipCity": None,
            "disccount2": 3,
            "expenses": None,
            "withholdingCREEPUCId": None,
            "annuled": False,
            "disccount2TaxBase": True,
            "payrollEntityId": None,
            "typeThirdParty": None,
            "retentionPUCId": 85829,
            "currency": {
              "code": "COP",
              "isDeleted": 0,
              "createdBy": "Migracion",
              "updateBy": "ADMINISTRADOR UPDATE del Sistema",
              "name": "PESO COLOMBIANO",
              "symbol": "$",
              "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
              "updateDate": "Tue, 11 Oct 2016 11:52:54 GMT",
              "currencyId": 4
            },
            "reteIVAValue": 2512.45,
            "otherThird": None,
            "branchId": 14,
            "isChangeNoted": 0,
            "layoffValue": 0,
            "freight": None,
            "providerId": 532,
            "year": None,
            "sectionId": 7,
            "consumptionTaxValue": 41874.1,
            "prefixRequisitionNumber": None,
            "adjustment": None,
            "documentNumber": "0000003082",
            "globalTax": None,
            "valueCREE": 0,
            "overCostTaxBase": False,
            "withholdingTaxPercent": None,
            "semester": None,
            "comments": "ninguna observacion",
            "sourceId": 49,
            "shortWord": "FP",
            "paymentTermId": 2
          }
        # Envio la creacion del avance sin short word
        invoice_sale_item["shortWord"] = None
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        invoice_sale_item["shortWord"] = "XY"
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        invoice_sale_item["shortWord"] = "FP"
        # Crea un compra de item con un peso de diferencia en el credit
        invoice_sale_item['documentDetails'][0]['value'] = 550627
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        invoice_sale_item['documentDetails'][0]['value'] = 550627
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        invoice_sale_item['documentDetails'][0]['value'] = 550627.18
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = invoice_sale_item['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                      "currencyId": 2,
                      "isDeleted": 0,
                      "name": "DÓLAR AMERICANO",
                      "symbol": "$"}

        invoice_sale_item["currency"] = currency2
        invoice_sale_item["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(invoice_sale_item)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        invoice_sale_item["currency"] = currency
        invoice_sale_item["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=FP&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("dateFrom", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("disccount2Value", response.json)
        self.assertIn("comments", response.json)

        invoice_sale_item2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(invoice_sale_item2)
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