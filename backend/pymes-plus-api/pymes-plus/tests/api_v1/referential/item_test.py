#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Auth module
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
import time
import logging
import copy


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for Item Test API class
"""
class ItemTest(unittest.TestCase):
    """
    This Class is a Test Case for Inventory Group API class
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



    # ############################### REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/items# with items data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/items'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/items# with items data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/items'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/items# with items data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/items'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/items# with items data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/items'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    # #####################################################################################


    def test_get_items(self):
        """
        This function test get all items
        ** First validate that contains the items key and content
        """
        response = self.request_get("")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("items" in response.json)
        self.assertIsNotNone(response.json['items'])

        # print("##"*10, response.json)


    def test_get_item(self):
        """
        This function test get a items according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # response = self.request_get("","/1658")
        # print( "ITEM"*1000, response.data )
        pass

    def test_get_item_by_company(self):
        """
        This function test get a items according to company identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        # api/v1/items/search?company_id=1&search=

        response = self.request_get('', '/search?company_id=1&search=')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Ok')
        self.assertIn('data', response.json)

        self.assertNotEqual(0, len(response.json['data']))
        # print(len(response.json['data']))

        self.assertIn("code", response.json['data'][0])
        self.assertIn("costPUC", response.json['data'][0])
        self.assertIn("incomingPUC", response.json['data'][0])
        self.assertIn("itemId", response.json['data'][0])
        self.assertIn("measurementUnit", response.json['data'][0])
        self.assertIn("name", response.json['data'][0])
        self.assertIn("typeItem", response.json['data'][0])

        # api/v1/items/search?company_id=1&search=COSMET
        response = self.request_get('', '/search?company_id=1&search=COSMET')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Ok')
        self.assertIn('data', response.json)

        self.assertNotEqual(0, len(response.json['data']))
        # print(len(response.json['data']))

        self.assertIn("code", response.json['data'][0])
        self.assertIn("costPUC", response.json['data'][0])
        self.assertIn("incomingPUC", response.json['data'][0])
        self.assertIn("itemId", response.json['data'][0])
        self.assertIn("measurementUnit", response.json['data'][0])
        self.assertIn("name", response.json['data'][0])
        self.assertIn("typeItem", response.json['data'][0])

        # api/v1/items/search?search=
        response = self.request_get('', '/search?search=')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Ok')
        self.assertIn('data', response.json)

        self.assertEquals(0, len(response.json['data']))

        # api/v1/items/search?code=ANI351
        response = self.request_get('', '/search?code=ANI351')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404, 'Ok')
        self.assertIn('error', response.json)
        self.assertEquals("Not Found".upper(), response.json['error'].upper())

        # api/v1/items/search?company_id=1&code=ANI351
        response = self.request_get('', '/search?company_id=1&code=ANI351')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Ok')
        self.assertNotIn('data', response.json)
        self.assertIn('code', response.json)
        self.assertEqual("ANI351", response.json['code'])

        self.assertIn("costPUC", response.json)
        self.assertIn("incomingPUC", response.json)
        self.assertIn("itemId", response.json)
        self.assertIn("measurementUnit", response.json)
        self.assertIn("name", response.json)
        self.assertIn("typeItem", response.json)

        # /api/v1/items/search?company_id=1&name=A COSMET SOBRE  x 10 GRM
        response = self.request_get('', '/search?company_id=1&name=A COSMET SOBRE  x 10 GRM')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Ok')
        self.assertIn('data', response.json)
        self.assertTrue("data" in response.json)
        self.assertIsNotNone(response.json['data'])
        response.json = response.json['data'][0]

        self.assertIn('code', response.json)
        # self.assertEqual("ANI351", response.json['code'])

        self.assertIn("costPUC", response.json)
        self.assertIn("incomingPUC", response.json)
        self.assertIn("itemId", response.json)
        self.assertIn("measurementUnit", response.json)
        self.assertIn("name", response.json)
        self.assertIn("typeItem", response.json)

        # /api/v1/items/search?company_id=1&name=A COSMET SOBRE  x 10 GRM
        response = self.request_get('', '/search?company_id=1&name=B_COSMET_SBR_10GRM')
        response.json = json.loads(response.data.decode('utf-8'))

        # self.assertEqual(response.status_code, 404, 'Ok')
        # self.assertIn('error', response.json)
        # self.assertEquals("Not Found".upper(), response.json['error'].upper())

    def test_post_put_get_delete_items(self):
        """
        Returns: I will create a item, get it and updated, and finally deleted.
        """

        data = {
            "subInventoryGroup3Id": 2, "incomingPUCId": 2520, "percentageICA": "1.00", "withholdingSalePercentage": 2.5,
            "priceListA5": 2900, "equivalentArt": "ANI351 A COSMET SOBRE  x 10 GRM", "disccountToUnitValue": True,
            "withholdingTaxPurchasePUCId": 85677, "conversionFactor2": 2.5,
            "incomingPUC": {
                "name": "VENTA DE QUIMICOS",
                "pucId": 2520,
                "account": "413550005 VENTA DE QUIMICOS", "percentage": 0
            },
            "reference": "102030", "description": "DESCRIPCIÓN 2", "name": "ITEM TEST",
            "inventoryPUC": {
                "name": "MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                "pucId": 84706,
                "account": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA", "percentage": 0
            },
            "priceListA1": 2500, "priceListA9": 3300, "priceList2": 1600, "withholdingTaxSalePUCId": 84519,
            "priceListB7": 4100, "costPUCId": 88508, "priceListB10": 4400, "priceListA4": 2800,
            "percentagePurchaseIVA": 16, "priceListB1": 3500, "discountPercentage": "10.00", "minimumStock": 100,
            "priceListA6": 3000, "weight": 10, "conversionFactor": 1.5, "color": False, "priceListB6": 4000,
            "priceListB9": 4300, "priceList5": 1900, "priceListB4": 3800,
            "consumptionPUC": {
                "name": "IMPUESTO AL CONSUMO 4%",
                "pucId": 85857,
                "account": "246205005 IMPUESTO AL CONSUMO 4%",
                "percentage": 4
            },
            "code": "0008",
            "ivaSalePUC": {
                "name": "IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%", "pucId": 85778,
                "account": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%", "percentage": 16
            },
            "measurementUnitId": 3, "priceListB5": 3900, "priceList3": 1700,
            "lastPurchaseDate": "2015-08-11T05:00:00.000Z",
            "saleIVAId": 2, "measurementUnit2Id": 30, "invimaRegister": "102030", "withholdingPurchasePercentage": 3.5,
            "subInventoryGroup1Id": 1,
            "ivaPurchasePUC": {
                "name": "IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES", "pucId": 85796,
                "account": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                "percentage": 16
            },
            "priceList7": 2100, "priceListA7": 3100, "plu": "102030", "packagePrice": "1500.0",
            "listItems": [
                {
                    "itemId": 220, "name": "A COSMET SOBRE  x 10 GRM", "code": "ANI351"
                },
                {
                    "itemId": 1436, "name": "PARAFINA ALEMANA COSMETICA KL", "code": "PRF008"
                }
            ],
            "withholdingICA": True, "priceListA3": 2700, "priceListB3": 3700, "lastCost": 0, "percentageSaleIVA": 16,
            "priceList6": 2000, "addConsumptionToCost": True, "priceList10": 2400,
            "withholdingTaxSalePUC": {
                "name": "RETENCION EN LA FUENTE - COBRADA AL 2.5%", "pucId": 84519,
                "account": "135515003 RETENCION EN LA FUENTE - COBRADA AL 2.5%",
                "percentage": 2.5
            },
            "priceListA8": 3200, "size": False, "priceListB2": 3600, "state": "A", "purchaseIVAId": 2,
            "costPUC": {
                "name": "VENTA DE QUIMICOS", "pucId": 88508, "account": "613550005 VENTA DE QUIMICOS",
                "percentage": 0
            },
            "ivaSalePUCId": 85778, "priceList9": 2300, "inventoryGroupId": 2, "namePOS": "ITEM TEST",
            "averageCost": 0, "orderQuantity": 100, "addConsumptionToPurchase": True, "priceList4": 1800,
            "serial": False,
            "logosConverter": [
                {
                    "favorite": True,
                    "logoConvert": "data:image/jpeg;base64,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"
                },
                {
                    "logoConvert": ""
                },
                {}, {}, {}, {}, {}, {}, {}, {}, {}
            ],
            "brandId": 7, "companyCost": 1500, "priceList1": 1500, "addIVAtoCost": True,
            "ivaPurchasePUCId": 85796, "subInventoryGroup2Id": 1, "priceListA2": 2600, "priceListA10": 3400,
            "measurementUnit3Id": 45, "barCode": "102030", "typeItem": "A", "inventoryPUCId": 84706,
            "lot": True, "priceList8": 2200, "itemsList": [220, 1436],
            "withholdingTaxPurchasePUC": {
                "name": "COMPRAS 3.5%", "pucId": 85677, "account": "236540005 COMPRAS 3.5%",
                "percentage": 3.5
            },
            "consumptionPercentage": 4, "priceListB8": 4200, "companyId": 1,
            "invimaDueDate": "2016-08-31T05:00:00.000Z", "consumptionPUCId": 85857
        }

        # *********************** POST *************************
        # Test Normal Save
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200, 'Error try to save')
        self.assertIn('itemId', response.json)

        # Assign the Id for the rest of the TESTs
        self.itemId = response.json['itemId']

        # Test Send Save Again
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 400, 'Item code already exist')

        data['itemId'] = self.itemId
        # Test Normal Save with Exist ID
        response = self.request_post(data, '/')
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'Error try to save')
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'El item ya existe')

        # ********************* GET **************************

        response = self.request_get('', '/' + str(self.itemId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertTrue("code" in response.json)
        self.assertEqual(data['code'], response.json['code'])
        # ********************* PUT **************************

        data_diferent_id_request = copy.deepcopy(response.json)
        data_id_dont_exist = copy.deepcopy(response.json)
        data_normal_update = copy.deepcopy(response.json)

        # Update data_diferent_id_request with diferent Id
        response = self.request_put(data_diferent_id_request, '/' + str(123123123))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400, 'Item Id Dont Match')
        self.assertIn("message", response.json)
        self.assertEqual(response.json['message'], 'Bad Request')

        # Update ID who dont Exist
        data_id_dont_exist['itemId'] = 123123123
        response = self.request_put(data_id_dont_exist, '/' + str(123123123))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404, 'Item Id Dont exist')
        self.assertIn("message", response.json)
        self.assertEqual(response.json['message'], 'Not Found')

        # Update data_normal_update for a correct Update
        data_normal_update['name'] = 'item test'
        response = self.request_put(data_normal_update, '/' + str(data_normal_update['itemId']))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("ok", response.json)
        self.assertEqual(response.json['ok'], 'ok')

        # ********************* DELETE  **********************

        response = self.request_delete('', '/' + str(self.itemId))
        response.json = json.loads(response.data.decode('utf-8'))

        self.assertIn("message", response.json)
        self.assertEqual(response.json['message'].upper(), 'Eliminado correctamente'.upper())

        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 500)

        # Test with invalid id
        response = self.request_delete('', '/')
        self.assertEquals(response.status_code, 405)



