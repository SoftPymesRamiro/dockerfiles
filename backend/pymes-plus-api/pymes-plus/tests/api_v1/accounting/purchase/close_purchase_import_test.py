#!/usr/bin/env python
#########################################################
# TEST purchase
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
handled close purchase improt
"""


class ClosePurchaseImportTest(unittest.TestCase):
    """
    This Class is a  Test Case for close_purchase_imports API class
    """

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

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self, data, path="/"):
        """Sent get request to #/api/v1/close_purchase_imports# with close_purchase_import data values

        :param data: close_purchase_import data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/close_purchase_imports' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_get_import(self, data, path="/"):
        """Sent get request to #/api/v1/close_purchase_imports# with close_purchase_import data values

        :param data: close_purchase_import data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/imports' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/close_purchase_imports# with close_purchase_import data values

        :param data: close_purchase_import data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/close_purchase_imports' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request

    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/close_purchase_imports# with close_purchase_import data values

        :param data: close_purchase_import data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/close_purchase_imports' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request

    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/close_purchase_imports# with close_purchase_import data values

        :param data: close_purchase_import data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/close_purchase_imports' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_close_purchase_import(self):
        """
        This function test get a close_purchase_import according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.request_get('', '/119224')  # envio la peticion
        response.json = json.loads(response.data.decode("utf-8"))  # convierte a json object
        # validacion de la clave en la respuesta
        self.assertTrue("documentHeaderId" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentTypeId" in response.json, 'incorrect response by correct request')
        self.assertTrue("closingType" in response.json, 'incorrect response by correct request')
        self.assertTrue("documentNumber" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0')  # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_close_purchase_import_search(self):
        """
        This function test get a close purchase import to search pattern
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=CM")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.test_client.get('/api/v1/document_headers/search?branchId=14&startDate=2017-03-01&limitDate='
                                        '2017-04-30&documentNumber=None&controlNumber=None&'
                                        'search=None&filterBy=None&initTotal=None&endTotal=None&shortWord=CM',
                                        data=json.dumps(''),
                                        content_type='application/json', headers=self.headers)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        print("response.json['data']>>>> ", response.json)

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' +
                                    '00000000')

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=CM&document_number=' +
                                    '0000000001')
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        close_purchase = response.json
        self.assertNotEquals(response.json, {})
        self.assertIn("total", response.json)
        # self.assertIn("controlPrefix", response.json)
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
        response = self.request_get("", "/" + str(close_purchase['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        # self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)
        self.assertIn("total", response.json)

        # response = self.test_client.get('api/v1/document_headers/'
        #                                 + str(close_purchase['documentHeaderId']) +
        #                                 '/accounting_records/preview',
        #                                 data=json.dumps(''),
        #                                 content_type='application/json', headers=self.headers)
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
        imports = {"branchId": 14, "sectionId": None, "costCenterId": 4, "dependencyId": None,
                   "divisionId": 14, "currencyId": 2, "pucId": 85090,
                   "puc": {"dueDate": False, "name": "MAQUINARIA Y EQUIPO", "percentage": 0, "pucAccount": "158805005",
                           "pucId": 85090, "quantity": False}, "date": "Mon, 03 Apr 2017 15:56:45 GMT", "state": None,
                   "isOutTime": None, "budget": 0, "code": "989", "name": "UNITTEST", "comments": None}

        response = self.test_client.post('/api/v1/imports/',
                                         data=json.dumps(imports),
                                         content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertIn("importId", response.json)

        self.importId = response.json['importId']

        invoice_import = {"sourceDocumentHeader": None, "sourceDocumentHeaderId": None, "documentNumber": "0000000131",
                          "annuled": None, "controlPrefix": None, "paymentTermId": 2,
                          "documentDate": "2017-04-03T15:56:45.000Z", "controlNumber": "2323",
                          "sourceDocumentOrigin": "FM", "termDays": 0, "dateTo": "2017-04-03T22:11:18.342Z",
                          "costCenter": None, "costCenterId": 4, "divisionId": 14, "sectionId": None,
                          "exchangeRate": 3000, "dependencyId": None, "shortWord": "FM", "sourceShortWord": "FM",
                          "currencyId": 2, "documentDetails": [
                {"indexItem": 0, "units": 0, "otr": "", "unitValue": 0, "quantity": 0, "disccount": 0, "iva": 0,
                 "withholdingTax": 4, "baseValue": 60000, "badgeValue": 20, "value": 60000,
                 "detailDate": "2017-04-03T15:56:45.000Z", "consultItem": True, "importConceptId": 194,
                 "ivaPUCId": 85795, "withholdingTaxPUCId": 85661}],
                          "provider": {"branch": "001", "isWithholdingCREE": 0,
                                       "name": "A.V.A. CHEMICALS SAS CON NOMBRE LARGO PARA VER LA VISTA PREVIA SI SE PASA A LA OTRA LINEA    (900445872) - PRINCIPAL",
                                       "providerId": 15, "thirdPartyId": 1992}, "providerId": 15, "disccount": 0,
                          "disccount2Value": 0, "ivaValue": 0, "withholdingTaxValue": 2400, "subtotal": 60000,
                          "ivaPUCId": None, "directIVA": 0, "directIVAPercent": 0, "reteICAValue": 0,
                          "reteICAPercent": 0, "reteIVAValue": 0, "reteIVAPercent": 0, "overCost": 0,
                          "overCostTaxBase": 0, "consumptionTaxValue": 0, "valueCREE": 0, "applyCree": None,
                          "reteICABase": 0, "reteIVABase": 0, "total": 57600, "payment": 57600, "percentageCREE": 0,
                          "comments": None, "paymentReceipt": {}, "documentAffecting": [], "importId": self.importId,
                          "baseCREE": 0, "branchId": 14}

        response = self.test_client.post('/api/v1/invoice_imports/',
                                         data=json.dumps(invoice_import),
                                         content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.invoice_import_document_number0 = response.json['documentNumber']
        self.invoice_import_id0 = response.json['id']

        # response = self.test_client.post('/api/v1/invoice_contract/',
        #                                  data=json.dumps(invoice_import),
        #                                  content_type='application/json', headers=self.headers)
        # response.json = json.loads(response.data.decode("utf-8"))
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.invoice_import_document_number1 = response.json['documentNumber']
        # self.invoice_import_id1 = response.json['id']

        response = self.request_get_import("",
                                    "/search?by_param=import_balance&branchId=14&import_id={0}&puc_id=85090&date=Mon,%2003%20Apr%202017%2015:56:45%20GMT".format(
                                        self.importId))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})
        self.assertIn('balance', response.json)

        self.importationValue = response.json['balance']
        # self.activoOitem = response.json['puc']['conceptAssetContract']
        # self.contractIDesc = response.json['description']
        # self.contractPucId = response.json['pucId']

        # self.assertEquals(response.json['contractId'], self.contractId)
        # self.assertEquals(response.json['pucId'], self.contractPucId)

        close_import = {"sourceDocumentHeader": None, "sourceDocumentHeaderId": None,
                                 "documentNumber": "0000000025", "annuled": None, "controlPrefix": None,
                                 "paymentTermId": 1, "documentDate": "2017-04-04T08:14:12.000Z", "controlNumber": None,
                                 "sourceDocumentOrigin": "CM", "termDays": 0, "dateTo": None, "costCenter": None,
                                 "costCenterId": 4, "divisionId": 14, "expenses": 0, "importationValue": 60000,
                                 "sectionId": None, "exchangeRate": None, "dependencyId": None, "shortWord": "CM",
                                 "sourceShortWord": "CM", "currencyId": 4, "documentDetails": [
                {"indexItem": 0, "code": "", "name": "", "units": 0, "otr": "", "unitValue": 0, "quantity": 0,
                 "value": 60000, "detailDate": "2017-04-04T08:14:12.000Z", "consultItem": True,
                 "asset": {"address": "CERCA A LA QUINTA", "assetGroupId": 4, "assetId": 24, "branchId": 14,
                           "builtArea": 0, "chassisSerial": "", "city": {"cityId": 418, "code": "001",
                                                                         "department": {"code": "11",
                                                                                        "country": {"countryId": 2,
                                                                                                    "indicative": "57"},
                                                                                        "departmentId": 3,
                                                                                        "name": "D.C."},
                                                                         "indicative": "1",
                                                                         "name": "BOGOTA - D.C. - COLOMBIA"},
                           "cityId": 418, "code": "EDI001", "comments": None, "costCenterId": 6, "costHour": 0,
                           "createdBy": "Administrador del Sistema", "creationDate": "Wed, 07 May 2014 17:04:22 GMT",
                           "dateNotarialDocument": "Wed, 07 May 2014 00:00:00 GMT", "dependencyId": None,
                           "depreciationMonth": 0, "depreciationMonthNIIF": 0, "depreciationYear": 20,
                           "depreciationYearNIIF": 0, "divisionId": 18, "engineSerial": "", "imageId": 363,
                           "isDeleted": 0, "landArea": 0, "line": "",
                           "model": 0, "name": "EDIFICIO", "netValueNIIF": 0, "notarialDocument": None, "notary": None,
                           "percentageResidual": 0, "percentageSaving": 0, "plate": "", "propertyNumber": None,
                           "puc": {"account": "110505003", "name": "ASDFG", "pucId": 84111}, "pucId": 84111,
                           "purchaseDate": "Wed, 01 Jan 2014 00:00:00 GMT", "rentable": False, "responsible": None,
                           "sectionId": None, "state": "A", "typeAsset": "I", "updateBy": "ADMINISTRADORAA del Sistema",
                           "updateDate": "Tue, 06 Sep 2016 16:06:55 GMT"}, "baseValue": 60000, "balance": 0,
                 "assetId": 24}], "provider": {"branch": "001", "isWithholdingCREE": 0,
                                               "name": "A.V.A. CHEMICALS SAS CON NOMBRE LARGO PARA VER LA VISTA PREVIA SI SE PASA A LA OTRA LINEA    (900445872) - PRINCIPAL",
                                               "providerId": 15, "thirdPartyId": 1992}, "providerId": None,
                                 "disccount": 0, "withholdingTaxValue": 0, "subtotal": 60000, "ivaPUCId": None,
                                 "applyCree": None, "total": 60000, "closingType": "1", "comments": None, "payment": 0,
                                 "paymentReceipt": {}, "ivaValue": 0, "reteIVAValue": 0, "reteICAValue": 0,
                                 "documentAffecting": [], "importId": 83, "expensesValue": 60000, "totalBase": 60000,
                                 "branchId": 14}

        # Envio la creacion del avance sin short word
        close_import["shortWord"] = None
        response = self.request_post(close_import)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        close_import["shortWord"] = "XY"
        response = self.request_post(close_import)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        close_import["shortWord"] = "CM"
        response = self.request_post(close_import)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # # Restaura el valor del avance
        # close_import['documentDetails'][0]['value'] = self.importationValue
        # # Crea un compra de item con un peso de diferencia en el debit
        # response = self.request_post(legalization_contract)
        # response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        # self.assertIn("documentNumber", response.json)
        # self.assertIn("id", response.json)
        # self.document_number0a = response.json['documentNumber']
        # self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        # close_import['documentDetails'][0]['value'] = self.importationValue
        # response = self.request_post(legalization_contract)
        # response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=CM&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        close_import2 = response.json
        # response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(close_import2)
        # Cambio el total
        purchase_copy['documentDetails'][0]['value'] = 70000
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
        purchase_copy['documentDetails'][0]['value'] = 50000
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = self.importationValue
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        # purchase_copy['documentDetails'][0]['value'] = self.importationValue
        # purchase_copy['comments'] = "Este es el test"
        # # Actualizo nuevamente
        # response = self.request_put(purchase_copy, "/" + str(self.id))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta
        # self.assertIn("ok", response.json)

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
        self.assertEquals(response.status_code, 200)

        # response = self.request_delete("", "/" + str(self.id0a))
        # response.json = json.loads(response.data.decode("utf-8"))
        # # Respuesta de eliminacion
        # self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('Close Purchase Import Not Found', response.json['message'],
                         'incorrect response by bad request')

        # Eliminar la factura de importacion
        response = self.test_client.delete('/api/v1/invoice_imports/{0}'.format(self.invoice_import_id0), content_type='application/json',
                                           headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 200)

        # Eliimina la importacion
        response = self.test_client.delete('/api/v1/imports/{0}'.format(self.importId), content_type='application/json',
                                           headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)


