#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
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
handled refund_provider
"""
class RefoundProvider(unittest.TestCase):
    """
    This Class is a  Test Case for refund_provider API class
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
        """Sent get request to #/api/v1/refund_provider# with refund_provider data values

        :param data: refund_provider data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/refund_providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/refund_provider# with refund_provider data values

        :param data: refund_provider data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/refund_providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/refund_provider# with refund_provider data values

        :param data: refund_provider data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/refund_providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/refund_provider# with refund_provider data values

        :param data: refund_provider data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/refund_providers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_refund_provider(self):
        """
        This function test get a Refund Third according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.request_get('', '/117562') # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        print(">>> ", response.json)
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentTypeId" in response.json, 'incorrect response by correct request')
        self.assertTrue("paymentTermId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0') # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_refund_provider_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=RP&document_number=0000000001")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        refund_provider = response.json['data'][-1]

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400, 'incorrect response by correct request')

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=DR&document_number=0000000066')

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number='+refund_provider['documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=DR&document_number=' + refund_provider['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("","/search?search=dsadsadlsakdjs")
        response.json = json.loads( response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, 'incorrect response by correct request')

        # ################## GET
        response = self.request_get("","/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json['status'], 404, '')

        # Peticion correcta
        response = self.request_get("","/" + str(refund_provider['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/" + str(refund_provider['documentHeaderId'])+"/preview?format=P")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("data", response.json)

    ##################################################################################
    def test_post_put_delete(self):
        """
        This function allow create, update and delete a advance third
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        refund_provider = {
          "retentionBase": 1,
          "withholdingTaxBase": 1,
          "withholdingTaxValue": 1,
          "subtotal": 1,
          "total": 1000,
          "sourceDocumentOrigin": "DR",
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
          "ivaBase": 1,
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
          "documentDetails": [
            {
              "unitValue": 1,
              "quantity": 1,
              "units": 1,
              "baseValue": 2,
              "consumptionTaxBase": 1,
              "withholdingTax": 16,
              "value": 500000,
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
              "importConceptId": None,
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
              "overCost": None,
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
          "documentTypeId": 49,
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
          "ivaValue": 2400,
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
          "provider": {
            "address1": "CRA 13 MO. 10-60",
            "address2": "",
            "branch": "01",
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
            "createdBy": "ADA LUZ LEGUIZAMON FUENTES",
            "creationDate": "Wed, 22 Jan 2014 13:13:53 GMT",
            "creditCapacity": 0,
            "fax": None,
            "isDeleted": 0,
            "isLaw1527": False,
            "isMain": True,
            "name": "IZACIGA SUAREZ HELI ALFREDO/INTERVIDRIOS",
            "phone": "3344618",
            "providerId": 125,
            "state": "A",
            "term": 0,
            "thirdPartyId": 486,
            "updateBy": "ADA LUZ LEGUIZAMON FUENTES",
            "updateDate": "Wed, 22 Jan 2014 13:13:53 GMT",
            "zipCode": ""
          },
          "providerId": 125,
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
            "comments": None,
            "createdBy": "Migracion",
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "documentTypeId": 35,
            "isDeleted": 0,
            "isIncomePayment": None,
            "name": "DEVOLUCION A PROVEEDOR",
            "needResolution": 0,
            "shortWord": "DR",
            "updateBy": "013",
            "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Dev_Prov"
          },
          "sourceDocument": "",
          "sourceDocumentHeader": {
              "source": {
                "comments": None,
                "createdBy": "Migracion",
                "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                "documentTypeId": 35,
                "isDeleted": 0,
                "isIncomePayment": None,
                "name": "DEVOLUCION A PROVEEDOR",
                "needResolution": 0,
                "shortWord": "DR",
                "updateBy": "013",
                "updateDate": "Fri, 17 Aug 2012 10:35:28 GMT",
                "url": "PYMESModule.Presenters.PurchaseInvoicePresenter~Dev_Prov"
              }
          },
          "sourceDocumentHeaderId": None,
          "sourceDocumentType": "DR",
          "sourceDocumentTypeId": 35,
          "sourceId": 35,
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
          "withholdingTaxPercent": None,
          "workNumber": "",
          "shortWord": "DR",
          "sourceShortWord":"DR",
          "year": None
        }

        # Envio la creacion del avance sin short word
        response = self.request_post(refund_provider)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        # self.assertEquals(response.status_code, 400)
        #
        # # Envio la creacion del avance con short word erroneo
        # refund_provider["shortWord"] = "XY"
        # response = self.request_post(refund_provider)
        # response.json = json.loads(response.data.decode("utf-8"))
        # self.assertNotEquals(response.json, {})
        # self.assertIn("error", response.json)
        # self.assertIn("message", response.json)
        # self.assertEquals(response.status_code, 500)
        #
        # # Agrega el short word correcto
        # refund_provider["shortWord"] = "DR"
        # # Crea un avance de tercero con un peso de diferencia en el credito
        # refund_provider['total'] = 500000.1
        # response = self.request_post(refund_provider)
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Obtengo los datos para despues eliminar
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.document_number0 = response.json['documentNumber']
        # self.id0 = response.json['id']
        #
        # # Restaura el valor del avance
        # refund_provider['total'] = 500000
        # refund_provider['paymentReceipt']['paymentDetails'][2]['value'] = 200000.1
        # # Crea un avance de tercero con un peso de diferencia en el debito
        # response = self.request_post(refund_provider)
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Obtengo los datos para despues eliminar
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.document_number0a = response.json['documentNumber']
        # self.id0a = response.json['id']
        #
        # # Crea un avance de tercero correcto con valor exacto
        # refund_provider['total'] = 500000
        # response = self.request_post(refund_provider)
        # response.json = json.loads(response.data.decode("utf-8"))
        #
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.document_number = response.json['documentNumber']
        # self.id = response.json['id']
        # # TODO: la moneda por defecto podria no ser el peso
        # # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        # currency = refund_provider['currency']
        # # FIXME: podria consultar las monedas y obtener una
        # # Establece una moneda distinta
        # currency2 = {"code": "USD",
        #               "currencyId": 2,
        #               "isDeleted": 0,
        #               "name": "DÓLAR AMERICANO",
        #               "symbol": "$"}
        #
        # refund_provider["currency"] = currency2
        # refund_provider["currencyId"] = 2
        # # Crea el avance de tercero con una moneda extranjera
        # response = self.request_post(refund_provider)
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Guarda los datos de este avance para la posterior eliminacion
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.document_number2 = response.json['documentNumber']
        # self.id2 = response.json['id']
        # # Reestablece la moneda actual
        # refund_provider["currency"] = currency
        # refund_provider["currencyId"] = 4
        #
        # # Consulta el avance de tercero
        # response = self.request_get('', '/search?branch_id=14&short_word=DR&document_number=' + self.document_number)
        # self.assertEquals(response.status_code, 200)
        # response.json = json.loads(response.data.decode("utf-8"))
        # self.assertNotEquals(response.json, {})
        # # Verifico algunos de las claves de la respuesta
        # self.assertIn("paymentReceipt", response.json)
        # self.assertIn("total", response.json)
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("division", response.json)
        # self.assertIn("puc", response.json)
        #
        # refund_provider2 = response.json
        # # *********************UPDATE*************************
        # #  Realizo una copia del avance de tercero consultado
        # advance_copy = copy.deepcopy(refund_provider2)
        # # Cambio el total
        # advance_copy['total'] = 800000
        # # Envio a actulizar el avance de tercero
        # response = self.request_put(advance_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("message", response.json)
        # self.assertIn("error", response.json)
        # self.assertIn("status", response.json)
        #
        # # Espero un error por descuadre...
        # # FIXME: deberia establecer un error particular para este caso
        # self.assertEquals(response.status_code, 500)
        # self.assertIn("message", response.json)
        # # Establece el valor correcto al avance de tercero
        # advance_copy['total'] = 500000
        # # Realiza un cambio del comentario
        # advance_copy['comments'] = "Este es el test"
        # # Peticion de actualizado para este avance
        # response = self.request_put(advance_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("ok", response.json)
        #
        # # Copio el ultimo de los detalles de pago
        # payment_detail = advance_copy['paymentReceipt']['paymentDetails'][2]
        # # Elimino esta posicion del arreglo
        # del advance_copy['paymentReceipt']['paymentDetails'][2]
        # # Cambio el valor total del avance
        # advance_copy['total'] = 300000
        # # Actualiza el avance de tercero
        # response = self.request_put(advance_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("ok", response.json)
        #
        # # Simula un nuevo detalle de pago con base al eliminado
        # payment_detail.pop('paymentDetailId', None)
        # advance_copy['paymentReceipt']['paymentDetails'].append(payment_detail)
        # # Cambio el valor total del avance
        # advance_copy['total'] = 500000
        # advance_copy['comments'] = "Este es el test"
        # # Actualizo nuevamente
        # response = self.request_put(advance_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("ok", response.json)
        #
        # # Cambio el estado del documento
        # advance_copy['annuled'] = 1
        # # Envio a actualizar
        # response = self.request_put(advance_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("ok", response.json)
        #
        # # *********************DELETE*************************
        # # TODO ESTE METODO NO DEBERIA USARSE DESDE LA VISTA
        # # TODO SE AGREGA PARA MANTENER LA COHERENCIA DE LA BD Y EN PRUEBAS
        # response = self.request_delete("", "/" + str(self.id0))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta de eliminacion
        # self.assertIn("message", response.json)
        #
        # response = self.request_delete("", "/" + str(self.id0a))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta de eliminacion
        # self.assertIn("message", response.json)
        #
        # response = self.request_delete("", "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta de eliminacion
        # self.assertIn("message", response.json)
        #
        # response = self.request_delete("", "/" + str(self.id2))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta de eliminacion
        # self.assertIn("message", response.json)
        #
        # response = self.request_delete("", "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        #
        # self.assertEqual('ADVANCE THIRD NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')