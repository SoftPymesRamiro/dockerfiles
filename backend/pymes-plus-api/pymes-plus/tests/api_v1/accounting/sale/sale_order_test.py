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
handled sales_orders
"""
class SalesOrdersTest(unittest.TestCase):
    """
    This Class is a  Test Case for sales_orders API class
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
        """Sent get request to #/api/v1/sales_orders# with sales_orders data values

        :param data: sales_orders data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/sales_orders' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/sales_orders# with sales_orders data values

        :param data: sales_orders data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/sales_orders' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/sales_orders# with sales_orders data values

        :param data: sales_orders data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/sales_orders' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/sales_orders# with sales_orders data values

        :param data: sales_orders data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/sales_orders' + path,
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

    def test_get_sales_orders_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=PE")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&document_number=0000000019&short_word=PE')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        sales_orders = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&document_number='+sales_orders['documentNumber']+'&short_word=PE')

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&document_number='+sales_orders['documentNumber']+'&short_word=PE')
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("shipTo", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {'error': 'bad request', 'status': 400, 'message': 'Invalid params'})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(sales_orders['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("shipTo", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(sales_orders['documentHeaderId']) + "/preview?format=P")
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
        sales_orders = {'disccount2Value': 0, 'reteICAPercent': '3.00', 'currencyId': 4, 'documentNumber': '0000000019', 'disccount2TaxBase': 0, 'reteIVAPercent': '3.00', 'documentDate': '2017-05-02T09:16:05.000Z', 'termDays': '1', 'documentDetails': [{'balance': '100.00', 'consumptionTaxBase': 539614.46, 'itemId': 1850, 'sectionId': 7, 'name': 'NORMAL', 'baseValue': 539614.46, 'ivaPurchasePUC': {'pucId': 85796, 'percentage': 16, 'pucAccount': '240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES'}, 'withholdingTax': 3.5, 'dueDate': None, 'withholdingTaxPUC': {'pucId': 85677, 'percentage': 3.5, 'pucAccount': '236540005 COMPRAS 3.5%'}, 'measurementUnits': [{'code': 'CAJ', 'name': 'CAJAS                         ', 'measurementUnitId': 42}, {'code': 'UNI', 'name': 'UNIDADES                      ', 'measurementUnitId': 36}], 'disccount': '2.00', 'size': False, 'itemToCompare': {'minimumStock': 0, 'priceListB4': 0, 'updateDate': 'Thu, 02 Feb 2017 15:14:10 GMT', 'itemId': 1850, 'ivaPurchasePUC': {'pucId': 85796, 'percentage': 16, 'pucAccount': '240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES'}, 'inventoryGroup': None, 'priceListA10': 0, 'measurementUnit': {'code': 'CAJ', 'name': 'CAJAS                         ', 'measurementUnitId': 42}, 'packagePrice': 0, 'photo': None, 'discountPercentage': 0, 'reference': None, 'conversionFactor2': 0, 'priceListB6': 0, 'subInventoryGroup2': None, 'lot': False, 'consumptionPercentage': 0, 'lastCost': 0, 'code': 'NORMAL', 'priceList2': 0, 'weight': 0, 'priceList9': 0, 'priceList7': 0, 'measurementUnit2Id': 36, 'ivaSalePUCId': 85778, 'brandId': None, 'listItems': [], 'inventoryPUC': {'pucId': 84706, 'percentage': 0, 'pucAccount': '143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA'}, 'addIVAtoCost': False, 'incomingPUC': {'pucId': 2520, 'percentage': 0, 'pucAccount': '413550005 VENTA DE QUIMICOS'}, 'saleIVA': {'code': 'G', 'name': 'GRAVADO', 'ivaId': 2}, 'measurementUnit3Id': None, 'withholdingPurchasePercentage': 3.5, 'priceListB7': 0, 'withholdingTaxSalePUC': {'pucId': 84521, 'percentage': 3.5, 'pucAccount': '135515010 RETENCION EN LA FUENTE - COBRADA AL 3.5%'}, 'plu': None, 'consumptionPUC': None, 'consumptionPUCId': None, 'companyId': 1, 'incomingPUCId': 2520, 'priceList6': 0, 'priceList3': 0, 'description': None, 'color': False, 'providerId': None, 'subInventoryGroup3': None, 'addConsumptionToCost': False, 'priceList4': 0, 'priceListB3': 0, 'conversionFactor': 10, 'percentageSaleIVA': 16, 'state': 'A', 'createdBy': 'ADMINISTRADOR UPDATE del Sistema', 'inventoryGroupId': None, 'withholdingICA': True, 'priceListA6': 0, 'subInventoryGroup1Id': None, 'imageId': None, 'invimaRegister': None, 'ivaPurchasePUCId': 85796, 'priceListA7': 0, 'priceListA2': 0, 'purchaseIVA': {'code': 'G', 'name': 'GRAVADO', 'ivaId': 2}, 'priceListB1': 0, 'ivaSalePUC': {'pucId': 85778, 'percentage': 16, 'pucAccount': '240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%'}, 'withholdingTaxPurchasePUCId': 85677, 'averageCost': 0, 'saleIVAId': 2, 'orderQuantity': 0, 'isDeleted': False, 'withholdingTaxSalePUCId': 84521, 'lastPurchaseDate': 'Thu, 02 Feb 2017 09:45:21 GMT', 'priceListB10': 0, 'itemDetails': [], 'disccountToUnitValue': False, 'priceListA4': 0, 'priceListB9': 0, 'measurementUnitId': 42, 'priceListB8': 0, 'priceListA8': 0, 'addConsumptionToPurchase': False, 'priceListA9': 0, 'costPUCId': 88508, 'measurementUnit2': {'code': 'UNI', 'name': 'UNIDADES                      ', 'measurementUnitId': 36}, 'barCode': None, 'withholdingSalePercentage': 0, 'costPUC': {'pucId': 88508, 'percentage': 0, 'pucAccount': '613550005 VENTA DE QUIMICOS'}, 'name': 'NORMAL', 'invimaDueDate': 'Thu, 02 Feb 2017 09:45:21 GMT', 'priceListB2': 0, 'measurementUnit3': None, 'withholdingTaxPurchasePUC': {'pucId': 85677, 'percentage': 3.5, 'pucAccount': '236540005 COMPRAS 3.5%'}, 'creationDate': 'Thu, 02 Feb 2017 15:14:10 GMT', 'updateBy': 'ADMINISTRADOR UPDATE del Sistema', 'subInventoryGroup3Id': None, 'size': False, 'serial': False, 'priceListA1': 600, 'priceList1': 5000, 'inventoryPUCId': 84706, 'percentagePurchaseIVA': 16, 'subInventoryGroup2Id': None, 'priceListA3': 0, 'priceListB5': 0, 'purchaseIVAId': 2, 'priceListA5': 0, 'priceList10': 0, 'companyCost': 1000, 'namePOS': 'NORMAL', 'priceList5': 0, 'subInventoryGroups1': None, 'typeItem': 'A', 'percentageICA': 5, 'priceList8': 0}, 'otr': '', 'iva': 16, 'withholdingICA': True, 'indexItem': 0, 'consumptionTaxValue': 0, 'units': '100.00', 'detailDate': '2017-05-02T09:16:05.000Z', 'color': False, 'withholdingTaxPUCId': 85677, 'detailWarehouse': {'code': '002', 'warehouseId': 6, 'typeWarehouse': 'S', 'name': 'LEGAQUIMICOS MODIFICAD', 'codeComplete': 'Código 002'}, 'consumptionTaxPercent': 0, 'code': 'NORMAL', 'unitValue': '5506.27', 'badgeValue': 1000, 'costCenterId': 4, 'ivaPUCId': 85796, 'consultItem': True, 'und': {'code': 'CAJ', 'name': 'CAJAS                         ', 'measurementUnitId': 42}, 'divisionId': 13, 'measurementUnitId': 42, 'value': 550627, 'quantity': '100.00', 'conversionFactor': 1, 'dependencyId': None, 'detailWarehouseId': 6}], 'controlPrefix': None, 'exchangeRate': 1, 'reteICABase': 0, 'controlNumber': None, 'disccount2Mode': False, 'consumptionTaxValue': 0, 'subtotal': 550627, 'baseCREE': 0, 'documentAffecting': [], 'dateTo': '2017-05-03T09:16:05.000Z', 'customerId': 1999, 'disccount2': 0, 'dependencyId': None, 'costCenter': None, 'customer': {'customerId': 1999, 'name': ' PEÑA TORRES AMADO (1234567891) - PEÑA', 'branch': '787'}, 'shipCountry': ' COLOMBIA', 'sourceShortWord': 'PE', 'divisionId': 13, 'sourceDocumentOrigin': 'PE', 'sectionId': 7, 'selectedSalesMan': {'name': ' PEÑA TORRES AMADO (1234567891) - PEÑA(AC)', 'type': 'BusinessAgent', 'id': 199}, 'shipZipCode': None, 'retentionPercent': 0, 'branchId': 14, 'reteIVABase': 86338.31, 'thirdId': None, 'paymentTermId': 2, 'annuled': None, 'shipTo': ' PEÑA TORRES AMADO', 'shipDepartment': ' VALLE DEL CAUCA ', 'percentageCREE': 0.3, 'comments': None, 'disccount': 11012.54, 'shipCity': 'CALI ', 'shortWord': 'PE', 'paymentReceipt': {}, 'payment': 601205.39, 'reteIVAValue': 2590.15, 'shipPhone': None, 'overCost': 0, 'retentionValue': 0, 'reteICAValue': 1618.84, 'applyCree': True, 'costCenterId': 4, 'overCostTaxBase': 0, 'withholdingTaxValue': 18886.51, 'valueCREE': 1651.88, 'shipAddress': 'CRA 34 # 121- 223', 'ivaValue': 86338.31, 'sourceDocumentHeaderId': None, 'retentionPUCId': None, 'total': 601205.39}
        # Envio la creacion del avance sin short word
        sales_orders["shortWord"] = None
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        sales_orders["shortWord"] = "XY"
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        sales_orders["shortWord"] = "PE"
        # Crea un compra de item con un peso de diferencia en el credit
        sales_orders['documentDetails'][0]['value'] = 550627.20
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        sales_orders['documentDetails'][0]['value'] = 550627.18
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        sales_orders['documentDetails'][0]['value'] = 550627.18
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        # currency = sales_orders['currency']
        # # FIXME: podria consultar las monedas y obtener una
        # # Establece una moneda distinta
        # currency2 = {"code": "USD",
        #               "currencyId": 2,
        #               "isDeleted": 0,
        #               "name": "DÓLAR AMERICANO",
        #               "symbol": "$"}
        #
        # sales_orders["currency"] = currency2
        # sales_orders["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(sales_orders)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        # sales_orders["currency"] = currency
        # sales_orders["currencyId"] = 4

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=PE&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("documentAffecting", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("withholdingTaxValue", response.json)
        self.assertIn("sourceDocumentHeaderId", response.json)

        sales_orders2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(sales_orders2)
        # Cambio el total
        purchase_copy['documentDetails'][0]['value'] = 0
        # Envio a actulizar el compra de item
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        # self.assertIn("message", response.json)
        # self.assertIn("error", response.json)
        self.assertIn("ok", response.json)

        # Espero un error por descuadre...
        # FIXME: deberia establecer un error particular para este caso
        self.assertEquals(response.status_code, 201)
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

        self.assertEqual('SALE ORDER NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')