#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Purchase remissions
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David Trochez"]
__version__ = "1.0.1"

import unittest
from flask import Flask
import unittest
import json
from app import create_app
from app.api_v1 import api
from functools import reduce

class PurchaseRemissionsTest(unittest.TestCase):
    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
                             password='Admin*2')  # valid data by access to SoftPymes plus

        app = Flask(__name__)  # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self)  # test client
        self.test_client.testing = False  # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                                              data=json.dumps(self.userdata),
                                              content_type='application/json')
        # User token
        self.token = json.loads(self.response.data.decode("utf-8"))['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    # ############################### REQUEST FUNCTIONS ##################################
    def request_get(self, data, path="/"):
        """Sent get request to #/api/v1/purchase_remissions# with purchase_remissions data values

        :param data: purchase_remissions data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/purchase_remissions' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/purchase_remissions# with purchase_remissions data values

        :param data: purchase_remissions data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/purchase_remissions' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/purchase_remissions# with purchase_remissions data values

        :param data: purchase_remissions data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/purchase_remissions' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/purchase_remissions# with purchase_remissions data values

        :param data: purchase_remissions data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/purchase_remissions' + path, headers=self.headers)  # envio el request

    # ############################### REQUEST FUNCTIONS ##################################
    def request_get_accounting(self, path="/"):
        """Sent get request to #/api/v1/accounting_records#
        :param path: specific path
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/accounting_records' + path,
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_get_other(self, path="/"):
        """Sent get request to #/api/v1/whatever#
        :param path: specific path
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1' + path,
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete_other(self, data, path="/"):
        """Sent delete request to #/api/v1/whatever#

        :param data: resource's id
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1' + path, headers=self.headers)  # envio el request

    def request_post_other(self, data, path="/"):
        """Sent post request to #/api/v1/whatever# with whatever data values

        :param data: whatever data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request
    ######################################################################################

    def test_post_purchase_remission(self):
        """
        This function test to save a purchase remission according to json data
        """
        data = {
          "shortWord": "RP",
          "anNoneed": False,
          "dayClosed": False,
          "termDays": 0,
          "subtotal": 10,
          "disccount": 0,
          "ivaValue": 0.2,
          "withholdingTaxValue": 0.3,
          "consumptionTaxValue": 0,
          "disccount2Value": 0,
          "disccount2": 0,
          "baseCREE": 0,
          "valueCREE": 0,
          "total": 9.899999999999999,
          "documentDetails": [
            {
              "code": "1993",
              "name": "PYTHON3",
              "units": "1",
              "otr": "",
              "unitValue": 10,
              "quantity": 2,
              "disccount": 0,
              "iva": 1.6,
              "withholdingTax": 3.5,
              "badgeValue": 10,
              "value": 10,
              "detailDate": "2016-08-06T08:58:21.000Z",
              "consultItem": True,
              "itemId": 1660,
              "size": False,
              "color": False,
              "consumptionTaxPercent": 0,
              "measurementUnitId": 1,
              "conversionFactor": 1,
              "costCenterId": 7,
              "divisionId": 2,
              "sectionId": 3,
              "dependencyId": 6,
              "baseValue": 10,
              "consumptionTaxBase": 10,
              "consumptionTaxValue": 0,
              "detailWarehouseId": 5,
              "ivaPUCId": 85801,
              "withholdingTaxPUCId": 85677,
              "listSerials": ["serial1", "serial2"]
            }
          ],
          "documentDate": "2016-08-06T08:58:21.000Z",
          "documentNumber": "0000000007",
          "shipTo": "LEGAQUIMICOS SAS modificada",
          "shipAddress": "CR 13 A 12 47",
          "shipCity": "BOGOTA",
          "shipZipCode": "",
          "shipDepartment": "D.C.",
          "shipPhone": "2860084",
          "shipCountry": "COLOMBIA",
          "currencyId": 4,
          "costCenterId": 7,
          "divisionId": 2,
          "sectionId": 3,
          "dependencyId": 6,
          "exchangeRate": 1,
          "sourceDocumentOrigin": "1",
          "paymentBy": "1",
          "providerId": 1,
          "branchId": 14
        }

        # ******************* POST **************************
        # Test save normal
        response = self.request_post(data, '/?short_word=RP&source_short_word=RP')
        response.json = json.loads(response.data.decode("utf-8"))
        # Asignacion de id para hacer los demas tests
        self.documentHeaderId = response.json['id']
        self.assertTrue('documentNumber' in response.json['data'], 'Failed assign the consecutive')
        self.assertNotEqual(response.json['id'], 0, 'Invalid assign id')

        # Test with invalid short word
        response = self.request_post(data, '/?short_word=XXX&source_short_word=RP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertTrue('message' in response.json)
        self.assertEquals(response.json['message'], 'Invalid short word', 'Shouldn`t save')
        self.assertEquals(response.status_code, 400, 'Shouldn`t save')

        # Test without document details
        del data['documentDetails']
        response = self.request_post(data, '/?short_word=RP&source_short_word=RP')
        self.assertEquals(response.status_code, 400, 'Shouldn`t save')

        # ******************* GET **************************
        """
            This function test get a PurchaseRemissions according to identifier
             ** First test is correct identifier
             ** Second test is incorrect identifier
        """
        response = self.request_get('', '/'+str(self.documentHeaderId))  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        # validacion de la clave en la respuesta
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')
        # Valida que venga con la lista de seriales
        self.assertIn('listSerials', response.json["documentDetails"][0], 'property named listSerials not found')
        self.assertTrue(
            float(len(response.json['documentDetails'][0]['listSerials'])) == response.json['documentDetails'][0]['quantity'],
            'quantity don`t match with length of serial list'
        )

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

        """
            This function test get a purchase remission according to search pattern
             ** First test is incorrect args
             ** Second test is correct args and data exist
             ** Third test is with incorrect short word
             ** Four test is without last consecutive and data exist
            """
        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 400, 'incorrect response by correct request')
        self.assertTrue('message' in response.json)
        self.assertEquals(response.json['message'], 'Invalid params', 'Incorrect response')

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?short_word=OP&document_number=0000000005&branch_id=14&'
                                        'last_consecutive=0000000006')

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)


        # envio la peticion sin el argumento last_consecutive
        response = self.request_get('', '/search?short_word=OP&document_number=0000000005&branch_id=14')
        # response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        # ******************* GET ACCOUNTING **************************
        response = self.request_get('', '/{0}/accounting_records'.format(str(self.documentHeaderId)))
        response.json = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 200, 'invalid request to accounting records')
        self.assertTrue('data' in response.json, 'not load a list of accounting records')
        self.assertEquals(response.json['data'][0]['documentHeaderId'], self.documentHeaderId,
                          'wrong assign documentheaderid to accounting')

        debits = reduce(lambda x, y: x + y, [data['debit'] for data in response.json['data']])
        credits = reduce(lambda x, y: x + y, [data['credit'] for data in response.json['data']])

        self.assertTrue(debits - credits == 0, 'wrong accounting (debits)-(credits)')

        # ******************* PUT **************************
        # obtiene el documento guardado previamente
        response = self.request_get('', '/'+str(self.documentHeaderId))
        data = json.loads(response.data.decode('utf-8'))
        # modifica el total
        data['total'] = 4000
        # realiza el update
        response = self.request_put(data, '/'+str(self.documentHeaderId))
        # valida que guardo bien
        self.assertEquals(response.status_code, 201)
        # obtiene de nuevo el documento que modifico
        response = self.request_get('', '/'+str(self.documentHeaderId))
        data = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code, 200)
        # valida que se haya guardado bien lo que modifico
        self.assertEquals(data['total'], 4000)

        # ******************* DELETE **************************
        # Test with invalid id
        response = self.request_delete('', '/0')
        self.assertEquals(response.status_code, 404)

        # Test with valid id
        path = '/' + str(self.documentHeaderId)
        response = self.request_delete('', path)
        self.assertEquals(response.status_code, 200)

        # ******************* POST (testeo de documento origen y saldos, sin saldos pendientes) ************************
        data_op = {
            "shortWord": "OP",
            "annuled": False,
            "termDays": 1,
            "subtotal": 10,
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "units": 1,
                "otr": "",
                "unitValue": 10,
                "quantity": 1,
                "balance": 1,
                "disccount": 0,
                "iva": 1.6,
                "withholdingTax": 3.5,
                "badgeValue": 10,
                "value": 10,
                "detailDate": "2016-08-29T12:00:57.000Z",
                "itemId": 1660,
                "size": False,
                "color": False,
                "consumptionTaxPercent": 0,
                "measurementUnitId": 1,
                "conversionFactor": 1,
                "costCenterId": 7,
                "divisionId": 2,
                "sectionId": 3,
                "dependencyId": 6,
                "baseValue": 10,
                "consumptionTaxBase": 10,
                "consumptionTaxValue": 0,
                "detailWarehouseId": 5,
                "ivaPUCId": 85801,
                "withholdingTaxPUCId": 85677
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "documentNumber": "0000001025",
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "currencyId": 4,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "exchangeRate": 1,
            "providerId": 15,
            "state": True,
            "branchId": 14
        }
        # guarda la orden de compra primero
        response = self.request_post_other(data_op, '/purchase_orders/?short_word=OP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('id', response.json)
        self.assertEquals(response.status_code, 200)
        self.purchase_order_id = response.json['id']
        self.detail_purchase_order = response.json['data']['documentDetails'][0]['documentDetailId']

        data_rp = {
            "shortWord": "RP",
            "dayClosed": False,
            "termDays": 0,
            "subtotal": 10,
            "paymentBy": "1",
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "accountNumber": None,
                "amount": None,
                "assetId": None,
                "authorizationNumber": None,
                "availableStock": None,
                "balance": 1,
                "bankAccountId": None,
                "bankCode": None,
                "bankName": None,
                "baseValue": 10,
                "businessAgentId": None,
                "cashRegisterId": None,
                "checkNumber": None,
                "colorId": None,
                "comments": None,
                "consumptionTaxBase": 10,
                "consumptionTaxPUCId": None,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": None,
                "costCenterId": 7,
                "createdBy": "ADMINISTRADORAA del Sistema",
                "creationDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "crossDocumentHeaderId": None,
                "customerId": None,
                "dependencyId": 6,
                "detailDate": "Mon, 29 Aug 2016 12:00:57 GMT",
                "detailDocument": None,
                "detailDocumentTypeId": 91,
                "detailPrefix": None,
                "detailWarehouseId": 5,
                "disccount": 0,
                "divisionId": 2,
                "dueDate": None,
                "employeeId": None,
                "finalDate": None,
                "financialEntityId": None,
                "globalTax": None,
                "icaPercent": None,
                "importConceptId": None,
                "initialDate": None,
                "interest": None,
                "isDeleted": None,
                "itemId": 1660,
                "iva": 1.6,
                "ivaCustomer": None,
                "ivaPUCId": 85801,
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
                "providerId": None,
                "pucId": None,
                "quantity": 1,
                "quantityRefund": None,
                "quoteNumber": None,
                "reteICA": None,
                "reteICAPercent": None,
                "sectionId": 3,
                "selected": None,
                "sizeId": None,
                "sourceDocumentDetailId": self.detail_purchase_order,
                "sourceDocumentNumber": None,
                "sourceDocumentPrefix": None,
                "sourceDocumentTypeId": None,
                "surcharge": None,
                "thirdId": None,
                "unitValue": 10,
                "units": 1,
                "updateBy": "ADMINISTRADORAA del Sistema",
                "updateDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "value": 10,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 85677,
                "withholdingValue": None,
                "size": False,
                "color": False,
                "sourceDocumentDetail":{
                    "balance": 0,
                    "documentDetailId": self.detail_purchase_order
                }
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "currencyId": 4,
            "exchangeRate": 1,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "documentNumber": "0000000194",
            "sourceDocumentHeaderId": self.purchase_order_id,
            "completedDocument": False,
            "providerId": 15,
            "branchId": 14
        }
        response = self.request_post(data_rp, '/?short_word=RP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 201)
        # Asignacion de id para hacer los demas tests
        self.purchase_remission_id = response.json['id']

        response = self.request_get_other('/purchase_orders/{0}'.format(self.purchase_order_id))
        response.json = json.loads(response.data.decode('utf-8'))
        # valida que el saldo haya quedado en 0 en la orden de compra
        self.assertEquals(0, response.json['documentDetails'][0]['balance'], 'The balance in purchase order is wrong')
        # valida que se haya cerrado el documento
        self.assertEquals(0, response.json['state'], 'The state should be false')
        print(self.purchase_order_id)
        # elimina la remision
        response = self.request_delete('', '/{0}'.format(self.purchase_remission_id))
        self.assertEquals(response.status_code, 200)

        # elimina la orden de compra primero
        response = self.request_delete_other('', '/purchase_orders/{0}'.format(self.purchase_order_id))
        self.assertEquals(response.status_code, 200)

        # ********** POST (testeo de documento origen y saldos, dejando saldos pendientes,cerrando documento origen) ***
        self.purchase_order_id = None
        self.purchase_remission_id = None
        data_op = {
            "shortWord": "OP",
            "annuled": False,
            "termDays": 1,
            "subtotal": 100,
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "units": 10,
                "otr": "",
                "unitValue": 10,
                "quantity": 10,
                "balance": 10,
                "disccount": 0,
                "iva": 1.6,
                "withholdingTax": 3.5,
                "badgeValue": 10,
                "value": 100,
                "detailDate": "2016-08-29T12:00:57.000Z",
                "itemId": 1660,
                "size": False,
                "color": False,
                "consumptionTaxPercent": 0,
                "measurementUnitId": 1,
                "conversionFactor": 1,
                "costCenterId": 7,
                "divisionId": 2,
                "sectionId": 3,
                "dependencyId": 6,
                "baseValue": 10,
                "consumptionTaxBase": 10,
                "consumptionTaxValue": 0,
                "detailWarehouseId": 5,
                "ivaPUCId": 85801,
                "withholdingTaxPUCId": 85677
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "documentNumber": "0000001025",
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "currencyId": 4,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "exchangeRate": 1,
            "providerId": 15,
            "state": True,
            "branchId": 14
        }
        # guarda la orden de compra primero
        response = self.request_post_other(data_op, '/purchase_orders/?short_word=OP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('id', response.json)
        self.assertEquals(response.status_code, 200)
        self.purchase_order_id = response.json['id']
        self.detail_purchase_order = response.json['data']['documentDetails'][0]['documentDetailId']

        data_rp = {
            "shortWord": "RP",
            "dayClosed": False,
            "termDays": 0,
            "subtotal": 10,
            "paymentBy": "1",
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "accountNumber": None,
                "amount": None,
                "assetId": None,
                "authorizationNumber": None,
                "availableStock": None,
                "balance": 1,
                "bankAccountId": None,
                "bankCode": None,
                "bankName": None,
                "baseValue": 10,
                "businessAgentId": None,
                "cashRegisterId": None,
                "checkNumber": None,
                "colorId": None,
                "comments": None,
                "consumptionTaxBase": 10,
                "consumptionTaxPUCId": None,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": None,
                "costCenterId": 7,
                "createdBy": "ADMINISTRADORAA del Sistema",
                "creationDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "crossDocumentHeaderId": None,
                "customerId": None,
                "dependencyId": 6,
                "detailDate": "Mon, 29 Aug 2016 12:00:57 GMT",
                "detailDocument": None,
                "detailDocumentTypeId": 91,
                "detailPrefix": None,
                "detailWarehouseId": 5,
                "disccount": 0,
                "divisionId": 2,
                "dueDate": None,
                "employeeId": None,
                "finalDate": None,
                "financialEntityId": None,
                "globalTax": None,
                "icaPercent": None,
                "importConceptId": None,
                "initialDate": None,
                "interest": None,
                "isDeleted": None,
                "itemId": 1660,
                "iva": 1.6,
                "ivaCustomer": None,
                "ivaPUCId": 85801,
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
                "providerId": None,
                "pucId": None,
                "quantity": 1,
                "quantityRefund": None,
                "quoteNumber": None,
                "reteICA": None,
                "reteICAPercent": None,
                "sectionId": 3,
                "selected": None,
                "sizeId": None,
                "sourceDocumentDetailId": self.detail_purchase_order,
                "sourceDocumentNumber": None,
                "sourceDocumentPrefix": None,
                "sourceDocumentTypeId": None,
                "surcharge": None,
                "thirdId": None,
                "unitValue": 10,
                "units": 1,
                "updateBy": "ADMINISTRADORAA del Sistema",
                "updateDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "value": 10,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 85677,
                "withholdingValue": None,
                "size": False,
                "color": False,
                "sourceDocumentDetail": {
                    "balance": 9,
                    "documentDetailId": self.detail_purchase_order
                }
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "currencyId": 4,
            "exchangeRate": 1,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "documentNumber": "0000000194",
            "sourceDocumentHeaderId": self.purchase_order_id,
            "sourceDocumentHeader": {
                "state": False
            },
            "completedDocument": True,
            "providerId": 15,
            "branchId": 14
        }
        response = self.request_post(data_rp, '/?short_word=RP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 201)
        # Asignacion de id para hacer los demas tests
        self.purchase_remission_id = response.json['id']

        response = self.request_get_other('/purchase_orders/{0}'.format(self.purchase_order_id))
        response.json = json.loads(response.data.decode('utf-8'))
        # valida que el saldo haya quedado en 9 en la orden de compra
        self.assertEquals(9, response.json['documentDetails'][0]['balance'], 'The balance in purchase order is wrong')
        # valida que se haya cerrado el documento
        self.assertEquals(0, response.json['state'], 'The state should be false')

        # elimina la remision
        response = self.request_delete('', '/{0}'.format(self.purchase_remission_id))
        self.assertEquals(response.status_code, 200)

        # elimina la orden de compra primero
        response = self.request_delete_other('', '/purchase_orders/{0}'.format(self.purchase_order_id))
        self.assertEquals(response.status_code, 200)

        # ******* POST (testeo de documento origen y saldos, dejando saldos pendientes, sin cerrar documento origen) ***
        self.purchase_order_id = None
        self.purchase_remission_id = None
        data_op = {
            "shortWord": "OP",
            "annuled": False,
            "termDays": 1,
            "subtotal": 100,
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "units": 10,
                "otr": "",
                "unitValue": 10,
                "quantity": 10,
                "balance": 10,
                "disccount": 0,
                "iva": 1.6,
                "withholdingTax": 3.5,
                "badgeValue": 10,
                "value": 100,
                "detailDate": "2016-08-29T12:00:57.000Z",
                "itemId": 1660,
                "size": False,
                "color": False,
                "consumptionTaxPercent": 0,
                "measurementUnitId": 1,
                "conversionFactor": 1,
                "costCenterId": 7,
                "divisionId": 2,
                "sectionId": 3,
                "dependencyId": 6,
                "baseValue": 10,
                "consumptionTaxBase": 10,
                "consumptionTaxValue": 0,
                "detailWarehouseId": 5,
                "ivaPUCId": 85801,
                "withholdingTaxPUCId": 85677
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "documentNumber": "0000001025",
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "currencyId": 4,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "exchangeRate": 1,
            "providerId": 15,
            "state": True,
            "branchId": 14
        }
        # guarda la orden de compra primero
        response = self.request_post_other(data_op, '/purchase_orders/?short_word=OP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('id', response.json)
        self.assertEquals(response.status_code, 200)
        self.purchase_order_id = response.json['id']
        self.detail_purchase_order = response.json['data']['documentDetails'][0]['documentDetailId']

        data_rp = {
            "shortWord": "RP",
            "dayClosed": False,
            "termDays": 0,
            "subtotal": 10,
            "paymentBy": "1",
            "disccount": 0,
            "ivaValue": 0.2,
            "withholdingTaxValue": 0.3,
            "consumptionTaxValue": 0,
            "disccount2Value": 0,
            "disccount2": 0,
            "baseCREE": 0,
            "valueCREE": 0,
            "total": 9.899999999999999,
            "documentDetails": [{
                "accountNumber": None,
                "amount": None,
                "assetId": None,
                "authorizationNumber": None,
                "availableStock": None,
                "balance": 1,
                "bankAccountId": None,
                "bankCode": None,
                "bankName": None,
                "baseValue": 10,
                "businessAgentId": None,
                "cashRegisterId": None,
                "checkNumber": None,
                "colorId": None,
                "comments": None,
                "consumptionTaxBase": 10,
                "consumptionTaxPUCId": None,
                "consumptionTaxPercent": 0,
                "consumptionTaxValue": 0,
                "conversionFactor": 1,
                "cost": None,
                "costCenterId": 7,
                "createdBy": "ADMINISTRADORAA del Sistema",
                "creationDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "crossDocumentHeaderId": None,
                "customerId": None,
                "dependencyId": 6,
                "detailDate": "Mon, 29 Aug 2016 12:00:57 GMT",
                "detailDocument": None,
                "detailDocumentTypeId": 91,
                "detailPrefix": None,
                "detailWarehouseId": 5,
                "disccount": 0,
                "divisionId": 2,
                "dueDate": None,
                "employeeId": None,
                "finalDate": None,
                "financialEntityId": None,
                "globalTax": None,
                "icaPercent": None,
                "importConceptId": None,
                "initialDate": None,
                "interest": None,
                "isDeleted": None,
                "itemId": 1660,
                "iva": 1.6,
                "ivaCustomer": None,
                "ivaPUCId": 85801,
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
                "providerId": None,
                "pucId": None,
                "quantity": 1,
                "quantityRefund": None,
                "quoteNumber": None,
                "reteICA": None,
                "reteICAPercent": None,
                "sectionId": 3,
                "selected": None,
                "sizeId": None,
                "sourceDocumentDetailId": self.detail_purchase_order,
                "sourceDocumentNumber": None,
                "sourceDocumentPrefix": None,
                "sourceDocumentTypeId": None,
                "surcharge": None,
                "thirdId": None,
                "unitValue": 10,
                "units": 1,
                "updateBy": "ADMINISTRADORAA del Sistema",
                "updateDate": "Mon, 29 Aug 2016 12:21:47 GMT",
                "value": 10,
                "withholdingTax": 3.5,
                "withholdingTaxPUCId": 85677,
                "withholdingValue": None,
                "size": False,
                "color": False,
                "sourceDocumentDetail": {
                    "balance": 9,
                    "documentDetailId": self.detail_purchase_order
                }
            }],
            "documentDate": "2016-08-29T12:00:57.000Z",
            "currencyId": 4,
            "exchangeRate": 1,
            "costCenterId": 7,
            "divisionId": 2,
            "sectionId": 3,
            "dependencyId": 6,
            "shipTo": "LEGAQUIMICOS SAS modificada",
            "shipAddress": "CR 13 A 12 47",
            "shipCity": "BOGOTA",
            "shipZipCode": "",
            "shipDepartment": "D.C.",
            "shipPhone": "2860084",
            "shipCountry": "COLOMBIA",
            "documentNumber": "0000000194",
            "sourceDocumentHeaderId": self.purchase_order_id,
            "sourceDocumentHeader": {
                "state": True
            },
            "completedDocument": False,
            "providerId": 15,
            "branchId": 14
        }
        response = self.request_post(data_rp, '/?short_word=RP&source_short_word=OP')
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 201)
        # Asignacion de id para hacer los demas tests
        self.purchase_remission_id = response.json['id']

        response = self.request_get_other('/purchase_orders/{0}'.format(self.purchase_order_id))
        response.json = json.loads(response.data.decode('utf-8'))
        # valida que el saldo haya quedado en 9 en la orden de compra
        self.assertEquals(9, response.json['documentDetails'][0]['balance'], 'The balance in purchase order is wrong')
        # valida que se haya cerrado el documento
        self.assertEquals(1, response.json['state'], 'The state should be true')

        # elimina la remision
        response = self.request_delete('', '/{0}'.format(self.purchase_remission_id))
        self.assertEquals(response.status_code, 200)

        # elimina la orden de compra primero
        response = self.request_delete_other('', '/purchase_orders/{0}'.format(self.purchase_order_id))
        self.assertEquals(response.status_code, 200)