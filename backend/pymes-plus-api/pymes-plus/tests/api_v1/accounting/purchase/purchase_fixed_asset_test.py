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
handled purchase_fixed_asset
"""
class PurchaseFixedAssetTest(unittest.TestCase):
    """
    This Class is a  Test Case for purchase_fixed_asset API class
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
        """Sent get request to #/api/v1/purchase_fixed_asset# with purchase_fixed_asset data values

        :param data: purchase_fixed_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/purchase_fixed_assets' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/purchase_fixed_asset# with purchase_fixed_asset data values

        :param data: purchase_fixed_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/purchase_fixed_assets' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/purchase_fixed_asset# with purchase_fixed_asset data values

        :param data: purchase_fixed_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/purchase_fixed_assets' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/purchase_fixed_asset# with purchase_fixed_asset data values

        :param data: purchase_fixed_asset data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/purchase_fixed_assets' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_purchaseItem(self):
        """
        This function test get a Purchase FAsset according to identifier
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

    def test_get_purchase_fixed_asset_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("", "/search?branch_id=14&short_word=FP")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200, "")

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=FP&document_number=0000002852')
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        purchase_fixed_asset = response.json

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' + purchase_fixed_asset[
            'documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('',
                                    '/search?branch_id=14&short_word=FP&document_number=' + purchase_fixed_asset['documentNumber'])
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/search?search=dsadsadlsakdjs")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.json, {})

        # ################## GET
        response = self.request_get("", "/117")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        # Peticion correcta
        response = self.request_get("", "/" + str(purchase_fixed_asset['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        # response = self.request_get("", "/" + str(purchase_fixed_asset['documentHeaderId']) + "/preview?format=P")
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
        purchase_fixed_asset = {'disccount2Value': 0, 'comments': 'esta es una prueba', 'disccount2TaxBase': 0, 'sourceDocumentOrigin': 'FPA', 'divisionId': 13, 'dateTo': '2017-03-30T17:22:24.472Z', 'reteICAValue': 20000, 'withholdingTaxValue': 350000, 'reteICAPercent': '2.00', 'sourceShortWord': 'FPA', 'costCenter': None, 'documentDate': '2017-03-30T09:02:57.000Z', 'annuled': None, 'reteIVABase': 1600000, 'reteICABase': 0, 'sectionId': 7, 'termDays': 0, 'percentageCREE': 0, 'consumptionTaxValue': 400000, 'ivaValue': 1600000, 'total': 981598000, 'branchId': 14, 'shortWord': 'FP', 'reteIVAPercent': '2.00', 'currencyId': 4, 'documentAffecting': [], 'paymentReceipt': {}, 'controlPrefix': 'TST', 'dependencyId': None, 'controlNumber': '99999', 'disccount2': 0, 'applyCree': None, 'disccount': 0, 'exchangeRate': 1, 'retentionPercent': '2.00', 'baseCREE': 0, 'costCenterId': 4, 'retentionPUCId': 85832, 'sourceDocumentHeaderId': None, 'providerId': 532, 'subtotal': 1000000000, 'valueCREE': 0, 'paymentTermId': 2, 'reteIVAValue': 32000, 'documentNumber': '0000003123', 'payment': 981598000, 'provider': {'name': ' PENA TORRES JEFFERSON AMADO (56403) - ASESORES JPT', 'isWithholdingCREE': 0, 'providerId': 532, 'branch': '789', 'thirdPartyId': 2394}, 'retentionValue': 20000000, 'documentDetails': [{'detailDate': '2017-03-30T09:02:57.000Z', 'value': 1000000000, 'consultItem': True, 'withholdingTaxPUCId': 85664, 'iva': 16, 'code': '', 'consumptionTax': {'pucId': 85857, 'pucAccount': '246205005', 'percentage': 4, 'quantity': False, 'name': 'IMPUESTO AL CONSUMO 4%', 'dueDate': True}, 'name': '', 'ivaPUCId': 85796, 'withholdingTax': 3.5, 'baseValue': 10000000, 'badgeValue': 0, 'consumptionTaxBase': 10000000, 'indexItem': 0, 'assetId': 77, 'consumptionTaxPUC': '', 'asset': {'percentageSaving': 0, 'responsible': None, 'comments': None, 'engineSerial': None, 'model': None, 'assetGroupId': None, 'updateDate': 'Mon, 27 Mar 2017 14:26:08 GMT', 'puc': {'pucId': 84776, 'account': '150605005', 'name': 'TUBERÍAS Y EQUIPO'}, 'netValueNIIF': 0, 'builtArea': 0, 'line': None, 'chassisSerial': None, 'costHour': 0, 'rentable': False, 'city': {'cityId': 822, 'code': '001', 'name': 'CALI - VALLE DEL CAUCA - COLOMBIA', 'indicative': '2', 'department': {'code': '76', 'name': 'VALLE DEL CAUCA', 'departmentId': 24, 'country': {'countryId': 2, 'indicative': '57'}}}, 'propertyNumber': None, 'assetId': 77, 'state': 'A', 'sectionId': None, 'dateNotarialDocument': 'Mon, 27 Mar 2017 19:25:20 GMT', 'purchaseDate': 'Mon, 27 Mar 2017 19:25:20 GMT', 'notarialDocument': None, 'branchId': 14, 'name': 'ACTIVO 8585', 'landArea': 0, 'isDeleted': None, 'divisionId': 15, 'code': '8585', 'dependencyId': None, 'imageId': None, 'percentageResidual': 0, 'depreciationMonth': 0, 'plate': None, 'costCenterId': 5, 'depreciationYearNIIF': 0, 'typeAsset': 'I', 'creationDate': 'Mon, 27 Mar 2017 14:26:08 GMT', 'createdBy': 'ADMINISTRADOR UPDATE del Sistema', 'depreciationMonthNIIF': 0, 'address': None, 'pucId': 84776, 'notary': None, 'updateBy': 'ADMINISTRADOR UPDATE del Sistema', 'cityId': 822, 'logoConvert': '', 'depreciationYear': 0}, 'consumptionTaxPercent': 4, 'disccount': 0, 'consumptionTaxPUCId': 85857}]}
        # Envio la creacion del avance sin short word
        purchase_fixed_asset["shortWord"] = None
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        purchase_fixed_asset["shortWord"] = "XY"
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        purchase_fixed_asset["shortWord"] = "FP"
        # Crea un compra de item con un peso de diferencia en el credit
        purchase_fixed_asset['documentDetails'][0]['value'] = 1000000000.1
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        purchase_fixed_asset['documentDetails'][0]['value'] = 1000000000
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        purchase_fixed_asset['documentDetails'][0]['value'] = 1000000000
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']

        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currencyId = purchase_fixed_asset['currencyId']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        purchase_fixed_asset["currencyId"] = 2
        # Crea el compra de item con una moneda extranjera
        response = self.request_post(purchase_fixed_asset)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        purchase_fixed_asset["currencyId"] = currencyId

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

        purchase_fixed_asset2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(purchase_fixed_asset2)
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
        purchase_copy['documentDetails'][0]['value'] = 1220000000.98
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)

        # Establece el valor correcto a la compra
        purchase_copy['documentDetails'][0]['value'] = 1000000000
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
        purchase_copy['documentDetails'][0]['value'] = 1000000000
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

        self.assertEqual('PURCHASE FIXED ASSET NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')