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
import uuid

from app import create_app
from app.api_v1 import api

import copy

"""
This module shows various methods and function by allow
handled purchase_order
"""
class PurchaseOrdersTest(unittest.TestCase):
    """
    This Class is a  Test Case for purchase_order API class
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
        """Sent get request to #/api/v1/purchase_order# with purchase_order data values

        :param data: purchase_order data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/purchase_orders' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/purchase_order# with purchase_order data values

        :param data: purchase_order data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/purchase_orders' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/purchase_order# with purchase_order data values

        :param data: purchase_order data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/purchase_orders' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/purchase_order# with purchase_order data values

        :param data: purchase_order data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/purchase_orders' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_purchase_orders(self):
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

    def test_get_purchase_order_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=OP")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.test_client.get('/api/v1/document_headers/search?branchId=14&startDate=2017-03-01&limitDate='
                                        '2017-03-31&documentNumber=null&controlNumber=null&'
                                        'search=null&filterBy=null&initTotal=null&endTotal=null&shortWord=OP',
                             data=json.dumps(''),
                             content_type='application/json', headers=self.headers)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        purchase_order = response.json['data'][0]

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' +
                                    purchase_order['documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 500)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=OP&document_number=' +
                                    purchase_order['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("total", response.json)
        self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {'error': 'bad request', 'message': 'Invalid params', 'status': 400})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(purchase_order['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)
        self.assertIn("total", response.json)

    ##################################################################################
    def test_post_put_delete(self):
        """
        This function allow create, update and delete a purchase item
         ** First test create with bad branch data
         ** Second test create with correct branch data
         ** Third test update branch
         ** Fourth test delete branch
        """
        purchase_order = {'orderNumber': None, 'shipAddress': 'CR 13 A 12 47', 'revolvingFund': None, 'termDays': 1, 'checks': None, 'workNumber': None, 'retentionPUCId': None, 'cutNumber': None, 'reteICAPUCId': None, 'kitId': None, 'subtotal': 500000, 'dateFrom': None, 'consumptionTaxBase': None, 'deductibleRF': None, 'createdBy': None, 'initialQuota': None, 'globalTax': None, 'freezeBill': None, 'initialDate': None, 'employeeId': None, 'bonus': None, 'assumedIVA': None, 'sourceDocumentHeaderId': None, 'thirdId': None, 'payrollBasicId': None, 'fspValue': None, 'costCenterId': 4, 'withholdingTaxBase': None, 'disccount': 0, 'disccount2Mode': None, 'isDeleted': None, 'retirement': None, 'depositNumber': None, 'requisitionNumber': None, 'daysPILA': None, 'documentDate': '2017-04-03T08:28:53.000Z', 'documentNumber': '0000001214', 'auxNumberTwo': None, 'freightPUCId': None, 'isChangeNoted': None, 'disccount2TaxBase': None, 'updateBy': None, 'addToPayroll': None, 'prefix': None, 'withholdingTaxValue': 17500, 'finalDate': None, 'withholdingTaxPUCId': None, 'retentionMode': None, 'disccountPercent': None, 'shipCity': 'BOGOTA', 'auxTimeOne': None, 'divisionId': 13, 'overCost': 0, 'realSimulated': None, 'payrollPaymentType': None, 'importId': None, 'reteIVAValue': None, 'state': True, 'inability': None, 'partnerId': None, 'exchangeRate': 1, 'pettyCash': None, 'withholdingTaxPercent': None, 'retentionPercent': 0, 'reteICAValue': None, 'productionOrderId': None, 'overCostTaxBase': None, 'bonusDateFrom': None, 'retentionValue': 0, 'stageCostTotal': None, 'customerId': None, 'typeThirdParty': None, 'reteIVAPercent': None, 'consumptionTaxPUCId': None, 'cashierId': None, 'disccount2': 0, 'productionUnits': None, 'accounted': None, 'sourceDocument': None, 'dependencyId': None, 'periodicityQuota': None, 'reteIVAPUCId': None, 'baseCREE': 0, 'typeAccount': None, 'sourcePrefix': None, 'paymentBy': None, 'shortWord': 'OP', 'accountsBackward': None, 'disccount2Value': 0, 'daysNet': None, 'leadDocumentTo': None, 'shipZipCode': '', 'sodicon': None, 'importReplaced': None, 'destinyBranchId': None, 'daysEnjoy': None, 'auxNumberOne': None, 'month': None, 'bankAccountId': None, 'annuled': None, 'ivaPUCId': None, 'epsValue': None, 'closingType': None, 'vacationDateFrom': None, 'financialEntityId': None, 'total': 562500, 'auxTimeTwo': None, 'comments': 'ESTO ES UNA PRUEBA', 'adjustment': None, 'isConsignment': None, 'afpValue': None, 'updateDate': None, 'currencyId': 4, 'documentAffecting': [], 'reteICABase': None, 'balance': 0, 'withholdingCREEPUCId': None, 'paymentTermId': None, 'ivaPercent': None, 'comissionPercent': None, 'daysWorked': None, 'destinyWarehouseId': None, 'assetId': None, 'importationValue': None, 'sectionId': 7, 'documentTypeConsign': None, 'payrollEntityId': None, 'auxCharacterOne': None, 'shipTo': 'LEGAQUIMICOS SAS modificada', 'dateTo': None, 'provider': {'providerId': 532, 'name': ' PENA TORRES JEFFERSON AMADO (56403) - ASESORES JPT', 'branch': '789', 'thirdPartyId': 2394, 'isWithholdingCREE': 0}, 'interest': None, 'year': None, 'cash': None, 'consumptionTaxValue': 0, 'reteICAPercent': None, 'sourceWarehouseId': None, 'comission': None, 'ivaValue': 80000, 'shipCountry': 'COLOMBIA', 'otherThirdId': None, 'payrollType': None, 'firtsContractDate': None, 'quotaNumbers': None, 'contractId': None, 'sourceShortWord': 'OP', 'percentageCREE': None, 'advanceLayoff': None, 'printed': None, 'prefixRequisitionNumber': None, 'shipPhone': '2860084', 'billingResolutionId': None, 'interestPUCId': None, 'expenses': None, 'creationDate': None, 'overTax': None, 'daysVacation': None, 'payment': None, 'shipDepartment': 'D.C.', 'directIVA': None, 'sourceDocumentTypeId': None, 'costCenter': {'updateDate': 'Fri, 23 Aug 2013 11:37:13 GMT', 'branchId': 14, 'name': 'LEGAQUIMICOS', 'costCenterId': 4, 'updateBy': 'Administrador del Sistema', 'createdBy': 'DENNY ORJUELA', 'divisions': [{'updateDate': 'Fri, 24 Mar 2017 09:45:20 GMT', 'costCenterId': 4, 'createdBy': 'DENNY ORJUELA', 'isDeleted': 0, 'code': '00001', 'sections': [{'updateDate': 'Fri, 18 Sep 2015 14:44:05 GMT', 'sectionId': 7, 'pucId': None, 'createdBy': 'ADMINISTRADOR', 'code': '00043', 'isDeleted': 0, 'dependencies': [], 'name': 'F', 'divisionId': 13, 'puc': None, 'updateBy': 'ADMINISTRADOR', 'expenses': None, 'creationDate': 'Fri, 18 Sep 2015 14:44:05 GMT'}], 'name': 'ADMINISTRACION', 'divisionId': 13, 'puc': {'name': 'GASTOS - OPERACIONALES DE ADMINISTRACION', 'pucAccount': '510000000', 'percentage': 0, 'account': '510000000 GASTOS - OPERACIONALES DE ADMINISTRACION', 'pucId': 87304}, 'updateBy': 'ADMINISTRADOR UPDATE del Sistema', 'expenses': 'Cuenta 51', 'creationDate': 'Wed, 14 Aug 2013 10:42:14 GMT', 'pucId': 87304}, {'updateDate': 'Tue, 21 Mar 2017 14:34:12 GMT', 'costCenterId': 4, 'createdBy': 'Administrador del Sistema', 'isDeleted': 0, 'code': '00002', 'sections': [], 'name': 'VENTAS', 'divisionId': 14, 'puc': {'name': 'COSTOS DE PRODUCCIÓN - CONTRATOS DE SERVICIOS', 'pucAccount': '740000000', 'percentage': 0, 'account': '740000000 COSTOS DE PRODUCCIÓN - CONTRATOS DE SERVICIOS', 'pucId': 5365}, 'updateBy': 'ADMINISTRADOR UPDATE del Sistema', 'expenses': 'Cuenta 74', 'creationDate': 'Fri, 23 Aug 2013 11:39:40 GMT', 'pucId': 5365}], 'code': '00001', 'creationDate': 'Wed, 14 Aug 2013 10:41:52 GMT', 'isDeleted': 0}, 'branchId': 14, 'directIVAPercent': None, 'controlPrefix': None, 'daysLicensed': None, 'insurance': None, 'sanction': None, 'documentHeaderId': None, 'auxCharacterTwo': None, 'sourceId': None, 'pucId': None, 'consumptionTaxPercent': None, 'insurancePUCId': None, 'valueCREE': 0, 'documentTypeId': None, 'baseSalary': None, 'vacation': None, 'ivaBase': None, 'reteIVABase': None, 'tipValue': None, 'providerId': 532, 'documentDetails': [{'sectionId': 7, 'costCenterId': 4, 'detailWarehouse': {'name': 'LEGAQUIMICOS MODIFICAD', 'warehouseId': 6, 'codeComplete': 'Código 002', 'typeWarehouse': 'S', 'code': '002'}, 'ivaPUCId': 85796, 'consumptionTaxPercent': 0, 'measurementUnitId': 34, 'disccount': 0, 'badgeValue': 4249.94, 'color': False, 'size': False, 'conversionFactor': 1, 'divisionId': 13, 'quantity': '5.00', 'value': 500000, 'withholdingTaxPUCId': 85677, 'withholdingTaxPUC': {'pucAccount': '236540005 COMPRAS 3.5%', 'pucId': 85677, 'percentage': 3.5}, 'consumptionTaxValue': 0, 'itemToCompare': {'percentagePurchaseIVA': 16, 'reference': '', 'inventoryPUC': {'pucAccount': '143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA', 'pucId': 84706, 'percentage': 0}, 'inventoryPUCId': 84706, 'ivaSalePUCId': 85778, 'consumptionPercentage': 0, 'size': False, 'priceListB7': None, 'incomingPUC': {'pucAccount': '413550005 VENTA DE QUIMICOS', 'pucId': 86636, 'percentage': 0}, 'conversionFactor': 0, 'lastPurchaseDate': 'Wed, 27 May 2015 00:00:00 GMT', 'priceListA10': 0, 'priceListB8': None, 'updateDate': 'Wed, 18 Dec 2013 16:21:50 GMT', 'addConsumptionToCost': False, 'subInventoryGroup1Id': None, 'typeItem': 'A', 'consumptionPUC': None, 'companyId': 1, 'purchaseIVAId': 2, 'ivaPurchasePUCId': 85796, 'withholdingTaxPurchasePUCId': 85677, 'priceListA7': 0, 'packagePrice': 0, 'withholdingTaxSalePUCId': 84520, 'priceListB10': None, 'costPUCId': 88508, 'subInventoryGroup3': None, 'inventoryGroup': {'inventoryGroupId': 9, 'name': 'COSMETICOS'}, 'averageCost': 4249.94, 'withholdingSalePercentage': 0, 'isDeleted': False, 'subInventoryGroup3Id': None, 'description': '', 'priceList4': 0, 'percentageSaleIVA': 16, 'priceListA8': 0, 'priceListB1': None, 'disccountToUnitValue': False, 'subInventoryGroup2Id': None, 'code': 'AC005', 'priceListB2': None, 'ivaPurchasePUC': {'pucAccount': '240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES', 'pucId': 85796, 'percentage': 16}, 'priceListA1': 0, 'namePOS': 'ACEITES AYB X 250 ML', 'measurementUnit3Id': None, 'updateBy': 'Migracion', 'saleIVA': {'ivaId': 2, 'name': 'GRAVADO', 'code': 'G'}, 'invimaDueDate': None, 'measurementUnit2': None, 'priceListA6': 0, 'brandId': None, 'plu': '', 'priceList6': 0, 'subInventoryGroups1': None, 'priceList5': 0, 'priceList8': None, 'measurementUnitId': 34, 'invimaRegister': None, 'measurementUnit2Id': None, 'minimumStock': 0, 'priceListA9': 0, 'withholdingICA': False, 'withholdingPurchasePercentage': 3.5, 'priceList1': 6034.48, 'orderQuantity': 0, 'priceListB9': None, 'creationDate': 'Tue, 10 Dec 2013 14:40:28 GMT', 'subInventoryGroup2': None, 'priceList7': None, 'itemId': 27, 'withholdingTaxSalePUC': {'pucAccount': '135515005 RETENCION EN LA FUENTE - EXENTA', 'pucId': 84520, 'percentage': 0}, 'saleIVAId': 2, 'itemDetails': [], 'priceList10': None, 'discountPercentage': 0, 'name': 'ACEITES AYB X 250 ML', 'lastCost': 4250, 'weight': 0, 'addIVAtoCost': False, 'priceListA3': 0, 'barCode': '', 'percentageICA': 11.04, 'imageId': None, 'costPUC': {'pucAccount': '613550005 VENTA DE QUIMICOS', 'pucId': 88508, 'percentage': 0}, 'consumptionPUCId': None, 'measurementUnit': {'name': 'MEDIA LIBRA                   ', 'measurementUnitId': 34, 'code': 'MDL'}, 'incomingPUCId': 86636, 'state': 'A', 'photo': None, 'priceListA2': 0, 'priceList9': None, 'priceList3': 0, 'priceListA4': 0, 'color': False, 'priceListB3': None, 'inventoryGroupId': 9, 'priceList2': 0, 'priceListB6': None, 'withholdingTaxPurchasePUC': {'pucAccount': '236540005 COMPRAS 3.5%', 'pucId': 85677, 'percentage': 3.5}, 'lot': False, 'priceListB4': None, 'conversionFactor2': None, 'priceListA5': 0, 'priceListB5': None, 'companyCost': 4641.91, 'createdBy': 'Migracion', 'providerId': None, 'listItems': [], 'ivaSalePUC': {'pucAccount': '240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%', 'pucId': 85778, 'percentage': 16}, 'purchaseIVA': {'ivaId': 2, 'name': 'GRAVADO', 'code': 'G'}, 'addConsumptionToPurchase': False, 'serial': False, 'measurementUnit3': None}, 'dependencyId': None, 'consumptionTaxBase': 500000, 'itemId': 27, 'indexItem': 0, 'units': '5.00', 'code': 'AC005', 'und': {'name': 'MEDIA LIBRA                   ', 'measurementUnitId': 34, 'code': 'MDL'}, 'iva': 16, 'detailWarehouseId': 6, 'balance': '5.00', 'measurementUnits': [{'name': 'MEDIA LIBRA                   ', 'measurementUnitId': 34, 'code': 'MDL'}], 'ivaPurchasePUC': {'pucAccount': '240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES', 'pucId': 85796, 'percentage': 16}, 'withholdingTax': 3.5, 'name': 'ACEITES AYB X 250 ML', 'baseValue': 500000, 'detailDate': '2017-04-03T08:28:53.000Z', 'unitValue': '100000.00', 'otr': '', 'consultItem': True}], 'semester': None, 'businessAgentId': None, 'stageId': None, 'baseType': None, 'controlNumber': None, 'retentionBase': None, 'cashRegisterId': None, 'freight': None, 'layoffValue': None}

        # Envio la creacion del avance sin short word
        purchase_order["shortWord"] = None
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Envio la creacion del avance con short word erroneo
        purchase_order["shortWord"] = "XY"
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        purchase_order["shortWord"] = "OP"
        # Crea un compra de item con un peso de diferencia en el credit
        purchase_order['documentDetails'][0]['value'] = 500000.01
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        purchase_order['documentDetails'][0]['value'] = 500000
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        purchase_order['documentDetails'][0]['value'] = 500000
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = purchase_order['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                      "currencyId": 2,
                      "isDeleted": 0,
                      "name": "DÓLAR AMERICANO",
                      "symbol": "$"}

        purchase_order["currency"] = currency2
        purchase_order["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(purchase_order)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        purchase_order["currency"] = currency
        purchase_order["currencyId"] = 4

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

        purchase_order2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(purchase_order2)
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
        purchase_copy['documentDetails'][0]['value'] = 500000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 500000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # Cambio el valor total del avance
        purchase_copy['documentDetails'][0]['value'] = 500000
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