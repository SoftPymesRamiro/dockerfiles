#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 29-03-2017
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
handled provider_note
"""
class ProviderNoteTest(unittest.TestCase):
    """
    This Class is a  Test Case for provider_note API class
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
        """Sent get request to #/api/v1/provider_note# with provider_note data values

        :param data: provider_note data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/provider_notes' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/provider_note# with provider_note data values

        :param data: provider_note data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/provider_notes' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/provider_note# with provider_note data values

        :param data: provider_note data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/provider_notes' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/provider_note# with provider_note data values

        :param data: provider_note data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/provider_notes' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_provider_notes(self):
        """
        This function test get a provider Notes according to identifier
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

    def test_get_provider_note_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=LT")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.test_client.get('/api/v1/document_headers/search?branchId=14&startDate=2017-03-01&limitDate='
                                        '2017-03-31&documentNumber=null&controlNumber=null&'
                                        'search=null&filterBy=null&initTotal=null&endTotal=null&shortWord=DP',
                             data=json.dumps(''),
                             content_type='application/json', headers=self.headers)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        provider_note = response.json['data'][0]

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' +
                                    provider_note['documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=DP&document_number=' +
                                    provider_note['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("total", response.json)
        self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(provider_note['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)
        self.assertIn("total", response.json)

        # response = self.test_client.get('api/v1/document_headers/'
        #                                 +str(provider_note['documentHeaderId'])+
        #                                 '/accounting_records/preview',
        #                      data = json.dumps(''),
        #                      content_type = 'application/json', headers=self.headers)
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
            "prefix": "UTST",
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
            "documentNumber": "0000009999",
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

        response = self.test_client.post('/api/v1/purchase_item/',
                                     data=json.dumps(purchase_item),
                                     content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.purchase_item_document_number0 = response.json['documentNumber']
        self.purchase_item_id0 = response.json['id']

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FP&document_number='+
                                    str(self.purchase_item_document_number0))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        purchase_item = response.json

        provider_note_dp = {
          "retentionBase": 1,
          "withholdingTaxBase": 1,
          "withholdingTaxValue": 1,
          "subtotal": 1,
          "total": 540000,
          "shortWord": "DP",
          "sourceShortWord":"DP",
          "documentDetails": [
            {
              "baseValue": 480000,
              "unitValue": 160000,
              "units": 3,
              "value": 480000,
              "accountNumber": None,
              "amount": None,
              "assetId": None,
              "authorizationNumber": None,
              "availableStock": None,
              "balance": 3,
              "bankAccountId": None,
              "bankCode": None,
              "bankName": None,
              "businessAgentId": None,
              "cashRegisterId": None,
              "checkNumber": None,
              "colorId": 2,
              "comments": None,
              "consumptionTaxBase": 1,
              "consumptionTaxPUCId": None,
              "consumptionTaxPercent": 0,
              "consumptionTaxValue": 0,
              "conversionFactor": 1,
              "cost": None,
              "costCenterId": 5,
              "createdBy": "ADMINISTRADOR UPDATE del Sistema",
              "creationDate": "Wed, 28 Dec 2016 11:45:59 GMT",
              "crossDocumentHeaderId": None,
              "customerId": None,
              "dependencyId": None,
              "detailDate": "Wed, 28 Dec 2016 11:28:44 GMT",
              "detailDocument": None,
              "detailDocumentTypeId": 49,
              "detailPrefix": None,
              "detailWarehouseId": 6,
              "disccount": 0,
              "divisionId": 16,
              "documentDetailId": 305379,
              "documentHeaderId": 117556,
              "dueDate": None,
              "employeeId": None,
              "finalDate": None,
              "financialEntityId": None,
              "globalTax": None,
              "icaPercent": None,
              "importConceptId": None,
              "initialDate": None,
              "interest": None,
              "isDeleted": 0,
              "item": {
                "addConsumptionToCost": False,
                "addConsumptionToPurchase": False,
                "addIVAtoCost": False,
                "averageCost": 0,
                "barCode": None,
                "brandId": None,
                "code": "PY003",
                "color": True,
                "companyCost": 100,
                "companyId": 1,
                "consumptionPUC": None,
                "consumptionPUCId": None,
                "consumptionPercentage": 0,
                "conversionFactor": 0,
                "conversionFactor2": 0,
                "costPUC": {
                  "percentage": 0,
                  "pucAccount": "613550005 VENTA DE QUIMICOS",
                  "pucId": 88508
                },
                "costPUCId": 88508,
                "createdBy": "ADRIAN",
                "creationDate": "Tue, 02 Aug 2016 15:14:41 GMT",
                "description": None,
                "disccountToUnitValue": False,
                "discountPercentage": 0,
                "imageId": None,
                "incomingPUC": {
                  "percentage": 0,
                  "pucAccount": "413550005 VENTA DE QUIMICOS",
                  "pucId": 2520
                },
                "incomingPUCId": 2520,
                "inventoryGroup": None,
                "inventoryGroupId": None,
                "inventoryPUC": {
                  "percentage": 0,
                  "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                  "pucId": 84706
                },
                "inventoryPUCId": 84706,
                "invimaDueDate": "Tue, 02 Aug 2016 14:56:49 GMT",
                "invimaRegister": None,
                "isDeleted": False,
                "itemId": 1751,
                "ivaPurchasePUC": {
                  "percentage": 10,
                  "pucAccount": "240820015 IMPUESTO A LAS VENTAS - PAGADO POR COMPRAS AL 10%",
                  "pucId": 85797
                },
                "ivaPurchasePUCId": 85797,
                "ivaSalePUC": {
                  "percentage": 10,
                  "pucAccount": "240810015 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 10%",
                  "pucId": 85783
                },
                "ivaSalePUCId": 85783,
                "lastCost": 0,
                "lastPurchaseDate": "Tue, 02 Aug 2016 14:56:49 GMT",
                "lot": False,
                "measurementUnit": {
                  "code": "ASD",
                  "measurementUnitId": 1,
                  "name": "PRODUCT2O 121"
                },
                "measurementUnit2": None,
                "measurementUnit2Id": None,
                "measurementUnit3": None,
                "measurementUnit3Id": None,
                "measurementUnitId": 1,
                "minimumStock": 0,
                "name": "PY003",
                "namePOS": "PY003",
                "orderQuantity": 0,
                "packagePrice": 0,
                "percentageICA": 10,
                "percentagePurchaseIVA": 10,
                "percentageSaleIVA": 10,
                "photo": None,
                "plu": None,
                "priceList1": 100,
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
                "priceListB1": 0,
                "priceListB10": 0,
                "priceListB2": 0,
                "priceListB3": 0,
                "priceListB4": 0,
                "priceListB5": 0,
                "priceListB6": 0,
                "priceListB7": 0,
                "priceListB8": 0,
                "priceListB9": 0,
                "providerId": None,
                "purchaseIVA": {
                  "code": "G",
                  "ivaId": 2,
                  "name": "GRAVADO"
                },
                "purchaseIVAId": 2,
                "reference": None,
                "saleIVA": {
                  "code": "G",
                  "ivaId": 2,
                  "name": "GRAVADO"
                },
                "saleIVAId": 2,
                "serial": False,
                "size": True,
                "state": "A",
                "subInventoryGroup1Id": None,
                "subInventoryGroup2": None,
                "subInventoryGroup2Id": None,
                "subInventoryGroup3": None,
                "subInventoryGroup3Id": None,
                "subInventoryGroups1": None,
                "typeItem": "A",
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "updateDate": "Tue, 27 Dec 2016 12:05:46 GMT",
                "weight": 0,
                "withholdingICA": True,
                "withholdingPurchasePercentage": 3.5,
                "withholdingSalePercentage": 2.5,
                "withholdingTaxPurchasePUC": {
                  "percentage": 3.5,
                  "pucAccount": "236540005 COMPRAS 3.5%",
                  "pucId": 85677
                },
                "withholdingTaxPurchasePUCId": 85677,
                "withholdingTaxSalePUC": {
                  "percentage": 2.5,
                  "pucAccount": "135515003 RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                  "pucId": 84519
                },
                "withholdingTaxSalePUCId": 84519
              },
              "itemId": 1751,
              "iva": 16,
              "ivaCustomer": None,
              "ivaPUCId": 85796,
              "kitAssetId": None,
              "kitItemId": None,
              "kitLaborId": None,
              "listSerials": [],
              "lot": None,
              "mainUnitValue": None,
              "measurementUnitId": 1,
              "otherThirdId": None,
              "overCost": None,
              "partnerId": None,
              "payrollConceptId": None,
              "payrollEntityId": None,
              "percentCost": None,
              "physicalLocation": None,
              "pieceId": None,
              "providerId": 26,
              "pucId": None,
              "quantity": 3,
              "quantityRefund": None,
              "quoteNumber": None,
              "reteICA": None,
              "reteICAPercent": None,
              "search": None,
              "sectionId": None,
              "selected": None,
              "sizeId": 2,
              "sourceDocumentDetailId": None,
              "sourceDocumentNumber": None,
              "sourceDocumentPrefix": None,
              "sourceDocumentTypeId": None,
              "surcharge": None,
              "thirdId": None,
              "updateBy": "ADMINISTRADOR UPDATE del Sistema",
              "updateDate": "Fri, 13 Jan 2017 11:36:17 GMT",
              "withholdingTax":3.5,
              "withholdingTaxPUCId": 85677,
              "withholdingValue": None
            }
          ],
          "sourceDocumentOrigin": "FP",
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
          "paymentReceipt": {
            "paymentNumber":"0000000000",
            "paymentDetails": [{
                "balance": 15568990.11,
                "isDeleted": 0,
                "paymentType": "EF",
                "state": 1,
                "value": 300000
              },{
                "balance": 15568990.11,
                "isDeleted": 0,
                "paymentType": "EF",
                "quoteNumber": 0,
                "state": 1,
                "value": 200000
              }]
          },
          "ivaBase": 0,
          "accounted": 0,
          "accountsBackward": 0,
          "addToPayroll": None,
          "adjustment": None,
          "advanceLayoff": 0,
          "afpValue": None,
          "annuled": 0,
          "asset": None,
          "assetId": None,
          "assumedIVA": 0,
          "auxCharacterOne": None,
          "auxCharacterTwo": None,
          "auxNumberOne": None,
          "auxNumberTwo": None,
          "auxTimeOne": None,
          "auxTimeTwo": None,
          "balance": 0,
          "bankAccount": None,
          "bankAccountId": None,
          "baseCREE": 0,
          "baseSalary": 0,
          "baseType": None,
          "billingResolution": None,
          "billingResolutionId": None,
          "bonus": 0,
          "bonusDateFrom": None,
          "branch": {
            "address1": "CR 13 A 12 47",
            "address2": None,
            "branchId": 14,
            "cityId": 418,
            "code": "001",
            "company": {
              "code": "001",
              "companyId": 1,
              "identificationDV": "3",
              "identificationNumber": "830081994",
              "name": "LEGAQUIMICOS SAS modificada"
            },
            "companyId": 1,
            "createdBy": "Administrador del Sistema",
            "creationDate": "Fri, 09 Aug 2013 11:25:30 GMT",
            "economicActivityId": 253,
            "email": "legaquimicos@hotmail.com",
            "fax": "2846030",
            "icaActivity1": "4664",
            "icaActivity2": None,
            "icaActivity3": None,
            "icaActivity4": None,
            "icaActivity5": None,
            "icaRate1": 11.04,
            "icaRate2": 0,
            "icaRate3": 0,
            "icaRate4": 0,
            "icaRate5": 0,
            "isDeleted": 0,
            "motionDate": "Mon, 05 Oct 2015 15:04:06 GMT",
            "name": "PRINCIPAL",
            "phone1": "2860084",
            "phone2": "2860084",
            "phone3": None,
            "updateBy": "YeffSolarte",
            "updateDate": "Mon, 05 Oct 2015 15:04:06 GMT",
            "withholdingCREEPUCId": 84558,
            "zipCode": ""
          },
          "branchId": 14,
          "businessAgent": None,
          "businessAgentId": None,
          "cash": 0,
          "cashRegister": None,
          "cashRegisterId": None,
          "cashier": None,
          "cashierId": None,
          "checks": None,
          "closingType": 0,
          "comission": None,
          "comissionPercent": None,
          "comments": "",
          "consumptionTaxBase": None,
          "consumptionTaxPUC": None,
          "consumptionTaxPUCId": None,
          "consumptionTaxPercent": None,
          "consumptionTaxValue": 0,
          "contract": None,
          "contractId": None,
          "controlNumber": "000000000",
          "controlPrefix": "01",
          "costCenter": {
            "branchId": 14,
            "code": "00001",
            "costCenterId": 4,
            "createdBy": "DENNY ORJUELA",
            "creationDate": "Wed, 14 Aug 2013 10:41:52 GMT",
            "divisions": [
              {
                "code": "00001",
                "costCenterId": 4,
                "createdBy": "DENNY ORJUELA",
                "creationDate": "Wed, 14 Aug 2013 10:42:14 GMT",
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
                    "createdBy": "ADMINISTRADOR",
                    "creationDate": "Fri, 18 Sep 2015 14:44:05 GMT",
                    "dependencies": [],
                    "divisionId": 13,
                    "isDeleted": 0,
                    "name": "F",
                    "puc": None,
                    "pucId": None,
                    "sectionId": 7,
                    "updateBy": "ADMINISTRADOR",
                    "updateDate": "Fri, 18 Sep 2015 14:44:05 GMT"
                  }
                ],
                "updateBy": "Administrador del Sistema",
                "updateDate": "Fri, 23 Aug 2013 11:39:20 GMT"
              },
              {
                "code": "00002",
                "costCenterId": 4,
                "createdBy": "Administrador del Sistema",
                "creationDate": "Fri, 23 Aug 2013 11:39:40 GMT",
                "divisionId": 14,
                "isDeleted": 0,
                "name": "VENTAS",
                "puc": {
                  "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                  "percentage": 0,
                  "pucId": 89100
                },
                "pucId": 89100,
                "sections": [],
                "updateBy": "ADMINISTRADOR",
                "updateDate": "Tue, 08 Sep 2015 17:34:33 GMT"
              }
            ],
            "isDeleted": 0,
            "name": "LEGAQUIMICOS",
            "updateBy": "Administrador del Sistema",
            "updateDate": "Fri, 23 Aug 2013 11:37:13 GMT"
          },
          "costCenterId": 4,
          "currency": {
            "code": "COP",
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
            "currencyId": 4,
            "isDeleted": 0,
            "name": "PESO COLOMBIANO",
            "symbol": "$",
            "updateBy": "ADMINISTRADOR UPDATE del Sistema",
            "updateDate": "Tue, 11 Oct 2016 11:52:54 GMT"
          },
          "currencyId": 4,
          "customer": None,
          "customerId": None,
          "cutNumber": 0,
          "dateFrom": None,
          "dateTo": None,
          "daysEnjoy": None,
          "daysLicensed": None,
          "daysNet": None,
          "daysPILA": None,
          "daysVacation": None,
          "daysWorked": None,
          "deductibleRF": 0,
          "dependency": None,
          "dependencyId": None,
          "depositNumber": None,
          "destinyBranch": None,
          "destinyBranchId": None,
          "destinyWarehouse": None,
          "destinyWarehouseId": None,
          "directIVA": 0,
          "directIVAPercent": 0,
          "disccount": 0,
          "disccount2": 0,
          "disccount2Mode": 0,
          "disccount2TaxBase": 0,
          "disccount2Value": 0,
          "disccountPercent": 0,
          "division": {
            "code": "00002",
            "costCenterId": 4,
            "createdBy": "Administrador del Sistema",
            "creationDate": "Fri, 23 Aug 2013 11:39:40 GMT",
            "divisionId": 14,
            "isDeleted": 0,
            "name": "VENTAS",
            "puc": {
              "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
              "percentage": 0,
              "pucId": 89100
            },
            "pucId": 89100,
            "sections": [],
            "updateBy": "ADMINISTRADOR",
            "updateDate": "Tue, 08 Sep 2015 17:34:33 GMT"
          },
          "divisionId": 14,
          "documentDate": "Tue, 07 Jan 2014 00:00:00 GMT",
          "documentNumber": "0000000000",
          "documentType": {
            "comments": None,
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "documentTypeId": 49,
            "isDeleted": 0,
            "isIncomePayment": None,
            "name": "FACTURA DE PROVEEDOR",
            "needResolution": 0,
            "shortWord": "FP",
            "updateBy": "011",
            "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider"
          },
          "documentTypeConsign": None,
          "documentTypeId": 35,
          "employee": None,
          "employeeId": None,
          "epsValue": None,
          "exchangeRate": 1,
          "expenses": 0,
          "finalDate": None,
          "financialEntity": None,
          "financialEntityId": None,
          "firtsContractDate": None,
          "freezeBill": 0,
          "freight": None,
          "freightPUC": None,
          "freightPUCId": None,
          "fspValue": None,
          "globalTax": 0,
          "import": None,
          "importId": None,
          "importReplaced": 0,
          "importationValue": None,
          "inability": 0,
          "initialDate": None,
          "initialQuota": 0,
          "insurance": None,
          "insurancePUC": None,
          "insurancePUCId": None,
          "interest": 0,
          "interestPUC": None,
          "interestPUCId": None,
          "isChangeNoted": 0,
          "isConsignment": 0,
          "isDeleted": 0,
          "ivaPUC": None,
          "ivaPUCId": None,
          "ivaPercent": None,
          "ivaValue": 76800,
          "kit": None,
          "kitId": None,
          "layoffValue": 0,
          "leadDocumentTo": None,
          "month": None,
          "orderNumber": "",
          "otherThird": None,
          "otherThirdId": None,
          "overCost": 0,
          "overCostTaxBase": 0,
          "overTax": 0,
          "partner": None,
          "partnerId": None,
          "payment": 0,
          "paymentBy": 0,
          "payrollBasic": None,
          "payrollBasicId": None,
          "payrollEntity": None,
          "payrollEntityId": None,
          "payrollPaymentType": None,
          "payrollType": None,
          "percentageCREE": 0,
          "periodicityQuota": "",
          "pettyCash": 0,
          "prefix": "",
          "prefixRequisitionNumber": "",
          "printed": 0,
          "productionOrder": None,
          "productionOrderId": None,
          "productionUnits": None,
          "providerId": 26,
          "puc": {
            "aCurrent": True,
            "account": "35",
            "accountPayableLayoff": False,
            "accountsPayableForeignProvider": False,
            "accountsPayableForeignProviders": False,
            "accountsPayableHolidays": False,
            "accountsPayableNationalProvider": False,
            "accountsPayableReport": True,
            "accountsReceivableCashReceipt": True,
            "accountsReceivableReport": False,
            "accruedInterestPayableOnLayoffs": False,
            "alternateDoc": False,
            "article": False,
            "asset": False,
            "assetUtility": False,
            "assetValuation": False,
            "assetsConsigning": False,
            "assetsConsigningCustomer": False,
            "auxiliary1": "005",
            "auxiliary2": "000",
            "auxiliaryName": None,
            "bankAccounts": False,
            "baseValue": False,
            "billingConceptsContractsCostsExpensesPayable": True,
            "billingConceptsFixedAssetsDeferred": False,
            "billingConceptsFixedAssetsIntangibles": False,
            "billingConceptsFixedAssetsOther": False,
            "billingConceptsFixedAssetsPropertyPlantEquipment": False,
            "billingConceptsInventories": False,
            "billingConceptsInventoryConsignment": False,
            "billingConceptsInventoryConsignmentCustomer": False,
            "billingConceptsInvestment": False,
            "billingConceptsSellingCosts": False,
            "cash": False,
            "cashBoxExcess": False,
            "ccfContributions": False,
            "ccfContributionsExpense": False,
            "changeNote": False,
            "checks": False,
            "className": "CUENTAS POR PAGAR COMERCIALES Y OTRAS CUENTAS POR PAGAR",
            "companyId": 1,
            "compensation": False,
            "compensationExpenses": False,
            "conceptAssetContract": False,
            "conceptInventoryContract": False,
            "conceptsAbroadProviderPayment": False,
            "conceptsBankCreditNotes": False,
            "conceptsBankDebitNotes": False,
            "conceptsCostsAndExpensesPayable": True,
            "conceptsForPayingTaxes": False,
            "conceptsIndirectCostsManufacturing": False,
            "conceptsNationalProviderPayment": True,
            "conceptsPayableShareHoldersPartners": False,
            "conceptsPaymentsOtherThirdParties": False,
            "conceptsProductionOrders": False,
            "constructionContracts": False,
            "consumptionTax": False,
            "contributionsExpenseDifferenceInSOI": False,
            "contributionsHealth": False,
            "contributionsToHealthExpenses": False,
            "costCenter": False,
            "createdBy": "Administrador del Sistema",
            "creationDate": "Fri, 09 Aug 2013 11:25:32 GMT",
            "creditBalanceICAPayments": False,
            "creditBalanceIVAPayments": False,
            "creditCardAccounts": False,
            "creditCardsVoucher": False,
            "creditorsOrderAccounts": False,
            "creeRetainingSale": False,
            "creeRetainingService": False,
            "customer": False,
            "customerAccountsReceivable": False,
            "customerAdvances": False,
            "customerFinancement": False,
            "debitOrderAccounts": False,
            "deferredCharges": False,
            "deferredIncome": False,
            "deferredInterest": False,
            "depositCommissionVoucher": False,
            "deprecation": {
              "deprecationPUC": None,
              "expensePUC": None
            },
            "depreciationConcepts": False,
            "depreciationFixedAssetsAccount": False,
            "deprecitionForInflation": False,
            "deterioration": {
              "deteriorationPUC": None
            },
            "dianBetsAndSimilar": False,
            "dianCommissions": False,
            "dianDisposalOfAssetsNatPersons": False,
            "dianDividendsAndShares": False,
            "dianFinancialPerformance": False,
            "dianHonorary": False,
            "dianIVAChargeOfCommon": False,
            "dianIVAPurchasesOrServicesSimplifiedSystem": False,
            "dianNationalRate": False,
            "dianPaymentsInForeignRent": False,
            "dianPurchases": False,
            "dianRents": False,
            "dianServices": False,
            "disabilities": False,
            "discountPurchases": False,
            "discountSales": False,
            "distressedInventory": False,
            "dueDate": True,
            "employee": False,
            "exemptRetefuente": False,
            "expenseContributionsToPensionFund": False,
            "expenseContributionstoProfessionalRiskInsurance": False,
            "expenseContributionstotheNationalLearningService": False,
            "expenseDifferenceChange": False,
            "expenseIncome": False,
            "expensesInternalConsumption": False,
            "extralegalBenefits": False,
            "feedLegalizationEmployees": False,
            "foreignCurrencyAccountsreceivable": False,
            "foreignExchangeAccountsReceivable": False,
            "foreignExchangeFinancialEntity": False,
            "forwardConceptsEmployeesLegalization": True,
            "freightPurchases": False,
            "freightSales": False,
            "gainsAndLosses": False,
            "generalInvestment": False,
            "giftVoucher": False,
            "holdingExpenseProvision": False,
            "icaRetainingSale": False,
            "icaRetainingService": False,
            "icbfContributions": False,
            "icbfContributionsExpense": False,
            "implicitInterest": False,
            "implicitInterestIncome": False,
            "implicitInterestPurchase": False,
            "imports": False,
            "importsIVA": False,
            "incentive": False,
            "incentiveExpenses": False,
            "incomeAdjustingWeight": False,
            "incomeDifferenceChange": False,
            "incurredTax": False,
            "industryAndCommerceTaxICA": False,
            "industryCommerceTax": False,
            "inflationConcepts": False,
            "insurance": False,
            "integralSalary": False,
            "interestLayoffs": False,
            "interestReceived": False,
            "interestonLayoffProvision": False,
            "interestonLayoffProvisionExpense": False,
            "inventoryImpairment": False,
            "inventoryIncomeAdjustment": False,
            "inventoryPieces": False,
            "investmentIncome": False,
            "investmentLoss": False,
            "isDeleted": False,
            "ivaCode": None,
            "ivaPurchase": False,
            "ivaPurchaseProperty": False,
            "ivaPurchaseService": False,
            "ivaPurchaseTradeZone": False,
            "ivaSale": False,
            "ivaSaleAIU": False,
            "ivaSaleBeer": False,
            "ivaSaleCI": False,
            "ivaSaleGambling": False,
            "ivaSalePropertyForeign": False,
            "ivaSaleServiceForeign": False,
            "ivaSaleTradeZone": False,
            "laborObligations": False,
            "layoffs": False,
            "legalCurrencyAccountsReceivable": False,
            "legalizationConceptsExpensesPayable": True,
            "legalizationConceptsLowerBox": True,
            "legalizationConceptsRevolvingFund": True,
            "legalizationExpensesPayable": False,
            "legalizationLowerBox": False,
            "lessCashPayoutTo": False,
            "loansEmployeesConcepts": False,
            "loansFromFinancialEntity": False,
            "loansFromOtherThirdParties": False,
            "loansFromPartnersShareholders": False,
            "loansMembersConcepts": False,
            "loansPrivateConcepts": False,
            "lossFixedAssets": False,
            "lossYear": False,
            "mainDocument": True,
            "monthlySalary": False,
            "movingBranchDestination": False,
            "movingHomeBranch": False,
            "name": "SERVICIOS DE MANTENIMIENTO",
            "nationalApprenticeshipServiceContributions": False,
            "nature": "C",
            "needCashRegister": False,
            "netIncome": False,
            "nonCurrent": False,
            "nonOperationalIncome": False,
            "occupationalInsuranceContributions": False,
            "operationalIncome": False,
            "otherAccountsPay": False,
            "otherAssetRetirementExpenses": False,
            "otherBonus": False,
            "otherDiscounts": False,
            "otherSaleByThirdParties": False,
            "partner": False,
            "patrimony": False,
            "paymentsForThirdParties": False,
            "payrollConcepts": False,
            "payrollEntity": False,
            "penaltyInterestPurchases": False,
            "pensionFundContributions": False,
            "pensionSolidarityFundContributions": False,
            "percentage": 0,
            "premiumsPayable": False,
            "productionExpenseLabor": False,
            "productionSpendingMachineHours": False,
            "provider": True,
            "providerAdvances": False,
            "provisionBonus": False,
            "provisionBonusExpense": False,
            "provisionCancelHolding": False,
            "provisionHolding": False,
            "provisionVacation": False,
            "provisionVacationExpense": False,
            "provisionlayoffs": False,
            "provisionlayoffsExpense": False,
            "pucAccount": "233535005",
            "pucClass": "2",
            "pucId": 85616,
            "pucSubClass": "3",
            "pucs": [
              {
                "name": "INDUSTRIA Y COMERCIO",
                "percentage": 0,
                "pucAccount": "511505005",
                "pucId": 87399
              },
              {
                "name": "DE TIMBRES",
                "percentage": 0,
                "pucAccount": "511510005",
                "pucId": 87401
              },
              {
                "name": "A LA PROPIEDAD RAIZ",
                "percentage": 0,
                "pucAccount": "511515005",
                "pucId": 87403
              },
              {
                "name": "DERECHOS SOBRE INSTRUMENTOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "511520005",
                "pucId": 87405
              },
              {
                "name": "DE VALORIZACION",
                "percentage": 0,
                "pucAccount": "511525005",
                "pucId": 87407
              },
              {
                "name": "DE TURISMO",
                "percentage": 0,
                "pucAccount": "511530005",
                "pucId": 87409
              },
              {
                "name": "TASA POR UTILIZACION DE PUERTOS",
                "percentage": 0,
                "pucAccount": "511535005",
                "pucId": 87411
              },
              {
                "name": "DE VEHICULOS",
                "percentage": 0,
                "pucAccount": "511540005",
                "pucId": 87413
              },
              {
                "name": "DE ESPECTACULOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "511545005",
                "pucId": 87415
              },
              {
                "name": "CUOTAS DE FOMENTO",
                "percentage": 0,
                "pucAccount": "511550005",
                "pucId": 87417
              },
              {
                "name": "IVA DESCONTABLE",
                "percentage": 0,
                "pucAccount": "511570005",
                "pucId": 87419
              },
              {
                "name": "IMPUESTO AL CONSUMO",
                "percentage": 0,
                "pucAccount": "511570010",
                "pucId": 87420
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "511595005",
                "pucId": 87422
              },
              {
                "name": "TERRENOS",
                "percentage": 0,
                "pucAccount": "514505005",
                "pucId": 87550
              },
              {
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucAccount": "514510005",
                "pucId": 87552
              },
              {
                "name": "MAQUINARIA Y EQUIPO",
                "percentage": 0,
                "pucAccount": "514515005",
                "pucId": 87554
              },
              {
                "name": "EQUIPO DE COMPUTACION Y COMUNICACION",
                "percentage": 0,
                "pucAccount": "514525005",
                "pucId": 87556
              },
              {
                "name": "EQUIPO MEDICO-CIENTIFICO",
                "percentage": 0,
                "pucAccount": "514530005",
                "pucId": 87558
              },
              {
                "name": "EQUIPO DE HOTELES Y RESTAURANTES",
                "percentage": 0,
                "pucAccount": "514535005",
                "pucId": 87560
              },
              {
                "name": "FLOTA Y EQUIPO DE TRANSPORTE",
                "percentage": 0,
                "pucAccount": "514540005",
                "pucId": 87562
              },
              {
                "name": "FLOTA Y EQUIPO FLUVIAL Y/O MARITIMO",
                "percentage": 0,
                "pucAccount": "514545005",
                "pucId": 87564
              },
              {
                "name": "FLOTA Y EQUIPO AEREO",
                "percentage": 0,
                "pucAccount": "514550005",
                "pucId": 87566
              },
              {
                "name": "FLOTA Y EQUIPO FERREO",
                "percentage": 0,
                "pucAccount": "514555005",
                "pucId": 87568
              },
              {
                "name": "ACUEDUCTOS, PLANTAS Y REDES",
                "percentage": 0,
                "pucAccount": "514560005",
                "pucId": 87570
              },
              {
                "name": "ARMAMENTO DE VIGILANCIA",
                "percentage": 0,
                "pucAccount": "514565005",
                "pucId": 87572
              },
              {
                "name": "VIAS DE COMUNICACION",
                "percentage": 0,
                "pucAccount": "514570005",
                "pucId": 87574
              },
              {
                "name": "INSTALACIONES ELECTRICAS",
                "percentage": 0,
                "pucAccount": "515005005",
                "pucId": 87579
              },
              {
                "name": "ARREGLOS ORNAMENTALES",
                "percentage": 0,
                "pucAccount": "515010005",
                "pucId": 87581
              },
              {
                "name": "REPARACIONES LOCATIVAS",
                "percentage": 0,
                "pucAccount": "515015005",
                "pucId": 87583
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "515095005",
                "pucId": 87585
              },
              {
                "name": "INDUSTRIA Y COMERCIO",
                "percentage": 0,
                "pucAccount": "521505005",
                "pucId": 87782
              },
              {
                "name": "DE TIMBRES",
                "percentage": 0,
                "pucAccount": "521510005",
                "pucId": 87784
              },
              {
                "name": "A LA PROPIEDAD RAIZ",
                "percentage": 0,
                "pucAccount": "521515005",
                "pucId": 87786
              },
              {
                "name": "DERECHOS SOBRE INSTRUMENTOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "521520005",
                "pucId": 87788
              },
              {
                "name": "DE VALORIZACION",
                "percentage": 0,
                "pucAccount": "521525005",
                "pucId": 87790
              },
              {
                "name": "DE TURISMO",
                "percentage": 0,
                "pucAccount": "521530005",
                "pucId": 87792
              },
              {
                "name": "TASA POR UTILIZACION DE PUERTOS",
                "percentage": 0,
                "pucAccount": "521535005",
                "pucId": 87794
              },
              {
                "name": "DE VEHICULOS",
                "percentage": 0,
                "pucAccount": "521540005",
                "pucId": 87796
              },
              {
                "name": "DE ESPECTACULOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "521545005",
                "pucId": 87798
              },
              {
                "name": "CUOTAS DE FOMENTO",
                "percentage": 0,
                "pucAccount": "521550005",
                "pucId": 87800
              },
              {
                "name": "IVA DESCONTABLE",
                "percentage": 0,
                "pucAccount": "521570005",
                "pucId": 87802
              },
              {
                "name": "IMPUESTO AL CONSUMO",
                "percentage": 0,
                "pucAccount": "521570010",
                "pucId": 87803
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "521595005",
                "pucId": 87805
              },
              {
                "name": "TERRENOS",
                "percentage": 0,
                "pucAccount": "524505005",
                "pucId": 87933
              },
              {
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucAccount": "524510005",
                "pucId": 87935
              },
              {
                "name": "MAQUINARIA Y EQUIPO",
                "percentage": 0,
                "pucAccount": "524515005",
                "pucId": 87937
              },
              {
                "name": "EQUIPO DE COMPUTACION Y COMUNICACION",
                "percentage": 0,
                "pucAccount": "524525005",
                "pucId": 87939
              },
              {
                "name": "EQUIPO MEDICO-CIENTIFICO",
                "percentage": 0,
                "pucAccount": "524530005",
                "pucId": 87941
              },
              {
                "name": "EQUIPO DE HOTELES Y RESTAURANTES",
                "percentage": 0,
                "pucAccount": "524535005",
                "pucId": 87943
              },
              {
                "name": "FLOTA Y EQUIPO DE TRANSPORTE",
                "percentage": 0,
                "pucAccount": "524540005",
                "pucId": 87945
              },
              {
                "name": "FLOTA Y EQUIPO FLUVIAL Y/O MARITIMO",
                "percentage": 0,
                "pucAccount": "524545005",
                "pucId": 87947
              },
              {
                "name": "FLOTA Y EQUIPO AEREO",
                "percentage": 0,
                "pucAccount": "524550005",
                "pucId": 87949
              },
              {
                "name": "FLOTA Y EQUIPO FERREO",
                "percentage": 0,
                "pucAccount": "524555005",
                "pucId": 87951
              },
              {
                "name": "ACUEDUCTOS, PLANTAS Y REDES",
                "percentage": 0,
                "pucAccount": "524560005",
                "pucId": 87953
              },
              {
                "name": "ARMAMENTO DE VIGILANCIA",
                "percentage": 0,
                "pucAccount": "524565005",
                "pucId": 87955
              },
              {
                "name": "VIAS DE COMUNICACION",
                "percentage": 0,
                "pucAccount": "524570005",
                "pucId": 87957
              },
              {
                "name": "INSTALACIONES ELECTRICAS",
                "percentage": 0,
                "pucAccount": "525005005",
                "pucId": 87962
              },
              {
                "name": "ARREGLOS ORNAMENTALES",
                "percentage": 0,
                "pucAccount": "525010005",
                "pucId": 87964
              },
              {
                "name": "REPARACIONES LOCATIVAS",
                "percentage": 0,
                "pucAccount": "525015005",
                "pucId": 87966
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "525095005",
                "pucId": 87968
              },
              {
                "name": "INDUSTRIA Y COMERCIO",
                "percentage": 0,
                "pucAccount": "721505005",
                "pucId": 88812
              },
              {
                "name": "DE TIMBRES",
                "percentage": 0,
                "pucAccount": "721510005",
                "pucId": 88814
              },
              {
                "name": "A LA PROPIEDAD RAIZ",
                "percentage": 0,
                "pucAccount": "721515005",
                "pucId": 88816
              },
              {
                "name": "DERECHOS SOBRE INSTRUMENTOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "721520005",
                "pucId": 88818
              },
              {
                "name": "DE VALORIZACION",
                "percentage": 0,
                "pucAccount": "721525005",
                "pucId": 88820
              },
              {
                "name": "DE TURISMO",
                "percentage": 0,
                "pucAccount": "721530005",
                "pucId": 88822
              },
              {
                "name": "TASA POR UTILIZACION DE PUERTOS",
                "percentage": 0,
                "pucAccount": "721535005",
                "pucId": 88824
              },
              {
                "name": "DE VEHICULOS",
                "percentage": 0,
                "pucAccount": "721540005",
                "pucId": 88826
              },
              {
                "name": "DE ESPECTACULOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "721545005",
                "pucId": 88828
              },
              {
                "name": "CUOTAS DE FOMENTO",
                "percentage": 0,
                "pucAccount": "721550005",
                "pucId": 88830
              },
              {
                "name": "IVA DESCONTABLE",
                "percentage": 0,
                "pucAccount": "721570005",
                "pucId": 88832
              },
              {
                "name": "IMPUESTO AL CONSUMO",
                "percentage": 0,
                "pucAccount": "721570010",
                "pucId": 88833
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "721595005",
                "pucId": 88835
              },
              {
                "name": "TERRENOS",
                "percentage": 0,
                "pucAccount": "724505005",
                "pucId": 88963
              },
              {
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucAccount": "724510005",
                "pucId": 88965
              },
              {
                "name": "MAQUINARIA Y EQUIPO",
                "percentage": 0,
                "pucAccount": "724515005",
                "pucId": 88967
              },
              {
                "name": "EQUIPO DE COMPUTACION Y COMUNICACION",
                "percentage": 0,
                "pucAccount": "724525005",
                "pucId": 88969
              },
              {
                "name": "EQUIPO MEDICO-CIENTIFICO",
                "percentage": 0,
                "pucAccount": "724530005",
                "pucId": 88971
              },
              {
                "name": "EQUIPO DE HOTELES Y RESTAURANTES",
                "percentage": 0,
                "pucAccount": "724535005",
                "pucId": 88973
              },
              {
                "name": "FLOTA Y EQUIPO DE TRANSPORTE",
                "percentage": 0,
                "pucAccount": "724540005",
                "pucId": 88975
              },
              {
                "name": "FLOTA Y EQUIPO FLUVIAL Y/O MARITIMO",
                "percentage": 0,
                "pucAccount": "724545005",
                "pucId": 88977
              },
              {
                "name": "FLOTA Y EQUIPO AEREO",
                "percentage": 0,
                "pucAccount": "724550005",
                "pucId": 88979
              },
              {
                "name": "FLOTA Y EQUIPO FERREO",
                "percentage": 0,
                "pucAccount": "724555005",
                "pucId": 88981
              },
              {
                "name": "ACUEDUCTOS, PLANTAS Y REDES",
                "percentage": 0,
                "pucAccount": "724560005",
                "pucId": 88983
              },
              {
                "name": "ARMAMENTO DE VIGILANCIA",
                "percentage": 0,
                "pucAccount": "724565005",
                "pucId": 88985
              },
              {
                "name": "VIAS DE COMUNICACION",
                "percentage": 0,
                "pucAccount": "724570005",
                "pucId": 88987
              },
              {
                "name": "INSTALACIONES ELECTRICAS",
                "percentage": 0,
                "pucAccount": "725005005",
                "pucId": 88992
              },
              {
                "name": "ARREGLOS ORNAMENTALES",
                "percentage": 0,
                "pucAccount": "725010005",
                "pucId": 88994
              },
              {
                "name": "REPARACIONES LOCATIVAS",
                "percentage": 0,
                "pucAccount": "725015005",
                "pucId": 88996
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "725095005",
                "pucId": 88998
              },
              {
                "name": "INDUSTRIA Y COMERCIO",
                "percentage": 0,
                "pucAccount": "731505005",
                "pucId": 89195
              },
              {
                "name": "DE TIMBRES",
                "percentage": 0,
                "pucAccount": "731510005",
                "pucId": 89197
              },
              {
                "name": "A LA PROPIEDAD RAIZ",
                "percentage": 0,
                "pucAccount": "731515005",
                "pucId": 89199
              },
              {
                "name": "DERECHOS SOBRE INSTRUMENTOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "731520005",
                "pucId": 89201
              },
              {
                "name": "DE VALORIZACION",
                "percentage": 0,
                "pucAccount": "731525005",
                "pucId": 89203
              },
              {
                "name": "DE TURISMO",
                "percentage": 0,
                "pucAccount": "731530005",
                "pucId": 89205
              },
              {
                "name": "TASA POR UTILIZACION DE PUERTOS",
                "percentage": 0,
                "pucAccount": "731535005",
                "pucId": 89207
              },
              {
                "name": "DE VEHICULOS",
                "percentage": 0,
                "pucAccount": "731540005",
                "pucId": 89209
              },
              {
                "name": "DE ESPECTACULOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "731545005",
                "pucId": 89211
              },
              {
                "name": "CUOTAS DE FOMENTO",
                "percentage": 0,
                "pucAccount": "731550005",
                "pucId": 89213
              },
              {
                "name": "IVA DESCONTABLE",
                "percentage": 0,
                "pucAccount": "731570005",
                "pucId": 89215
              },
              {
                "name": "IMPUESTO AL CONSUMO",
                "percentage": 0,
                "pucAccount": "731570010",
                "pucId": 89216
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "731595005",
                "pucId": 89218
              },
              {
                "name": "TERRENOS",
                "percentage": 0,
                "pucAccount": "734505005",
                "pucId": 89346
              },
              {
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucAccount": "734510005",
                "pucId": 89348
              },
              {
                "name": "MAQUINARIA Y EQUIPO",
                "percentage": 0,
                "pucAccount": "734515005",
                "pucId": 89350
              },
              {
                "name": "EQUIPO DE COMPUTACION Y COMUNICACION",
                "percentage": 0,
                "pucAccount": "734525005",
                "pucId": 89352
              },
              {
                "name": "EQUIPO MEDICO-CIENTIFICO",
                "percentage": 0,
                "pucAccount": "734530005",
                "pucId": 89354
              },
              {
                "name": "EQUIPO DE HOTELES Y RESTAURANTES",
                "percentage": 0,
                "pucAccount": "734535005",
                "pucId": 89356
              },
              {
                "name": "FLOTA Y EQUIPO DE TRANSPORTE",
                "percentage": 0,
                "pucAccount": "734540005",
                "pucId": 89358
              },
              {
                "name": "FLOTA Y EQUIPO FLUVIAL Y/O MARITIMO",
                "percentage": 0,
                "pucAccount": "734545005",
                "pucId": 89360
              },
              {
                "name": "FLOTA Y EQUIPO AEREO",
                "percentage": 0,
                "pucAccount": "734550005",
                "pucId": 89362
              },
              {
                "name": "FLOTA Y EQUIPO FERREO",
                "percentage": 0,
                "pucAccount": "734555005",
                "pucId": 89364
              },
              {
                "name": "ACUEDUCTOS, PLANTAS Y REDES",
                "percentage": 0,
                "pucAccount": "734560005",
                "pucId": 89366
              },
              {
                "name": "ARMAMENTO DE VIGILANCIA",
                "percentage": 0,
                "pucAccount": "734565005",
                "pucId": 89368
              },
              {
                "name": "VIAS DE COMUNICACION",
                "percentage": 0,
                "pucAccount": "734570005",
                "pucId": 89370
              },
              {
                "name": "INSTALACIONES ELECTRICAS",
                "percentage": 0,
                "pucAccount": "735005005",
                "pucId": 89375
              },
              {
                "name": "ARREGLOS ORNAMENTALES",
                "percentage": 0,
                "pucAccount": "735010005",
                "pucId": 89377
              },
              {
                "name": "REPARACIONES LOCATIVAS",
                "percentage": 0,
                "pucAccount": "735015005",
                "pucId": 89379
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "735095005",
                "pucId": 89381
              },
              {
                "name": "INDUSTRIA Y COMERCIO",
                "percentage": 0,
                "pucAccount": "741505005",
                "pucId": 89578
              },
              {
                "name": "DE TIMBRES",
                "percentage": 0,
                "pucAccount": "741510005",
                "pucId": 89580
              },
              {
                "name": "A LA PROPIEDAD RAIZ",
                "percentage": 0,
                "pucAccount": "741515005",
                "pucId": 89582
              },
              {
                "name": "DERECHOS SOBRE INSTRUMENTOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "741520005",
                "pucId": 89584
              },
              {
                "name": "DE VALORIZACION",
                "percentage": 0,
                "pucAccount": "741525005",
                "pucId": 89586
              },
              {
                "name": "DE TURISMO",
                "percentage": 0,
                "pucAccount": "741530005",
                "pucId": 89588
              },
              {
                "name": "TASA POR UTILIZACION DE PUERTOS",
                "percentage": 0,
                "pucAccount": "741535005",
                "pucId": 89590
              },
              {
                "name": "DE VEHICULOS",
                "percentage": 0,
                "pucAccount": "741540005",
                "pucId": 89592
              },
              {
                "name": "DE ESPECTACULOS PUBLICOS",
                "percentage": 0,
                "pucAccount": "741545005",
                "pucId": 89594
              },
              {
                "name": "CUOTAS DE FOMENTO",
                "percentage": 0,
                "pucAccount": "741550005",
                "pucId": 89596
              },
              {
                "name": "IVA DESCONTABLE",
                "percentage": 0,
                "pucAccount": "741570005",
                "pucId": 89598
              },
              {
                "name": "IMPUESTO AL CONSUMO",
                "percentage": 0,
                "pucAccount": "741570010",
                "pucId": 89599
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "741595005",
                "pucId": 89601
              },
              {
                "name": "TERRENOS",
                "percentage": 0,
                "pucAccount": "744505005",
                "pucId": 89729
              },
              {
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucAccount": "744510005",
                "pucId": 89731
              },
              {
                "name": "MAQUINARIA Y EQUIPO",
                "percentage": 0,
                "pucAccount": "744515005",
                "pucId": 89733
              },
              {
                "name": "EQUIPO DE COMPUTACION Y COMUNICACION",
                "percentage": 0,
                "pucAccount": "744525005",
                "pucId": 89735
              },
              {
                "name": "EQUIPO MEDICO-CIENTIFICO",
                "percentage": 0,
                "pucAccount": "744530005",
                "pucId": 89737
              },
              {
                "name": "EQUIPO DE HOTELES Y RESTAURANTES",
                "percentage": 0,
                "pucAccount": "744535005",
                "pucId": 89739
              },
              {
                "name": "FLOTA Y EQUIPO DE TRANSPORTE",
                "percentage": 0,
                "pucAccount": "744540005",
                "pucId": 89741
              },
              {
                "name": "FLOTA Y EQUIPO FLUVIAL Y/O MARITIMO",
                "percentage": 0,
                "pucAccount": "744545005",
                "pucId": 89743
              },
              {
                "name": "FLOTA Y EQUIPO AEREO",
                "percentage": 0,
                "pucAccount": "744550005",
                "pucId": 89745
              },
              {
                "name": "FLOTA Y EQUIPO FERREO",
                "percentage": 0,
                "pucAccount": "744555005",
                "pucId": 89747
              },
              {
                "name": "ACUEDUCTOS, PLANTAS Y REDES",
                "percentage": 0,
                "pucAccount": "744560005",
                "pucId": 89749
              },
              {
                "name": "ARMAMENTO DE VIGILANCIA",
                "percentage": 0,
                "pucAccount": "744565005",
                "pucId": 89751
              },
              {
                "name": "VIAS DE COMUNICACION",
                "percentage": 0,
                "pucAccount": "744570005",
                "pucId": 89753
              },
              {
                "name": "INSTALACIONES ELECTRICAS",
                "percentage": 0,
                "pucAccount": "745005005",
                "pucId": 89758
              },
              {
                "name": "ARREGLOS ORNAMENTALES",
                "percentage": 0,
                "pucAccount": "745010005",
                "pucId": 89760
              },
              {
                "name": "REPARACIONES LOCATIVAS",
                "percentage": 0,
                "pucAccount": "745015005",
                "pucId": 89762
              },
              {
                "name": "OTROS",
                "percentage": 0,
                "pucAccount": "745095005",
                "pucId": 89764
              }
            ],
            "purchaseReteIVA": False,
            "quantity": False,
            "reteICAOtherTaxes": False,
            "reteICAPurchase": False,
            "reteICASale": False,
            "retention": False,
            "retirementExpensesPropertyPlantEquipment": False,
            "returningCustomer": False,
            "revolvingFundPayoutTo": False,
            "saleByThirdParties": False,
            "saleCommissionsThirdParty": False,
            "salesReteIVA": False,
            "salesTaxPaidSimplifiedRegimen": False,
            "sanctionsPayingTaxes": False,
            "sellerRequire": False,
            "serviceExpenses": False,
            "soiTaxCreditContributions": False,
            "staffCosts": False,
            "subAccount": "35",
            "subAccountName": "COSTOS Y GASTOS POR PAGAR",
            "subsistenceFundContributions": False,
            "taxExpenseIndustryCommerce": False,
            "technicalServiceFromAbroadWithoutAgreement": False,
            "third": False,
            "thirdRequiredDCNB": False,
            "typesCreditInventoryAdjustment": False,
            "typesDebitInventoryAdjustment": False,
            "updateBy": "Administrador del Sistema",
            "updateDate": "Fri, 09 Aug 2013 11:25:32 GMT",
            "utilitiesAndOrLossesLastYear": False,
            "vacation": False,
            "valueProduction": False,
            "valuesReceivedThirdParties": False,
            "weightAdjustmentExpense": False,
            "withholdingCREEPurchase": False,
            "withholdingCREESale": False,
            "withholdingFinancialIncome": False,
            "withholdingRetainingSale": False,
            "withholdingRetainingService": False,
            "withholdingTaxPurchase": False,
            "withholdingTaxSalary": False,
            "withholdingTaxSale": False,
            "yearEndClose": False
          },
          "pucId": 85616,
          "quotaNumbers": 0,
          "realSimulated": None,
          "requisitionNumber": "",
          "reteICABase": 0,
          "reteICAPUC": None,
          "reteICAPUCId": None,
          "reteICAPercent": None,
          "reteICAValue": 0,
          "reteIVABase": 0,
          "reteIVAPUC": None,
          "reteIVAPUCId": None,
          "reteIVAPercent": None,
          "reteIVAValue": 0,
          "retentionMode": 0,
          "retentionPUC": None,
          "retentionPUCId": None,
          "retentionPercent": 0,
          "retentionValue": 0,
          "retirement": None,
          "revolvingFund": 0,
          "sanction": None,
          "section": None,
          "sectionId": None,
          "semester": None,
          "shipAddress": None,
          "shipCity": None,
          "shipCountry": None,
          "shipDepartment": None,
          "shipPhone": None,
          "shipTo": None,
          "shipZipCode": None,
          "sodicon": 0,
          "source": {
            "shortWord": "FP"
          },
          "sourceDocument": "",
          "sourceDocumentHeader": {
            "providerId": 26,
            "documentHeaderId": 117556,
            "documentDetails": [
              {
                "colorId": 2,
                "units": 23,
                "balance": 23,
                "quantity": 23,
                "sizeId": 2,
                "itemId": 1751,
                "lot": None,
                "sourceDocumentDetailId": None,
                "dueDate": None,
                "documentDetailId": 305379,
                "value": 2300
              },{
                "colorId": None,
                "units": 56,
                "balance": 56,
                "quantity": 56,
                "sizeId": None,
                "itemId": 40,
                "lot": None,
                "sourceDocumentDetailId": None,
                "dueDate": None,
                "documentDetailId": 305566,
                "value": 104197.8672
              },{
                "colorId": None,
                "units": 8,
                "balance": 8,
                "quantity": 8,
                "sizeId": None,
                "itemId": 27,
                "lot": None,
                "sourceDocumentDetailId": None,
                "dueDate": None,
                "documentDetailId": 305567,
                "value": 33999.52
              }
            ],
            "nameComplete": "0000002888 | 28/12/2016 | 529.7 | PRINCIPAL |  (P)",
            "documentDate": "Wed, 28 Dec 2016 11:28:44 GMT",
            "total": 139092.41,
            "state": True,
            "documentNumber": "0000002888"
          },
          "sourceDocumentHeaderId": 117556,
          "sourceDocumentType": {
            "documentTypeId": 49,
            "isIncomePayment": None,
            "isDeleted": 0,
            "updateBy": "009",
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "createdBy": "Migracion",
            "needResolution": 0,
            "shortWord": "FP",
            "comments": None,
            "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~PurchaseOrders",
            "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "name": "FACTURA DE PROVEEDOR"
          },
          "sourceDocumentTypeId": 49,
          "sourceId": 49,
          "sourcePrefix": "",
          "sourceWarehouse": None,
          "sourceWarehouseId": None,
          "stage": None,
          "stageCostTotal": None,
          "stageId": None,
          "state": 0,
          "termDays": 1,
          "third": None,
          "thirdId": None,
          "tipValue": 0,
          "typeAccount": None,
          "typeThirdParty": None,
          "vacation": 0,
          "vacationDateFrom": None,
          "valueCREE": 0,
          "withholdingCREEPUC": None,
          "withholdingCREEPUCId": None,
          "withholdingTaxPUC": None,
          "withholdingTaxPUCId": None,
          "withholdingTaxPercent": 3.5,
          "workNumber": "",
          "year": None
        }
        provider_note_cp = {
          "sourceDocumentTypeId": 49,
          "costCenterId": 4,
          "branchId": 14,
          "sourceDocumentHeader": {
            "documentDetails": [
              {
                "puc": None,
                "sourceDocumentTypeId": None,
                "asset": None,
                "costCenterId": 4,
                "finalDate": None,
                "kitItemId": None,
                "unitValue": 1000,
                "detailDate": "Fri, 24 Mar 2017 11:44:15 GMT",
                "financialEntityId": None,
                "withholdingValue": None,
                "creationDate": "Fri, 24 Mar 2017 14:25:04 GMT",
                "pucId": None,
                "businessAgentId": None,
                "sourceDocumentDetailId": None,
                "value": 2000,
                "colorId": None,
                "detailWarehouseId": 6,
                "thirdId": None,
                "iva": 16,
                "item": {
                  "percentagePurchaseIVA": 16,
                  "priceListA7": 0,
                  "priceList10": 0,
                  "inventoryGroup": None,
                  "priceList7": 0,
                  "withholdingICA": True,
                  "priceListA8": 0,
                  "ivaPurchasePUC": {
                    "pucId": 85796,
                    "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                    "percentage": 16
                  },
                  "priceListA2": 0,
                  "percentageICA": 5,
                  "creationDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                  "inventoryPUCId": 84706,
                  "description": None,
                  "measurementUnit2": {
                    "measurementUnitId": 36,
                    "code": "UNI",
                    "name": "UNIDADES                      "
                  },
                  "measurementUnit3Id": None,
                  "incomingPUCId": 2520,
                  "size": False,
                  "plu": None,
                  "ivaSalePUC": {
                    "pucId": 85778,
                    "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                    "percentage": 16
                  },
                  "barCode": None,
                  "reference": None,
                  "consumptionPercentage": 0,
                  "lastPurchaseDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                  "namePOS": "NORMAL",
                  "measurementUnitId": 42,
                  "priceListB1": 0,
                  "subInventoryGroups1": None,
                  "inventoryGroupId": None,
                  "discountPercentage": 0,
                  "priceListA1": 600,
                  "priceListB6": 0,
                  "priceList8": 0,
                  "conversionFactor2": 0,
                  "priceList9": 0,
                  "companyId": 1,
                  "updateDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                  "withholdingTaxSalePUCId": 84521,
                  "priceListB4": 0,
                  "costPUC": {
                    "pucId": 88508,
                    "pucAccount": "613550005 VENTA DE QUIMICOS",
                    "percentage": 0
                  },
                  "withholdingSalePercentage": 0,
                  "name": "NORMAL",
                  "purchaseIVA": {
                    "ivaId": 2,
                    "code": "G",
                    "name": "GRAVADO"
                  },
                  "priceList2": 0,
                  "addConsumptionToCost": False,
                  "purchaseIVAId": 2,
                  "priceList5": 0,
                  "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                  "photo": None,
                  "priceListB10": 0,
                  "priceListA10": 0,
                  "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                  "priceList6": 0,
                  "providerId": None,
                  "lastCost": 0,
                  "priceListB2": 0,
                  "addConsumptionToPurchase": False,
                  "invimaDueDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                  "priceListB5": 0,
                  "subInventoryGroup2": None,
                  "itemId": 1850,
                  "minimumStock": 0,
                  "costPUCId": 88508,
                  "priceList3": 0,
                  "saleIVAId": 2,
                  "conversionFactor": 10,
                  "withholdingTaxPurchasePUCId": 85677,
                  "ivaSalePUCId": 85778,
                  "code": "NORMAL",
                  "measurementUnit": {
                    "measurementUnitId": 42,
                    "code": "CAJ",
                    "name": "CAJAS                         "
                  },
                  "withholdingPurchasePercentage": 3.5,
                  "subInventoryGroup3Id": None,
                  "withholdingTaxSalePUC": {
                    "pucId": 84521,
                    "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                    "percentage": 3.5
                  },
                  "subInventoryGroup2Id": None,
                  "priceListB8": 0,
                  "priceListA3": 0,
                  "measurementUnit2Id": 36,
                  "percentageSaleIVA": 16,
                  "orderQuantity": 0,
                  "priceListA4": 0,
                  "withholdingTaxPurchasePUC": {
                    "pucId": 85677,
                    "pucAccount": "236540005 COMPRAS 3.5%",
                    "percentage": 3.5
                  },
                  "companyCost": 1000,
                  "priceListB3": 0,
                  "invimaRegister": None,
                  "state": "A",
                  "priceList1": 5000,
                  "measurementUnit3": None,
                  "incomingPUC": {
                    "pucId": 2520,
                    "pucAccount": "413550005 VENTA DE QUIMICOS",
                    "percentage": 0
                  },
                  "typeItem": "A",
                  "priceListA9": 0,
                  "serial": False,
                  "subInventoryGroup1Id": None,
                  "consumptionPUCId": None,
                  "lot": False,
                  "priceListA6": 0,
                  "ivaPurchasePUCId": 85796,
                  "consumptionPUC": None,
                  "priceListA5": 0,
                  "priceListB7": 0,
                  "saleIVA": {
                    "ivaId": 2,
                    "code": "G",
                    "name": "GRAVADO"
                  },
                  "weight": 0,
                  "disccountToUnitValue": False,
                  "brandId": None,
                  "imageId": None,
                  "priceListB9": 0,
                  "color": False,
                  "inventoryPUC": {
                    "pucId": 84706,
                    "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                    "percentage": 0
                  },
                  "averageCost": 0,
                  "priceList4": 0,
                  "subInventoryGroup3": None,
                  "packagePrice": 0,
                  "isDeleted": False,
                  "addIVAtoCost": False
                },
                "sectionId": 7,
                "surcharge": None,
                "detailDocument": None,
                "globalTax": None,
                "measurementUnitId": 42,
                "withholdingTax": 3.5,
                "payrollConceptId": None,
                "assetId": None,
                "overCost": None,
                "physicalLocation": None,
                "updateDate": "Fri, 24 Mar 2017 14:25:04 GMT",
                "amount": None,
                "consumptionTaxValue": 0,
                "employeeId": None,
                "sizeId": None,
                "consumptionTaxBase": 2000,
                "payrollEntityId": None,
                "sourceDocumentDetail": None,
                "mainUnitValue": None,
                "importConceptId": None,
                "quantityRefund": None,
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "providerId": None,
                "otherThirdId": None,
                "icaPercent": None,
                "third": None,
                "partnerId": None,
                "cost": None,
                "customerId": None,
                "crossDocumentHeaderId": None,
                "itemId": 1850,
                "search": None,
                "sourceDocumentPrefix": None,
                "conversionFactor": 1,
                "documentDetailId": 306709,
                "percentCost": None,
                "bankCode": None,
                "reteICA": None,
                "disccount": 0,
                "sourceDocumentNumber": None,
                "kitAssetId": None,
                "listSerials": [],
                "bankName": None,
                "kitLaborId": None,
                "pieceId": None,
                "accountNumber": None,
                "authorizationNumber": None,
                "consumptionTaxPercent": 0,
                "cashRegisterId": None,
                "divisionId": 13,
                "interest": None,
                "detailDocumentTypeId": 49,
                "detailPrefix": None,
                "checkNumber": None,
                "withholdingTaxPUCId": 85677,
                "isDeleted": 0,
                "lot": None,
                "balance": 2,
                "ivaCustomer": None,
                "selected": None,
                "dueDate": None,
                "ivaPUCId": 85796,
                "dependencyId": None,
                "initialDate": None,
                "consumptionTaxPUCId": None,
                "units": 2,
                "quoteNumber": None,
                "baseValue": 2000,
                "availableStock": None,
                "quantity": 2,
                "comments": None,
                "documentHeaderId": 118663,
                "reteICAPercent": None,
                "bankAccountId": None
              }
            ]
          },
          "documentDetails": [
            {
              "puc": None,
              "sourceDocumentTypeId": None,
              "asset": None,
              "costCenterId": 4,
              "finalDate": None,
              "kitItemId": None,
              "und": {
                "measurementUnitId": 42,
                "code": "CAJ",
                "name": "CAJAS                         "
              },
              "unitValue": 1000,
              "detailDate": "Fri, 24 Mar 2017 11:44:15 GMT",
              "financialEntityId": None,
              "withholdingValue": None,
              "creationDate": "Fri, 24 Mar 2017 14:25:04 GMT",
              "pucId": None,
              "businessAgentId": None,
              "sourceDocumentDetailId": None,
              "value": 5000,
              "size": False,
              "colorId": None,
              "detailWarehouseId": 6,
              "thirdId": None,
              "iva": 16,
              "item": {
                "percentagePurchaseIVA": 16,
                "priceListA7": 0,
                "priceList10": 0,
                "inventoryGroup": None,
                "priceList7": 0,
                "withholdingICA": True,
                "priceListA8": 0,
                "ivaPurchasePUC": {
                  "pucId": 85796,
                  "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                  "percentage": 16
                },
                "priceListA2": 0,
                "percentageICA": 5,
                "creationDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                "inventoryPUCId": 84706,
                "description": None,
                "measurementUnit2": {
                  "measurementUnitId": 36,
                  "code": "UNI",
                  "name": "UNIDADES                      "
                },
                "measurementUnit3Id": None,
                "incomingPUCId": 2520,
                "size": False,
                "plu": None,
                "ivaSalePUC": {
                  "pucId": 85778,
                  "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                  "percentage": 16
                },
                "barCode": None,
                "reference": None,
                "consumptionPercentage": 0,
                "lastPurchaseDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                "namePOS": "NORMAL",
                "measurementUnitId": 42,
                "priceListB1": 0,
                "subInventoryGroups1": None,
                "inventoryGroupId": None,
                "discountPercentage": 0,
                "priceListA1": 600,
                "priceListB6": 0,
                "priceList8": 0,
                "conversionFactor2": 0,
                "priceList9": 0,
                "companyId": 1,
                "updateDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                "withholdingTaxSalePUCId": 84521,
                "priceListB4": 0,
                "costPUC": {
                  "pucId": 88508,
                  "pucAccount": "613550005 VENTA DE QUIMICOS",
                  "percentage": 0
                },
                "withholdingSalePercentage": 0,
                "name": "NORMAL",
                "purchaseIVA": {
                  "ivaId": 2,
                  "code": "G",
                  "name": "GRAVADO"
                },
                "priceList2": 0,
                "addConsumptionToCost": False,
                "purchaseIVAId": 2,
                "priceList5": 0,
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "photo": None,
                "priceListB10": 0,
                "priceListA10": 0,
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "priceList6": 0,
                "providerId": None,
                "lastCost": 0,
                "priceListB2": 0,
                "addConsumptionToPurchase": False,
                "invimaDueDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                "priceListB5": 0,
                "subInventoryGroup2": None,
                "itemId": 1850,
                "minimumStock": 0,
                "costPUCId": 88508,
                "priceList3": 0,
                "saleIVAId": 2,
                "conversionFactor": 10,
                "withholdingTaxPurchasePUCId": 85677,
                "ivaSalePUCId": 85778,
                "code": "NORMAL",
                "measurementUnit": {
                  "measurementUnitId": 42,
                  "code": "CAJ",
                  "name": "CAJAS                         "
                },
                "withholdingPurchasePercentage": 3.5,
                "subInventoryGroup3Id": None,
                "withholdingTaxSalePUC": {
                  "pucId": 84521,
                  "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                  "percentage": 3.5
                },
                "subInventoryGroup2Id": None,
                "priceListB8": 0,
                "priceListA3": 0,
                "measurementUnit2Id": 36,
                "percentageSaleIVA": 16,
                "orderQuantity": 0,
                "priceListA4": 0,
                "withholdingTaxPurchasePUC": {
                  "pucId": 85677,
                  "pucAccount": "236540005 COMPRAS 3.5%",
                  "percentage": 3.5
                },
                "companyCost": 1000,
                "priceListB3": 0,
                "invimaRegister": None,
                "state": "A",
                "priceList1": 5000,
                "measurementUnit3": None,
                "incomingPUC": {
                  "pucId": 2520,
                  "pucAccount": "413550005 VENTA DE QUIMICOS",
                  "percentage": 0
                },
                "typeItem": "A",
                "priceListA9": 0,
                "serial": False,
                "subInventoryGroup1Id": None,
                "consumptionPUCId": None,
                "lot": False,
                "priceListA6": 0,
                "ivaPurchasePUCId": 85796,
                "consumptionPUC": None,
                "priceListA5": 0,
                "priceListB7": 0,
                "saleIVA": {
                  "ivaId": 2,
                  "code": "G",
                  "name": "GRAVADO"
                },
                "weight": 0,
                "disccountToUnitValue": False,
                "brandId": None,
                "imageId": None,
                "priceListB9": 0,
                "color": False,
                "inventoryPUC": {
                  "pucId": 84706,
                  "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                  "percentage": 0
                },
                "averageCost": 0,
                "priceList4": 0,
                "subInventoryGroup3": None,
                "packagePrice": 0,
                "isDeleted": False,
                "addIVAtoCost": False
              },
              "sectionId": 7,
              "surcharge": None,
              "detailDocument": None,
              "globalTax": None,
              "name": "NORMAL",
              "measurementUnitId": 42,
              "withholdingTax": 3.5,
              "payrollConceptId": None,
              "itemToCompare": {
                "percentagePurchaseIVA": 16,
                "priceListA7": 0,
                "priceList10": 0,
                "inventoryGroup": None,
                "priceList7": 0,
                "withholdingICA": True,
                "priceListA8": 0,
                "ivaPurchasePUC": {
                  "pucId": 85796,
                  "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                  "percentage": 16
                },
                "priceListA2": 0,
                "percentageICA": 5,
                "creationDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                "inventoryPUCId": 84706,
                "description": None,
                "measurementUnit2": {
                  "measurementUnitId": 36,
                  "code": "UNI",
                  "name": "UNIDADES                      "
                },
                "measurementUnit3Id": None,
                "incomingPUCId": 2520,
                "size": False,
                "plu": None,
                "ivaSalePUC": {
                  "pucId": 85778,
                  "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                  "percentage": 16
                },
                "barCode": None,
                "reference": None,
                "consumptionPercentage": 0,
                "lastPurchaseDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                "namePOS": "NORMAL",
                "measurementUnitId": 42,
                "priceListB1": 0,
                "subInventoryGroups1": None,
                "inventoryGroupId": None,
                "discountPercentage": 0,
                "priceListA1": 600,
                "priceListB6": 0,
                "priceList8": 0,
                "conversionFactor2": 0,
                "priceList9": 0,
                "companyId": 1,
                "updateDate": "Thu, 02 Feb 2017 15:14:10 GMT",
                "withholdingTaxSalePUCId": 84521,
                "priceListB4": 0,
                "costPUC": {
                  "pucId": 88508,
                  "pucAccount": "613550005 VENTA DE QUIMICOS",
                  "percentage": 0
                },
                "withholdingSalePercentage": 0,
                "name": "NORMAL",
                "purchaseIVA": {
                  "ivaId": 2,
                  "code": "G",
                  "name": "GRAVADO"
                },
                "priceList2": 0,
                "addConsumptionToCost": False,
                "purchaseIVAId": 2,
                "priceList5": 0,
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "photo": None,
                "priceListB10": 0,
                "priceListA10": 0,
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "priceList6": 0,
                "providerId": None,
                "lastCost": 0,
                "priceListB2": 0,
                "addConsumptionToPurchase": False,
                "invimaDueDate": "Thu, 02 Feb 2017 09:45:21 GMT",
                "priceListB5": 0,
                "subInventoryGroup2": None,
                "itemId": 1850,
                "minimumStock": 0,
                "costPUCId": 88508,
                "priceList3": 0,
                "saleIVAId": 2,
                "conversionFactor": 10,
                "withholdingTaxPurchasePUCId": 85677,
                "ivaSalePUCId": 85778,
                "code": "NORMAL",
                "measurementUnit": {
                  "measurementUnitId": 42,
                  "code": "CAJ",
                  "name": "CAJAS                         "
                },
                "withholdingPurchasePercentage": 3.5,
                "subInventoryGroup3Id": None,
                "withholdingTaxSalePUC": {
                  "pucId": 84521,
                  "pucAccount": "135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%",
                  "percentage": 3.5
                },
                "subInventoryGroup2Id": None,
                "priceListB8": 0,
                "priceListA3": 0,
                "measurementUnit2Id": 36,
                "percentageSaleIVA": 16,
                "orderQuantity": 0,
                "priceListA4": 0,
                "withholdingTaxPurchasePUC": {
                  "pucId": 85677,
                  "pucAccount": "236540005 COMPRAS 3.5%",
                  "percentage": 3.5
                },
                "companyCost": 1000,
                "priceListB3": 0,
                "invimaRegister": None,
                "state": "A",
                "priceList1": 5000,
                "measurementUnit3": None,
                "incomingPUC": {
                  "pucId": 2520,
                  "pucAccount": "413550005 VENTA DE QUIMICOS",
                  "percentage": 0
                },
                "typeItem": "A",
                "priceListA9": 0,
                "serial": False,
                "subInventoryGroup1Id": None,
                "consumptionPUCId": None,
                "lot": False,
                "priceListA6": 0,
                "ivaPurchasePUCId": 85796,
                "consumptionPUC": None,
                "priceListA5": 0,
                "priceListB7": 0,
                "saleIVA": {
                  "ivaId": 2,
                  "code": "G",
                  "name": "GRAVADO"
                },
                "weight": 0,
                "disccountToUnitValue": False,
                "brandId": None,
                "imageId": None,
                "priceListB9": 0,
                "color": False,
                "inventoryPUC": {
                  "pucId": 84706,
                  "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                  "percentage": 0
                },
                "averageCost": 0,
                "priceList4": 0,
                "subInventoryGroup3": None,
                "packagePrice": 0,
                "isDeleted": False,
                "addIVAtoCost": False
              },
              "assetId": None,
              "withholdingICA": True,
              "overCost": None,
              "physicalLocation": None,
              "updateDate": "Fri, 24 Mar 2017 14:25:04 GMT",
              "amount": None,
              "exchangeRate": None,
              "consumptionTaxValue": 0,
              "employeeId": None,
              "sizeId": None,
              "withholdingTaxPUC": {
                "pucId": 85677,
                "pucAccount": "236540005 COMPRAS 3.5%",
                "percentage": 3.5
              },
              "consumptionTaxBase": 5000,
              "payrollEntityId": None,
              "mainUnitValue": None,
              "importConceptId": None,
              "quantityRefund": None,
              "updateBy": "ADMINISTRADOR UPDATE del Sistema",
              "valueNP": 2000,
              "createdBy": "ADMINISTRADOR UPDATE del Sistema",
              "providerId": None,
              "otherThirdId": None,
              "icaPercent": None,
              "third": None,
              "partnerId": None,
              "cost": None,
              "measurementUnits": [
                {
                  "measurementUnitId": 42,
                  "code": "CAJ",
                  "name": "CAJAS                         "
                },
                {
                  "measurementUnitId": 36,
                  "code": "UNI",
                  "name": "UNIDADES                      "
                }
              ],
              "customerId": None,
              "crossDocumentHeaderId": None,
              "itemId": 1850,
              "search": None,
              "sourceDocumentPrefix": None,
              "conversionFactor": 1,
              "documentDetailId": 306709,
              "code": "NORMAL",
              "percentCost": None,
              "bankCode": None,
              "reteICA": None,
              "disccount": 0,
              "sourceDocumentNumber": None,
              "kitAssetId": None,
              "listSerials": [],
              "bankName": None,
              "kitLaborId": None,
              "ivaPurchasePUC": {
                "pucId": 85796,
                "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "percentage": 16
              },
              "badgeValue": None,
              "pieceId": None,
              "accountNumber": None,
              "authorizationNumber": None,
              "consumptionTaxPercent": 0,
              "cashRegisterId": None,
              "divisionId": 13,
              "interest": None,
              "detailDocumentTypeId": 49,
              "detailPrefix": None,
              "checkNumber": None,
              "withholdingTaxPUCId": 85677,
              "isDeleted": 0,
              "lot": None,
              "sourceDocumentDetail": None,
              "ivaCustomer": None,
              "selected": None,
              "dueDate": None,
              "indexItem": 0,
              "ivaPUCId": 85796,
              "dependencyId": None,
              "initialDate": None,
              "consumptionTaxPUCId": None,
              "units": 2,
              "color": False,
              "quoteNumber": None,
              "baseValue": 5000,
              "detailWarehouse": {
                "codeComplete": "Código 002",
                "warehouseId": 6,
                "typeWarehouse": "S",
                "code": "002",
                "name": "LEGAQUIMICOS MODIFICAD"
              },
              "availableStock": None,
              "quantity": 2,
              "comments": None,
              "balance": 2,
              "reteICAPercent": None,
              "bankAccountId": None
            }
          ],
          "documentDate": "2017-03-30T08:52:00.000Z",
          "applyCree": None,
          "reteICABase": 0,
          "reteICAValue": 12,
          "termDays": 15,
          "percentageCREE": 0,
          "withholdingTaxValue": 175,
          "dependencyId": None,
          "valueCREE": 0,
          "ivaValue": 800,
          "reteIVAValue": 20,
          "currencyId": 4,
          "sectionId": 7,
          "disccount": 0,
          "baseCREE": 0,
          "paymentTermId": 2,
          "paymentTerm": {
            "needTermDays": 1
          },
          "divisionId": 13,
          "disccount2": 0,
          "comments": None,
          "total": 5478,
          "dateTo": "2017-04-14T13:52:29.729Z",
          "provider": {
            "thirdPartyId": 194,
            "branch": "01",
            "providerId": 456,
            "isWithholdingCREE": 0,
            "name": " ALFARO AMORTEGUI OMAR (11436655) - NORTE"
          },
          "payment": 5478,
          "paymentReceipt": {},
          "sourceShortWord": "DP",
          "reteIVAPercent": "2.50",
          "documentNumber": "0000000012",
          "subtotal": 5000,
          "overCost": 0,
          "sourceDocumentHeaderId": 118663,
          "costCenter": None,
          "exchangeRate": 1,
          "retentionValue": 115,
          "consumptionTaxValue": 0,
          "shortWord": "CP",
          "sourceDocumentType": {
            "needResolution": 0,
            "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Fact_Provider",
            "documentTypeId": 49,
            "isIncomePayment": None,
            "updateBy": "011",
            "createdBy": "Migracion",
            "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "comments": None,
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "shortWord": "FP",
            "isDeleted": 0,
            "name": "FACTURA DE PROVEEDOR"
          },
          "sourceDocumentOrigin": "FP",
          "reteIVABase": 800,
          "reteICAPercent": "2.40",
          "controlPrefix": None,
          "documentAffecting": [],
          "annuled": None,
          "disccount2TaxBase": 0,
          "controlNumber": None,
          "disccount2Value": 0,
          "retentionPercent": "2.30",
          "providerId": 456,
          "retentionPUCId": 85843
        }

        ######
        #  Envio la creacion de la nota sin short word
        provider_note_dp["shortWord"] = None
        response = self.request_post(provider_note_dp)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        provider_note_cp["shortWord"] = None
        response = self.request_post(provider_note_cp)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        #####
        #  Envio la creacion del avance con short word erroneo
        provider_note_dp["shortWord"] = "XY"
        response = self.request_post(provider_note_dp)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        provider_note_cp["shortWord"] = "XY"
        response = self.request_post(provider_note_cp)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        #####
        # Agrega el short word correcto
        provider_note_dp["shortWord"] = "DP"
        response = self.request_post(provider_note_dp)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        provider_note_cp["shortWord"] = "CP"
        response = self.request_post(provider_note_cp)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number1 = response.json['documentNumber']
        self.id1 = response.json['id']

        ###
        # Consulta la nota
        response = self.request_get('', '/search?branch_id=14&short_word=DP&document_number=' + self.document_number0)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)

        provider_note1 = response.json
        response = self.request_put("", "/"+str(self.id0)+"/preview")

        response = self.request_get('', '/search?branch_id=14&short_word=CP&document_number=' + self.document_number1)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)

        provider_note2 = response.json
        response = self.request_put("", "/"+str(self.id1)+"/preview")



        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy_dp = copy.deepcopy(provider_note1)
        purchase_copy_cp = copy.deepcopy(provider_note2)
        print("VALUE>>>> ", purchase_copy_cp['documentDetails'][0]['value'])
        # Cambio el total
        purchase_copy_dp['documentDetails'][0]['value'] = 1000
        purchase_copy_cp['documentDetails'][0]['value'] = 1000

        ####
        #  Actualizacion de la nota
        response = self.request_put(purchase_copy_dp, "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)
        # Espero un error por descuadre...
        self.assertEquals(response.status_code, 500)
        self.assertIn("message", response.json)


        response = self.request_put(purchase_copy_cp, "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)
        # Espero un error por descuadre...
        self.assertEquals(response.status_code, 500)
        self.assertIn("message", response.json)


        ####
        #  Establece el valor correcto a la compra
        purchase_copy_dp['documentDetails'][0]['value'] = 500000
        purchase_copy_cp['documentDetails'][0]['value'] = 500000
        # Realiza un cambio del comentario
        purchase_copy_dp['comments'] = "Este es el test"
        purchase_copy_cp['comments'] = "Este es el test"

        # Peticion de actualizado para la nota
        response = self.request_put(purchase_copy_dp, "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        # Peticion de actualizado para la nota
        response = self.request_put(purchase_copy_cp, "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)

        #####
        # Establece el valor correcto a la compra
        purchase_copy_dp['documentDetails'][0]['value'] = 480000.1
        purchase_copy_cp['documentDetails'][0]['value'] = 5000.1
        # Realiza un cambio del comentario
        purchase_copy_dp['comments'] = "Este es el test"
        purchase_copy_cp['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy_dp, "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy_cp, "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        ######
        # Cambio d estado
        purchase_copy_dp['documentDetails'][0]['value'] = 480000
        purchase_copy_dp['comments'] = "Este es el test"
        purchase_copy_cp['documentDetails'][0]['value'] = 5000
        purchase_copy_cp['comments'] = "Este es el test"
        purchase_copy_cp['annuled'] = 1
        # Actualizo nuevamente
        response = self.request_put(purchase_copy_dp, "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Actualizo nuevamente
        response = self.request_put(purchase_copy_cp, "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)


        # Cambio el estado del documento
        purchase_copy_dp['annuled'] = 1
        # Envio a actualizar
        response = self.request_put(purchase_copy_dp, "/" + str(self.id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Cambio el estado del documento
        purchase_copy_cp['annuled'] = 1
        # Envio a actualizar
        response = self.request_put(purchase_copy_cp, "/" + str(self.id1))
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

        response = self.request_delete("", "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id1))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('PROVIDER NOTE NOT FOUND', response.json['message'].upper(),
                         'incorrect response by bad request')

        response = self.request_delete("", "/" + str(self.purchase_item_id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

