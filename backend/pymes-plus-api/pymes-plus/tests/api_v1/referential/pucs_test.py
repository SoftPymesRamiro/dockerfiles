 #!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
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
from copy import *


from app import create_app
from app.api_v1 import api

"""
This Class is a Test Case for Pucs API class
"""
class PucsTest(unittest.TestCase):
    """
    This Class is a Test Case for Pucs API class
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
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/puc'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent get request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/puc'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent get request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/puc'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent get request to #/api/v1/providers# with providers data values

        :param data: providers data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/puc'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_puc(self):
        """
        This function test get puc by Id
        ** First validate that contains the data key and content
        """
        response = self.request_get("", "/0")
        response.json = json.loads(response.data.decode("utf-8"))
        # print(response.json)

        self.assertTrue(response.json['code'] == 404)

        response = self.request_get("", "/84105")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('pucId' in response.json)

    def test_search_pucs(self):
        """
        This function test search a pucs according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        response = self.request_get("", "/search?to_items=1&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("ivaPurchasePUC" in response.json)
        self.assertTrue("ivaSalePUC" in response.json)
        self.assertTrue("incomingPUC" in response.json)
        self.assertTrue("costPUC" in response.json)
        self.assertTrue("withholdingTaxPurchasePUC" in response.json)
        self.assertTrue("inventoryPUC" in response.json)

        response = self.request_get("", "/search?by_param=withholdingTaxPurchase&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)

        response = self.request_get("", "/search?by_param=ivaPurchase&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue("data" in response.json)

        response = self.request_get("",
                                    "/search?&by_param=purchaseListWithType&paginate=true&company_id=1&iva_code=G"
                                    "&search=&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=saleListWithType&paginate=true&company_id=1&iva_code=G&search="
                                    "&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=bonus&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=taxConsumption&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=withholdingTaxPurchase&paginate=true&company_id=1&search="
                                    "&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=withholdingTaxSale&paginate=true&company_id=1&search="
                                    "&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=inventory&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        response = self.request_get("",
                                    "/search?&by_param=incoming&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=cost&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=expensesPuc&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=expenses&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=depreciation&paginate=true&company_id=1&search=&page_size=10"
                                    "&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=inventoryImpairment&paginate=true&company_id=1&search="
                                    "&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        response = self.request_get("",
                                    "/search?&by_param=allWithoutAuxiliary&paginate=true&company_id=1&search="
                                    "&page_size=10&page_number=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('listPUC' in response.json)
        self.assertTrue('totalCount' in response.json)
        self.assertTrue('totalPages' in response.json)
        self.assertTrue(len(response.json['listPUC']) <= 10)

        # TODO: Faltan agregar los metodos que no se han realizado de search by param

        response = self.request_get("", "/search?account_name=True&company_id=1&puc_class=1&puc_sub_class=0"
                                        "&puc_account=00&puc_sub_account=00&puc_auxiliary1=000")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('name' in response.json)
        self.assertTrue(response.json['name'].upper() == "ACTIVO")

        response = self.request_get("", "/search?account_name=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=00&puc_sub_account=00&puc_auxiliary1=000")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('name' in response.json)
        self.assertTrue(response.json['name'].upper() == "ACTIVO - DISPONIBLE")

        response = self.request_get("", "/search?account_name=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=00&puc_auxiliary1=000")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('name' in response.json)
        self.assertTrue(response.json['name'].upper() == "CAJA")

        response = self.request_get("", "/search?account_name=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=05&puc_auxiliary1=000")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('name' in response.json)
        self.assertTrue(response.json['name'].upper() == "CAJA GENERAL")

        response = self.request_get("", "/search?account_name=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=05&puc_auxiliary1=999")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue(response.json['code'] == 404)

        response = self.request_get("", "/search?full_account=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=05&puc_auxiliary1=999")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue(response.json['code'] == 404)

        response = self.request_get("", "/search?full_account=True&company_id=1&puc_class=1&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=05&puc_auxiliary1=005")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('pucId' in response.json)
        self.assertTrue('pucs' in response.json)
        self.assertEqual(type(response.json['pucs']), type([]))

        response = self.request_get("", "/search?unique_by_param=creeRetainingSale&puc_id=84105&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('data' in response.json)

        response = self.request_get("", "/search?unique_by_param=creeRetainingSales&puc_id=84105&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue(response.json['status'] == 500)

        response = self.request_get("", "/search?unique_by_param=creeRetainingSale&puc_id=85722&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue(response.json['code'] == 404)

        response = self.request_get("", "/search?unique_by_param=creeRetainingSale&puc_id=&company_id=1")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('data' in response.json)

        response = self.request_get("", "/search?company_id=1&search=AS")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertTrue('data' in response.json)

        response = self.request_get("", "/search?full_names=True&company_id=1&puc_class=4&puc_sub_class=1"
                                        "&puc_account=05&puc_sub_account=05&puc_auxiliary1=000")
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.json['name'].upper(), 'CULTIVO DE CEREALES')
        self.assertEqual(response.json['subAccountName1'].upper(), 'CULTIVO DE CEREALES')
        self.assertEqual(response.json['accountName'].upper(), 'INGRESOS OPERACIONALES - AGRICULTURA, GANADERIA, CAZA Y SILVICULTU')
        self.assertEqual(response.json['pucSubClassName'].upper(), 'INGRESOS OPERACIONALES')
        self.assertEqual(response.json['pucClassName'].upper(), 'INGRESOS')

    def test_post_put_delete_puc(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        data = {
            "companyId": 1,
            "pucClass": "1",
            "pucSubClass": "0",
            "account": "05",
            "subAccount": "05",
            "auxiliary1": "006",
            "billingConceptsInventories": True,
            "billingConceptsFixedAssetsIntangibles": True,
            "billingConceptsFixedAssetsPropertyPlantEquipment": False,
            "billingConceptsFixedAssetsOther": False,
            "name": "CREATECLB",
            "depreciationPucObj": {
                "account": "159205005 CONSTRUCCIONES Y EDIFICACIONES",
                "name": "CONSTRUCCIONES Y EDIFICACIONES",
                "percentage": 0,
                "pucId": 85119
            },
            "expensesPucObj": {
                "account": "510521005 VIATICOS",
                "name": "VIATICOS",
                "percentage": 0,
                "pucId": 87319
            },
            "conceptsNationalProviderPayment": True,
            "otherDiscounts": True,
            "valuesReceivedThirdParties": True,
            "depreciationFixedAssetsAccount": True,
            "expenseDifferenceChange": False,
            "incomeDifferenceChange": False,
            "holdingExpenseProvision": False,
            "otherAssetRetirementExpenses": True,
            "expenseIncome": True,
            "loansFromOtherThirdParties": True,
            "movingHomeBranch": False,
            "typesDebitInventoryAdjustment": True,
            "interestReceived": True,
            "icbfContributions": True,
            "interestonLayoffProvisionExpense": True,
            "provisionlayoffs": False,
            "integralSalary": True,
            "interestonLayoffProvision": True,
            "creditCardAccounts": False,
            "foreignExchangeFinancialEntity": True,
            "legalizationConceptsLowerBox": True,
            "industryCommerceTax": True,
            "creditBalanceIVAPayments": False,
            "salesTaxPaidSimplifiedRegimen": False,
            "importsIVA": True,
            "icaRetainingSale": False,
            "withholdingTaxSalary": False,
            "creeRetainingSale": False,
            "withholdingRetainingService": False,
            "icaRetainingService": False,
            "withholdingRetainingSale": False,
            "exemptRetefuente": True,
            "incurredTax": False,
            "retention": True,
            "dianPaymentsInForeignRent": True,
            "ivaPurchaseTradeZone": True,
            "dianIVAPurchasesOrServicesSimplifiedSystem": True,
            "dianNationalRate": True,
            "debitOrderAccounts": True,
            "className": "NOMBRE NIFF",
            "subAccountName": "SUB NIFF",
            "auxiliaryName": "AUX NIFF",
            "aCurrent": True,
            "nonCurrent": True,
            "implicitInterestPurchase": True,
            "implicitInterest": True,
            "customerFinancement": True,
            "distressedInventory": True,
            "inventoryImpairment": True,
            "implicitInterestIncome": True,
            "assosiateAccount": "",
            "pucs": [
            {
                "account": "110505005 EFECTIVO MOD",
                "name": "EFECTIVO MOD",
                "percentage": 0,
                "pucId": 84113
            },
            {
                "account": "110505009 ASDASD",
                "name": "ASDASD",
                "percentage": 0,
                "pucId": 84115
            }
            ],
            "conceptsCostsAndExpensesPayable": True,
            "conceptsProductionOrders": True,
            "partner": True,
            "deferredCharges": True,
            "deteriorationPucObj": {
            "account": "149905005 PARA OBSOLESCENCIA",
            "name": "PARA OBSOLESCENCIA",
            "percentage": 0,
            "pucId": 84741
            },
            "nature": "C",
            "percentage": "10.00",
            "depreciationPUC": 85119,
            "deteriorationPUC": 84741,
            "expensesPUC": 87319,
            "associationList": [
                84113,
                84115
                ]
            }
        # envio la peticion al sevidor
        response = self.request_post(data)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("pucId", response.json)
        self.pucId = response.json['pucId']

        data_copy = copy(data)
        data_copy['pucId'] = self.pucId
        data_copy["name"] = "CLNUPDATE"
        data_copy["nature"] = 'D'
        data_copy["percentage"] = "5.05"

        # envio la peticion al sevidor
        response = self.request_put(data_copy)

        self.assertEqual('405 METHOD NOT ALLOWED', response.status,
                         '405 METHOD NOT ALLOWED is correct response')

        # envio la peticion al sevidor
        response = self.request_put(data_copy, "/" + str(self.pucId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('ok', response.json)

        # *******************************
        response = self.request_get("", "/" + str(self.pucId))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual(response.json["className"].upper(), "NOMBRE NIFF")
        self.assertEqual(response.json["expenseIncome"], True)

        self.assertEqual(data_copy['pucId'], response.json['pucId'])
        self.assertEqual(data_copy["name"], response.json["name"])
        self.assertEqual(data_copy["nature"], response.json["nature"])
        self.assertEqual(float(data_copy["percentage"]), response.json["percentage"])

        response = self.request_delete(data_copy, "/" + str(self.pucId))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('ok', response.json)


