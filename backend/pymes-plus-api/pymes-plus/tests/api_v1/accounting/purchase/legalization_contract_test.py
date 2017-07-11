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
handled legalization_contract
"""
class LegalizationContractTest(unittest.TestCase):
    """
    This Class is a  Test Case for legalization_contract API class
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
        """Sent get request to #/api/v1/legalization_contract# with legalization_contract data values

        :param data: legalization_contract data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/legalization_contracts' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_post(self, data, path="/"):
        """Sent post request to #/api/v1/legalization_contract# with legalization_contract data values

        :param data: legalization_contract data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/legalization_contracts' + path,
                                     data=json.dumps(data),
                                     content_type='application/json', headers=self.headers)  # envio el request


    def request_put(self, data, path="/"):
        """Sent put request to #/api/v1/legalization_contract# with legalization_contract data values

        :param data: legalization_contract data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/legalization_contracts' + path,
                                    data=json.dumps(data),
                                    content_type='application/json', headers=self.headers)  # envio el request


    def request_delete(self, data, path="/"):
        """Sent delete request to #/api/v1/legalization_contract# with legalization_contract data values

        :param data: legalization_contract data
        :type data: json object, default None
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/legalization_contracts' + path,
                                       data=json.dumps(data),
                                       content_type='application/json', headers=self.headers)  # envio el request

    ######################################################################################
    def test_get_legalization_contract(self):
        """
        This function test get a legalization_contract according to identifier
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

    def test_get_legalization_contract_search(self):
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
                                        'search=null&filterBy=null&initTotal=null&endTotal=null&shortWord=LT',
                             data=json.dumps(''),
                             content_type='application/json', headers=self.headers)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        print("response.json['data']>>>> ", response.json)

        legalization_contract = response.json['data'][0]

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number=' +
                                    legalization_contract['documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=LT&document_number=' +
                                    legalization_contract['documentNumber'])
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
        response = self.request_get("", "/" + str(legalization_contract['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("controlPrefix", response.json)
        self.assertIn("documentDate", response.json)
        self.assertIn("documentHeaderId", response.json)
        self.assertIn("total", response.json)

        # response = self.test_client.get('api/v1/document_headers/'
        #                                 +str(legalization_contract['documentHeaderId'])+
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
        contracts={
          'budget': 90000000.0,
          'isDeleted': 0,
          'costCenterId': 6,
          'creationDate': 'Wed, 16 Sep 2015 09:54:32 GMT',
          'comments': 'TEST AGREEMENT',
          'sectionId': 8,
          'state': True,
          'puc': {
            'percentage': 0.0,
            'name': 'VIAS DE COMUNICACION',
            'companyId': 1,
            'account': '115515005',
            'pucId': 84789
          },
          'providerId': None,
          'pucId': 84789,
          'code': str(uuid.uuid4())[:8],
          'divisionId': 17,
          'description': 'TEST AGREEMENT',
          'dependencyId': None,
          'branchId': 14
        }
        response = self.test_client.post('/api/v1/contracts/',
                                     data=json.dumps(contracts),
                                     content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))  # convert to json object
        self.assertIn("contractId", response.json)

        self.contractId = response.json['contractId']

        invoice_contract = {
          "withholdingTaxBase": 0,
          "shortWord": "FT",
          "retentionBase": None,
          "reteICAPercent": 0,
          "reteivaBase": 0,
          "documentAffecting": [],
          "providerId": 532,
          "ivaPUC": None,
          "retentionPUCId": None,
          "reteIVABase": 0,
          "withholdingTaxValue": 0,
          "subtotal": 1000000,
          "paymentTerm": {
            "updateDate": "Mon, 05 Sep 2016 11:33:21 GMT",
            "quotaNumbers": 0,
            "name": "Credito",
            "createdBy": "Migracion",
            "termDays": 0,
            "needTermDays": 1,
            "interestRate": 0.01,
            "isDeleted": 0,
            "paymentTermId": 2,
            "updateBy": "ADRIAN",
            "promptPayment": 0,
            "quota": 0,
            "creationDate": "Fri, 17 Aug 2012 10:35:28 GMT",
            "code": "02"
          },
          "currency": {
            "createdBy": "Migracion",
            "updateDate": "Tue, 11 Oct 2016 11:52:54 GMT",
            "name": "PESO COLOMBIANO",
            "isDeleted": 0,
            "updateBy": "ADMINISTRADOR UPDATE del Sistema",
            "code": "COP",
            "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
            "symbol": "$",
            "currencyId": 4
          },
          "freight": 0,
          "ivaValue": 0,
          "currencyId": 4,
          "reteIVAPercent": 0,
          "documentDetails": [],
          "payment": 1000000,
          "reteIVAValue": 0,
          "exchangeRate": 1,
          "section": {
            "expenses": None,
            "name": "PROOOO",
            "dependencies": [
              {
                "dependencyId": 4,
                "updateDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                "expenses": None,
                "createdBy": "ADMINISTRADOR",
                "pucId": None,
                "puc": None,
                "sectionId": 8,
                "isDeleted": 0,
                "updateBy": "ADMINISTRADOR",
                "code": "0001",
                "creationDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                "name": "PROOO2"
              }
            ],
            "createdBy": "ADMINISTRADOR",
            "divisionId": 17,
            "puc": None,
            "updateBy": "ADMINISTRADOR",
            "sectionId": 8,
            "isDeleted": 0,
            "pucId": None,
            "updateDate": "Tue, 08 Sep 2015 09:57:25 GMT",
            "creationDate": "Tue, 08 Sep 2015 09:57:25 GMT",
            "code": "1"
          },
          "total": 1000000,
          "controlNumber": "23323",
          "ivaPercent": 0,
          "annuled": None,
          "documentHeaderId": None,
          "reteICAValue": 0,
          "ivaBase": 0,
          "withholdingTaxPUCId": None,
          "termDays": 0,
          "documentDate": "2017-03-29T15:02:18.000Z",
          "reteicaBase": 1000000,
          "dependencyId": None,
          "dateTo": "2017-03-29T20:12:21.994Z",
          "pucId": 84789,
          "retentionValue": None,
          "reteICAPUC": None,
          "paymentNumber": None,
          "divisionId": 17,
          "dependency": None,
          "provider": {
            "isWithholdingCREE": 0,
            "providerId": 532,
            "thirdPartyId": 2394,
            "name": " PENA TORRES JEFFERSON AMADO (56403) - ASESORES JPT",
            "branch": "789"
          },
          "controlPrefix": "FF",
          "sourceShortWord": "FT",
          "description": "TEST AGREEMENT",
          "contractId": self.contractId,
          "valueCREE": 0,
          "retentionPercent": None,
          "reteIVAPUC": None,
          "withholdingTaxPUC": None,
          "comments": None,
          "interest": None,
          "employeeId": None,
          "costCenter": {
            "isDeleted": 0,
            "updateDate": "Wed, 14 Aug 2013 10:43:11 GMT",
            "divisions": [
              {
                "expenses": "Cuenta 51",
                "costCenterId": 6,
                "createdBy": "DENNY ORJUELA",
                "divisionId": 17,
                "puc": {
                  "percentage": 0,
                  "pucAccount": "510000000",
                  "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
                  "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
                  "pucId": 87304
                },
                "updateBy": "Administrador del Sistema",
                "pucId": 87304,
                "isDeleted": 0,
                "sections": [
                  {
                    "expenses": None,
                    "name": "PROOOO",
                    "dependencies": [
                      {
                        "dependencyId": 4,
                        "updateDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                        "expenses": None,
                        "createdBy": "ADMINISTRADOR",
                        "pucId": None,
                        "puc": None,
                        "sectionId": 8,
                        "isDeleted": 0,
                        "updateBy": "ADMINISTRADOR",
                        "code": "0001",
                        "creationDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                        "name": "PROOO2"
                      }
                    ],
                    "createdBy": "ADMINISTRADOR",
                    "divisionId": 17,
                    "puc": None,
                    "updateBy": "ADMINISTRADOR",
                    "sectionId": 8,
                    "isDeleted": 0,
                    "pucId": None,
                    "updateDate": "Tue, 08 Sep 2015 09:57:25 GMT",
                    "creationDate": "Tue, 08 Sep 2015 09:57:25 GMT",
                    "code": "1"
                  }
                ],
                "updateDate": "Fri, 23 Aug 2013 11:40:48 GMT",
                "creationDate": "Wed, 14 Aug 2013 10:43:24 GMT",
                "name": "ADMINISTRACION",
                "code": "00001"
              },
              {
                "expenses": "Cuenta 52",
                "costCenterId": 6,
                "createdBy": "Administrador del Sistema",
                "divisionId": 18,
                "puc": {
                  "percentage": 0,
                  "pucAccount": "520000000",
                  "account": "520000000 GASTOS - OPERACIONALES DE VENTAS",
                  "name": "GASTOS - OPERACIONALES DE VENTAS",
                  "pucId": 87687
                },
                "updateBy": "Administrador del Sistema",
                "pucId": 87687,
                "isDeleted": 0,
                "sections": [],
                "updateDate": "Fri, 23 Aug 2013 11:41:02 GMT",
                "creationDate": "Fri, 23 Aug 2013 11:41:02 GMT",
                "name": "VENTAS",
                "code": "00002"
              }
            ],
            "costCenterId": 6,
            "createdBy": "DENNY ORJUELA",
            "updateBy": "DENNY ORJUELA",
            "branchId": 14,
            "creationDate": "Wed, 14 Aug 2013 10:43:11 GMT",
            "name": "BODEGA",
            "code": "00003"
          },
          "costCenterId": 6,
          "disccount": 0,
          "contract": response.json,
          "withholdingTaxPercent": 0,
          "insurance": 0,
          "branchId": 14,
          "paymentReceipt": {},
          "division": {
            "expenses": "Cuenta 51",
            "costCenterId": 6,
            "createdBy": "DENNY ORJUELA",
            "divisionId": 17,
            "puc": {
              "percentage": 0,
              "pucAccount": "510000000",
              "account": "510000000 GASTOS - OPERACIONALES DE ADMINISTRACION",
              "name": "GASTOS - OPERACIONALES DE ADMINISTRACION",
              "pucId": 87304
            },
            "updateBy": "Administrador del Sistema",
            "pucId": 87304,
            "isDeleted": 0,
            "sections": [
              {
                "expenses": None,
                "name": "PROOOO",
                "dependencies": [
                  {
                    "dependencyId": 4,
                    "updateDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                    "expenses": None,
                    "createdBy": "ADMINISTRADOR",
                    "pucId": None,
                    "puc": None,
                    "sectionId": 8,
                    "isDeleted": 0,
                    "updateBy": "ADMINISTRADOR",
                    "code": "0001",
                    "creationDate": "Tue, 08 Sep 2015 10:07:35 GMT",
                    "name": "PROOO2"
                  }
                ],
                "createdBy": "ADMINISTRADOR",
                "divisionId": 17,
                "puc": None,
                "updateBy": "ADMINISTRADOR",
                "sectionId": 8,
                "isDeleted": 0,
                "pucId": None,
                "updateDate": "Tue, 08 Sep 2015 09:57:25 GMT",
                "creationDate": "Tue, 08 Sep 2015 09:57:25 GMT",
                "code": "1"
              }
            ],
            "updateDate": "Fri, 23 Aug 2013 11:40:48 GMT",
            "creationDate": "Wed, 14 Aug 2013 10:43:24 GMT",
            "name": "ADMINISTRACION",
            "code": "00001"
          },
          "puc": {
            "depreciationConcepts": False,
            "bankAccounts": False,
            "cash": False,
            "discountPurchases": False,
            "checks": False,
            "feedLegalizationEmployees": False,
            "ivaPurchaseProperty": False,
            "accruedInterestPayableOnLayoffs": False,
            "legalizationExpensesPayable": False,
            "soiTaxCreditContributions": False,
            "holdingExpenseProvision": False,
            "dianDividendsAndShares": False,
            "premiumsPayable": False,
            "subsistenceFundContributions": False,
            "incurredTax": False,
            "auxiliaryName": None,
            "loansFromOtherThirdParties": False,
            "provisionVacation": False,
            "mainDocument": False,
            "billingConceptsFixedAssetsOther": False,
            "asset": True,
            "dianIVAChargeOfCommon": False,
            "dianBetsAndSimilar": False,
            "distressedInventory": False,
            "importsIVA": False,
            "provisionBonusExpense": False,
            "contributionsHealth": False,
            "typesCreditInventoryAdjustment": False,
            "deferredInterest": False,
            "creeRetainingSale": False,
            "reteICAPurchase": False,
            "netIncome": False,
            "accountsPayableHolidays": False,
            "billingConceptsInventoryConsignmentCustomer": False,
            "nature": "D",
            "deferredIncome": False,
            "icbfContributionsExpense": False,
            "staffCosts": False,
            "occupationalInsuranceContributions": False,
            "article": False,
            "pensionFundContributions": False,
            "productionExpenseLabor": False,
            "auxiliary2": "000",
            "otherDiscounts": False,
            "dianRents": False,
            "laborObligations": False,
            "ivaSaleBeer": False,
            "deferredCharges": False,
            "generalInvestment": False,
            "subAccountName": "CONSTRUCCIONES EN CURSO",
            "giftVoucher": False,
            "implicitInterestPurchase": False,
            "monthlySalary": False,
            "discountSales": False,
            "dianPaymentsInForeignRent": False,
            "ivaSaleGambling": False,
            "withholdingTaxSale": False,
            "accountPayableLayoff": False,
            "withholdingCREESale": False,
            "updateDate": "Fri, 09 Aug 2013 11:25:32 GMT",
            "changeNote": False,
            "dueDate": False,
            "otherAssetRetirementExpenses": False,
            "ivaPurchase": False,
            "foreignCurrencyAccountsreceivable": False,
            "className": "PROPIEDADES, PLANTA Y EQUIPO",
            "legalizationConceptsLowerBox": True,
            "disabilities": False,
            "provisionlayoffs": False,
            "customer": False,
            "inflationConcepts": False,
            "patrimony": False,
            "withholdingFinancialIncome": False,
            "loansPrivateConcepts": False,
            "ccfContributions": False,
            "third": False,
            "investmentLoss": False,
            "sanctionsPayingTaxes": False,
            "incentiveExpenses": False,
            "companyId": 1,
            "billingConceptsInvestment": False,
            "compensation": False,
            "billingConceptsInventories": False,
            "expenseIncome": False,
            "provisionlayoffsExpense": False,
            "creditBalanceICAPayments": False,
            "legalCurrencyAccountsReceivable": False,
            "saleByThirdParties": False,
            "salesReteIVA": False,
            "industryCommerceTax": False,
            "gainsAndLosses": False,
            "imports": False,
            "updateBy": "Administrador del Sistema",
            "subAccount": "15",
            "productionSpendingMachineHours": False,
            "conceptsPaymentsOtherThirdParties": False,
            "provisionHolding": False,
            "movingBranchDestination": False,
            "ivaSale": False,
            "lossFixedAssets": False,
            "quantity": False,
            "accountsPayableForeignProvider": False,
            "revolvingFundPayoutTo": False,
            "foreignExchangeFinancialEntity": False,
            "accountsPayableReport": False,
            "interestReceived": False,
            "consumptionTax": False,
            "integralSalary": False,
            "conceptsNationalProviderPayment": False,
            "pucs": [],
            "ivaPurchaseService": False,
            "operationalIncome": False,
            "creditBalanceIVAPayments": False,
            "provisionCancelHolding": False,
            "legalizationLowerBox": False,
            "billingConceptsInventoryConsignment": False,
            "creationDate": "Fri, 09 Aug 2013 11:25:32 GMT",
            "dianHonorary": False,
            "retirementExpensesPropertyPlantEquipment": False,
            "insurance": False,
            "ivaSaleTradeZone": False,
            "technicalServiceFromAbroadWithoutAgreement": False,
            "taxExpenseIndustryCommerce": False,
            "deprecation": {
              "expensePUC": None,
              "deprecationPUC": None
            },
            "serviceExpenses": False,
            "thirdRequiredDCNB": False,
            "icaRetainingSale": False,
            "typesDebitInventoryAdjustment": False,
            "returningCustomer": False,
            "expensesInternalConsumption": False,
            "dianServices": False,
            "expenseDifferenceChange": False,
            "provider": False,
            "contributionsExpenseDifferenceInSOI": False,
            "loansFromPartnersShareholders": False,
            "incomeDifferenceChange": False,
            "customerAccountsReceivable": False,
            "assetsConsigningCustomer": False,
            "implicitInterestIncome": False,
            "provisionBonus": False,
            "investmentIncome": False,
            "account": "08",
            "conceptsAbroadProviderPayment": False,
            "incentive": False,
            "exemptRetefuente": False,
            "interestLayoffs": False,
            "creditorsOrderAccounts": False,
            "needCashRegister": False,
            "aCurrent": False,
            "conceptInventoryContract": False,
            "lessCashPayoutTo": False,
            "inventoryImpairment": False,
            "weightAdjustmentExpense": False,
            "utilitiesAndOrLossesLastYear": False,
            "forwardConceptsEmployeesLegalization": True,
            "incomeAdjustingWeight": False,
            "assetValuation": False,
            "customerFinancement": False,
            "employee": False,
            "conceptsIndirectCostsManufacturing": False,
            "ivaSaleAIU": False,
            "freightSales": False,
            "dianNationalRate": False,
            "layoffs": False,
            "billingConceptsContractsCostsExpensesPayable": False,
            "dianIVAPurchasesOrServicesSimplifiedSystem": False,
            "alternateDoc": False,
            "dianFinancialPerformance": False,
            "pensionSolidarityFundContributions": False,
            "conceptAssetContract": True,
            "conceptsBankCreditNotes": False,
            "icaRetainingService": False,
            "deprecitionForInflation": False,
            "pucAccount": "150815005",
            "expenseContributionstoProfessionalRiskInsurance": False,
            "billingConceptsSellingCosts": False,
            "billingConceptsFixedAssetsPropertyPlantEquipment": True,
            "ivaSaleCI": False,
            "cashBoxExcess": False,
            "saleCommissionsThirdParty": False,
            "creeRetainingService": False,
            "withholdingRetainingSale": False,
            "conceptsProductionOrders": False,
            "depreciationFixedAssetsAccount": False,
            "ivaPurchaseTradeZone": False,
            "legalizationConceptsExpensesPayable": True,
            "withholdingCREEPurchase": False,
            "name": "VIAS DE COMUNICACION",
            "paymentsForThirdParties": False,
            "accountsReceivableCashReceipt": False,
            "creditCardsVoucher": False,
            "pucClass": "1",
            "ivaCode": None,
            "ivaSaleServiceForeign": False,
            "freightPurchases": False,
            "provisionVacationExpense": False,
            "loansMembersConcepts": False,
            "icbfContributions": False,
            "baseValue": False,
            "conceptsForPayingTaxes": False,
            "purchaseReteIVA": False,
            "billingConceptsFixedAssetsDeferred": False,
            "retention": False,
            "withholdingRetainingService": False,
            "pucSubClass": "5",
            "penaltyInterestPurchases": False,
            "conceptsBankDebitNotes": False,
            "compensationExpenses": False,
            "dianDisposalOfAssetsNatPersons": False,
            "interestonLayoffProvision": False,
            "ivaSalePropertyForeign": False,
            "payrollConcepts": False,
            "accountsPayableNationalProvider": False,
            "providerAdvances": False,
            "loansFromFinancialEntity": False,
            "loansEmployeesConcepts": False,
            "conceptsCostsAndExpensesPayable": False,
            "sellerRequire": False,
            "deterioration": {
              "deteriorationPUC": None
            },
            "creditCardAccounts": False,
            "lossYear": False,
            "vacation": False,
            "reteICAOtherTaxes": False,
            "dianCommissions": False,
            "createdBy": "Administrador del Sistema",
            "payrollEntity": False,
            "foreignExchangeAccountsReceivable": False,
            "debitOrderAccounts": False,
            "yearEndClose": False,
            "industryAndCommerceTaxICA": False,
            "inventoryIncomeAdjustment": False,
            "legalizationConceptsRevolvingFund": True,
            "movingHomeBranch": False,
            "reteICASale": False,
            "billingConceptsFixedAssetsIntangibles": False,
            "ccfContributionsExpense": False,
            "valuesReceivedThirdParties": False,
            "pucId": 84789,
            "valueProduction": False,
            "partner": False,
            "otherAccountsPay": False,
            "expenseContributionsToPensionFund": False,
            "dianPurchases": False,
            "constructionContracts": False,
            "contributionsToHealthExpenses": False,
            "depositCommissionVoucher": False,
            "interestonLayoffProvisionExpense": False,
            "isDeleted": False,
            "customerAdvances": False,
            "assetUtility": False,
            "salesTaxPaidSimplifiedRegimen": False,
            "percentage": 0,
            "inventoryPieces": False,
            "accountsPayableForeignProviders": False,
            "costCenter": False,
            "withholdingTaxSalary": False,
            "accountsReceivableReport": False,
            "nonOperationalIncome": False,
            "withholdingTaxPurchase": False,
            "extralegalBenefits": False,
            "expenseContributionstotheNationalLearningService": False,
            "auxiliary1": "005",
            "otherBonus": False,
            "otherSaleByThirdParties": False,
            "nationalApprenticeshipServiceContributions": False,
            "conceptsPayableShareHoldersPartners": False,
            "nonCurrent": True,
            "assetsConsigning": False,
            "implicitInterest": False
          },
          "sectionId": 8,
          "paymentTermId": 2,
          "sourceDocumentHeaderId": None,
          "reteICABase": 0,
          "paymentReceiptId": [],
          "documentNumber": "0000000161",
          "partnerId": None
        }

        response = self.test_client.post('/api/v1/invoice_contract/',
                                     data=json.dumps(invoice_contract),
                                     content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.invoice_contract_document_number0 = response.json['documentNumber']
        self.invoice_contract_id0 = response.json['id']

        response = self.test_client.post('/api/v1/invoice_contract/',
                                     data=json.dumps(invoice_contract),
                                     content_type='application/json', headers=self.headers)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.invoice_contract_document_number1 = response.json['documentNumber']
        self.invoice_contract_id1 = response.json['id']

        response = self.request_get("", "/contract/"+str(self.contractId))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.json, {})

        self.importationValue = response.json['importationValue']
        self.activoOitem = response.json['puc']['conceptAssetContract']
        self.contractIDesc = response.json['description']
        self.contractPucId = response.json['pucId']

        self.assertEquals(response.json['contractId'], self.contractId)
        self.assertEquals(response.json['pucId'], self.contractPucId)

        legalization_contract = {
          "pucId": self.contractPucId,
          "description": self.contractIDesc,
          "documentNumber": "0000000000",
          "costCenterId": 5,
          "sourceShortWord": "LT",
          "documentDate": "2017-03-29T09:51:35.000Z",
          "contractId": self.contractId,
          "documentAffecting": [],
          "controlNumber": None,
          "importationValue": self.importationValue,
          "contract": None,
          "sourceDocumentOrigin": "LT",
          "currencyId": 4,
          "costCenter": None,
          "comments": "ninguna",
          "annuled": None,
          "divisionId": 15,
          "dependencyId": None,
          "sourceDocumentHeaderId": None,
          "exchangeRate": 0,
          "sectionId": None,
          "shortWord": "LT",
          "total": self.importationValue,
          "branchId": 14,
          "documentDetails": [
            {
              "name": "",
              "indexItem": 0,
              "balance": 0,
              "value": self.importationValue,
              "asset": {
                "isDeleted": None,
                "puc": {
                  "pucId": 84776,
                  "name": "TUBERÍAS Y EQUIPO",
                  "account": "150605005"
                },
                "sectionId": None,
                "notarialDocument": None,
                "createdBy": "ADMINISTRADOR UPDATE del Sistema",
                "creationDate": "Mon, 27 Mar 2017 14:26:08 GMT",
                "percentageSaving": 0,
                "notary": None,
                "comments": None,
                "costHour": 0,
                "responsible": None,
                "city": {
                  "department": {
                    "country": {
                      "indicative": "57",
                      "countryId": 2
                    },
                    "departmentId": 24,
                    "code": "76",
                    "name": "VALLE DEL CAUCA"
                  },
                  "indicative": "2",
                  "code": "001",
                  "cityId": 822,
                  "name": "CALI - VALLE DEL CAUCA - COLOMBIA"
                },
                "depreciationYearNIIF": 0,
                "propertyNumber": None,
                "dependencyId": None,
                "depreciationYear": 0,
                "assetId": 77,
                "percentageResidual": 0,
                "code": "8585",
                "model": None,
                "cityId": 822,
                "rentable": False,
                "branchId": 14,
                "dateNotarialDocument": "Mon, 27 Mar 2017 19:25:20 GMT",
                "imageId": None,
                "pucId": 84776,
                "engineSerial": None,
                "costCenterId": 5,
                "chassisSerial": None,
                "purchaseDate": "Mon, 27 Mar 2017 19:25:20 GMT",
                "updateBy": "ADMINISTRADOR UPDATE del Sistema",
                "landArea": 0,
                "depreciationMonth": 0,
                "builtArea": 0,
                "typeAsset": "I",
                "updateDate": "Mon, 27 Mar 2017 14:26:08 GMT",
                "netValueNIIF": 0,
                "name": "ACTIVO 8585",
                "line": None,
                "divisionId": 15,
                "state": "A",
                "depreciationMonthNIIF": 0,
                "plate": None,
                "address": None,
                "assetGroupId": None,
                "logoConvert": ""
              },
              "consultItem": True,
              "unitValue": 0,
              "assetId": 77,
              "quantity": 0,
              "code": "",
              "detailDate": "2017-03-29T09:51:35.000Z",
              "otr": "",
              "units": 0,
              "baseValue": self.importationValue
            }
          ] if self.activoOitem == 1 else [
                {
                  "size": False,
                  "costCenterId": 4,
                  "unitValue": self.importationValue,
                  "measurementUnits": [
                    {
                      "measurementUnitId": 32,
                      "name": "KILOGRAMOS                    ",
                      "code": "KGM"
                    }
                  ],
                  "und": {
                    "measurementUnitId": 32,
                    "name": "KILOGRAMOS                    ",
                    "code": "KGM"
                  },
                  "conversionFactor": 1,
                  "consumptionTaxPercent": 0,
                  "detailWarehouse": {
                    "typeWarehouse": "S",
                    "warehouseId": 6,
                    "codeComplete": "Código 002",
                    "name": "LEGAQUIMICOS MODIFICAD",
                    "code": "002"
                  },
                  "detailDate": "2017-03-29T09:51:35.000Z",
                  "ivaPurchasePUC": {
                    "pucId": 85796,
                    "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                    "percentage": 16
                  },
                  "name": "ACEITE DE AGUACATE KL",
                  "divisionId": 13,
                  "measurementUnitId": 32,
                  "color": False,
                  "withholdingICA": False,
                  "units": 1,
                  "quantity": 1,
                  "withholdingTaxPUC": {
                    "pucId": 85677,
                    "pucAccount": "236540005 COMPRAS 3.5%",
                    "percentage": 3.5
                  },
                  "itemToCompare": {
                    "size": False,
                    "consumptionPUCId": None,
                    "incomingPUC": {
                      "pucId": 86636,
                      "pucAccount": "413550005 VENTA DE QUIMICOS",
                      "percentage": 0
                    },
                    "priceListA10": 0,
                    "incomingPUCId": 86636,
                    "typeItem": "A",
                    "barCode": "",
                    "ivaPurchasePUCId": 85796,
                    "ivaPurchasePUC": {
                      "pucId": 85796,
                      "pucAccount": "240820010 IMPUESTO A LAS VENTAS PAGADO POR COMPRAS GRAVADAS 16% BIENES",
                      "percentage": 16
                    },
                    "priceListB1": None,
                    "isDeleted": False,
                    "priceList2": 0,
                    "namePOS": "ACEITE DE AGUACATE KL",
                    "orderQuantity": 0,
                    "consumptionPercentage": 0,
                    "disccountToUnitValue": False,
                    "measurementUnitId": 32,
                    "companyId": 1,
                    "purchaseIVA": {
                      "name": "GRAVADO",
                      "code": "G",
                      "ivaId": 2
                    },
                    "color": False,
                    "measurementUnit2": None,
                    "ivaSalePUC": {
                      "pucId": 85778,
                      "pucAccount": "240810010 IMPUESTO A LAS VENTAS - COBRADO POR VENTAS AL 16%",
                      "percentage": 16
                    },
                    "priceListB8": None,
                    "priceList10": None,
                    "lot": False,
                    "priceListA3": 0,
                    "addConsumptionToCost": False,
                    "lastCost": 44000,
                    "packagePrice": 0,
                    "conversionFactor2": None,
                    "listItems": [],
                    "withholdingTaxPurchasePUC": {
                      "pucId": 85677,
                      "pucAccount": "236540005 COMPRAS 3.5%",
                      "percentage": 3.5
                    },
                    "measurementUnit3Id": None,
                    "discountPercentage": 0,
                    "priceListA4": 0,
                    "companyCost": 40700,
                    "addConsumptionToPurchase": False,
                    "priceListB2": None,
                    "subInventoryGroup2Id": None,
                    "withholdingSalePercentage": 0,
                    "addIVAtoCost": False,
                    "ivaSalePUCId": 85778,
                    "percentagePurchaseIVA": 16,
                    "priceListB9": None,
                    "priceList6": 0,
                    "brandId": None,
                    "plu": "",
                    "percentageSaleIVA": 16,
                    "saleIVA": {
                      "name": "GRAVADO",
                      "code": "G",
                      "ivaId": 2
                    },
                    "imageId": None,
                    "updateDate": "Wed, 18 Dec 2013 16:21:50 GMT",
                    "measurementUnit3": None,
                    "saleIVAId": 2,
                    "priceListA8": 0,
                    "priceList3": 0,
                    "purchaseIVAId": 2,
                    "priceListA2": 0,
                    "withholdingTaxPurchasePUCId": 85677,
                    "priceListA5": 0,
                    "subInventoryGroup3Id": None,
                    "creationDate": "Tue, 10 Dec 2013 14:40:27 GMT",
                    "priceListB5": None,
                    "priceList5": 0,
                    "priceList1": 0,
                    "withholdingICA": False,
                    "photo": None,
                    "inventoryPUC": {
                      "pucId": 84706,
                      "pucAccount": "143505005 MERCANCIAS NO FABRICADAS POR LA EMPRESA",
                      "percentage": 0
                    },
                    "priceList7": None,
                    "priceListB3": None,
                    "priceListB7": None,
                    "invimaRegister": None,
                    "priceListA7": 0,
                    "subInventoryGroup1Id": None,
                    "measurementUnit": {
                      "measurementUnitId": 32,
                      "name": "KILOGRAMOS                    ",
                      "code": "KGM"
                    },
                    "averageCost": 44000,
                    "description": "",
                    "code": "AC002",
                    "createdBy": "Migracion",
                    "inventoryGroupId": 9,
                    "priceList9": None,
                    "lastPurchaseDate": "Tue, 24 Mar 2015 00:00:00 GMT",
                    "priceList4": 0,
                    "subInventoryGroups1": None,
                    "priceListA1": 0,
                    "withholdingTaxSalePUC": {
                      "pucId": 84520,
                      "pucAccount": "135515005 RETENCION EN LA FUENTE - EXENTA",
                      "percentage": 0
                    },
                    "costPUC": {
                      "pucId": 88508,
                      "pucAccount": "613550005 VENTA DE QUIMICOS",
                      "percentage": 0
                    },
                    "priceListB10": None,
                    "conversionFactor": 0,
                    "serial": False,
                    "priceList8": None,
                    "inventoryPUCId": 84706,
                    "minimumStock": 0,
                    "name": "ACEITE DE AGUACATE KL",
                    "withholdingTaxSalePUCId": 84520,
                    "costPUCId": 88508,
                    "consumptionPUC": None,
                    "inventoryGroup": {
                      "inventoryGroupId": 9,
                      "name": "COSMETICOS"
                    },
                    "updateBy": "Migracion",
                    "priceListB6": None,
                    "priceListB4": None,
                    "subInventoryGroup3": None,
                    "itemId": 25,
                    "subInventoryGroup2": None,
                    "invimaDueDate": None,
                    "measurementUnit2Id": None,
                    "reference": "",
                    "priceListA9": 0,
                    "withholdingPurchasePercentage": 3.5,
                    "providerId": None,
                    "percentageICA": 11.04,
                    "state": "A",
                    "itemDetails": [],
                    "priceListA6": 0,
                    "weight": 0
                  },
                  "baseValue": self.importationValue,
                  "indexItem": 0,
                  "itemId": 25,
                  "otr": "",
                  "detailWarehouseId": 6,
                  "consultItem": True,
                  "dueDate": None,
                  "balance": 1,
                  "dependencyId": None,
                  "code": "AC002",
                  "sectionId": 7,
                  "value": self.importationValue,
                  "badgeValue": 44000
                }
              ]
        }

        # Envio la creacion del avance sin short word
        legalization_contract["shortWord"] = None
        response = self.request_post(legalization_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        legalization_contract["shortWord"] = "XY"
        response = self.request_post(legalization_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        legalization_contract["shortWord"] = "LT"
        response = self.request_post(legalization_contract)
        response.json = json.loads(response.data.decode("utf-8"))

        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        legalization_contract['documentDetails'][0]['value'] = self.importationValue
        # Crea un compra de item con un peso de diferencia en el debit
        response = self.request_post(legalization_contract)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un compra de item correcto con valor exacto
        legalization_contract['documentDetails'][0]['value'] = self.importationValue
        response = self.request_post(legalization_contract)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']

        # Consulta el compra de item
        response = self.request_get('', '/search?branch_id=14&short_word=LT&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        legalization_contract2 = response.json
        response = self.request_put("", "/"+str(self.id)+"/preview")
        # *********************UPDATE*************************
        #  Realizo una copia del compra de item consultado
        purchase_copy = copy.deepcopy(legalization_contract2)
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
        purchase_copy['documentDetails'][0]['value'] = self.importationValue
        # Realiza un cambio del comentario
        purchase_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(purchase_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn("ok", response.json)

        purchase_copy['documentDetails'][0]['value'] = self.importationValue
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

        response = self.request_delete("", "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertEqual('LEGALIZATION NOT FOUND', response.json['message'].upper(),
                         'incorrect response by bad request')

        response = self.request_delete("", "/" + str(self.contractId))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.invoice_contract_id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)

        response = self.request_delete("", "/" + str(self.invoice_contract_id0))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta de eliminacion
        self.assertIn("message", response.json)


