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
handled advance_thirds
"""
class AdvanceThirdTest(unittest.TestCase):
    """
    This Class is a  Test Case for advance_thirds API class
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
        """Sent get request to #/api/v1/advance_thirds# with advance_thirds data values

        :param data: advance_thirds data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/advance_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/advance_thirds# with advance_thirds data values

        :param data: advance_thirds data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/advance_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/advance_thirds# with advance_thirds data values

        :param data: advance_thirds data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/advance_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/advance_thirds# with advance_thirds data values

        :param data: advance_thirds data
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/advance_thirds'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_get_advance_third(self):
        """
        This function test get a Advance Third according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        # """
        response = self.request_get('', '/1') # envio la peticion
        response.json = json.loads(response.data.decode("utf-8")) # convierte a json object
        # validacion de la clave en la respuesta
        self.assertTrue("message" in response.json, 'incorrect response by correct request')

        response = self.request_get('', '/0') # envio la peticion con un id que no va existir
        # not found en la respuesta
        self.assertEqual(response.status_code, 404, 'incorrect response by bad request')

    def test_get_advance_thirds_search(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
         ** Third test generate error in server
        """
        response = self.request_get("","/")
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200,"")

        advance_third = response.json['data'][-1]

        # envio la peticion con argumentos invalidos
        response = self.request_get("", "/search?search=BLAN Hola")
        self.assertEquals(response.status_code, 400, 'incorrect response by correct request')

        # envio la peticion con argumentos validos
        response = self.request_get('', '/search?branch_id=14&short_word=AP&document_number=0000000066')

        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)

        # envio la peticion con short word que no existe
        response = self.request_get('', '/search?branch_id=14&short_word=XXXX&document_number='+advance_third['documentNumber'])

        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response.status_code, {})

        # uno correcto para ver lo que se obtiene
        response = self.request_get('', '/search?branch_id=14&short_word=AP&document_number=' + advance_third['documentNumber'])
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
        response = self.request_get("","/" + str(advance_third['documentHeaderId']))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response, {})
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)

        response = self.request_get("", "/" + str(advance_third['documentHeaderId'])+"/preview?format=P")
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
        advance_third = {
              "branchId": 14,
              "comments": "ESTA ES UNA PRUEBA",
              "costCenter": {
                "branchId": 14,
                "code": "00001",
                "costCenterId": 4,
                "divisions": [
                  {
                    "code": "00001",
                    "costCenterId": 4,
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
                        "dependencies": [],
                        "divisionId": 13,
                        "isDeleted": 0,
                        "name": "F",
                        "puc": None,
                        "pucId": None,
                        "sectionId": 7
                      }
                    ]
                  },
                  {
                    "code": "00002",
                    "costCenterId": 4,
                    "divisionId": 14,
                    "isDeleted": 0,
                    "name": "VENTAS",
                    "puc": {
                      "account": "730000000 COSTOS DE PRODUCCIÓN - COSTOS INDIRECTOS",
                      "percentage": 0,
                      "pucId": 89100
                    },
                    "pucId": 89100,
                    "sections": []
                  }
                ],
                "isDeleted": 0,
                "name": "LEGAQUIMICOS"
              },
              "costCenterId": 4,
              "currency": {
                "code": "COP",
                "currencyId": 4,
                "isDeleted": 0,
                "name": "PESO COLOMBIANO",
                "symbol": "$"
              },
              "currencyId": 4,
              "documentDate": "Thu, 24 Apr 2016 00:00:00 GMT",
              "exchangeRate": 1,
              "paymentReceipt": {
                "paymentDetails": [{
                    "balance": 15568990.11,
                    "paymentType": "EF",
                    "state": 1,
                    "value": 100000
                  },{
                    "balance": 2229469.51,
                    "bankAccount": {
                      "accountNumber": "1333979335",
                      "accountType": "T",
                      "bank": {
                        "financialEntityId": 5,
                        "name": "BANCOLOMBIA    - EDIFICIO LARA"
                      },
                      "bankAccountId": 7,
                      "bankId": 5,
                      "bankingTax": 0,
                      "branchId": 14,
                      "cardType": {
                        "financialEntityId": 9,
                        "name": "AMERICAN EXPRESS   "
                      },
                      "cardTypeId": 9,
                      "creditCapacity": 1000,
                      "expirationDate": "Wed, 14 Aug 2013 00:00:00 GMT",
                      "isDeleted": 0,
                      "office": "EDIFICIO LARA",
                      "openingDate": "Wed, 20 Feb 2008 00:00:00 GMT",
                      "overdraft": 0,
                      "owner": "LEGAQUIMICOS SAS modificada",
                      "puc": {
                        "account": "112005005",
                        "name": "BANCOS",
                        "pucId": 84135
                      },
                      "pucId": 84135
                    },
                    "bankAccountId": 7,
                    "beneficiary": "CODENSA S.A. ESP",
                    "paymentType": "TR",
                    "state": 1,
                    "value": 200000
                  },{
                    "balance": 23487580.24,
                    "bankAccount": {
                      "accountNumber": "54545454",
                      "accountType": "C",
                      "bank": {
                        "financialEntityId": 5,
                        "name": "BANCOLOMBIA    - EDIFICIO LARA"
                      },
                      "bankAccountId": 8,
                      "bankId": 5,
                      "bankingTax": 0,
                      "branchId": 14,
                      "creditCapacity": 0,
                      "expirationDate": "Tue, 13 Oct 2015 11:47:15 GMT",
                      "isDeleted": 0,
                      "office": "EDIFICIO LARA",
                      "openingDate": "Tue, 13 Oct 2015 11:47:15 GMT",
                      "overdraft": 11120,
                      "owner": "LEGAQUIMICOS SAS",
                      "puc": {
                        "account": "111005005",
                        "name": "MONEDA NACIONAL",
                        "pucId": 84125
                      },
                      "pucId": 84125
                    },
                    "bankAccountId": 8,
                    "bankCheckBook": {
                      "bankAccountId": 8,
                      "bankCheckBookId": 6,
                      "finalCheck": "738350",
                      "initialCheck": "737851",
                      "isDeleted": 0,
                      "lastConsecutive": 738014,
                      "prefix": None,
                      "state": True
                    },
                    "bankCheckBookId": 6,
                    "beneficiary": "ASEGURADORA SOLIDARIA DE COLOMBIA",
                    "paymentType": "CH",
                    "state": 1,
                    "value": 200000
                  }]
              },
              "provider": {
                "address1": "BOGOTA",
                "address2": "",
                "branch": "001",
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
                "creditCapacity": 0,
                "fax": None,
                "isDeleted": 0,
                "isLaw1527": False,
                "isMain": True,
                "name": "PRINCIPAL",
                "phone": "5601515",
                "providerId": 286,
                "state": "A",
                "term": 0,
                "thirdPartyId": 1704,
                "zipCode": ""
              },
              "providerId": 286,
              "puc": {
                "aCurrent": True,
                "account": "30",
                "accountPayableLayoff": False,
                "accountsPayableForeignProvider": False,
                "accountsPayableForeignProviders": False,
                "accountsPayableHolidays": False,
                "accountsPayableNationalProvider": False,
                "accountsPayableReport": False,
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
                "billingConceptsContractsCostsExpensesPayable": False,
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
                "className": "ACTIVOS FINANCIEROS MEDIDOS AL COSTO AMORTIZADO",
                "companyId": 1,
                "compensation": False,
                "compensationExpenses": False,
                "conceptAssetContract": False,
                "conceptInventoryContract": False,
                "conceptsAbroadProviderPayment": True,
                "conceptsBankCreditNotes": False,
                "conceptsBankDebitNotes": False,
                "conceptsCostsAndExpensesPayable": True,
                "conceptsForPayingTaxes": False,
                "conceptsIndirectCostsManufacturing": False,
                "conceptsNationalProviderPayment": True,
                "conceptsPayableShareHoldersPartners": True,
                "conceptsPaymentsOtherThirdParties": True,
                "conceptsProductionOrders": False,
                "constructionContracts": False,
                "consumptionTax": False,
                "contributionsExpenseDifferenceInSOI": False,
                "contributionsHealth": False,
                "contributionsToHealthExpenses": False,
                "costCenter": False,
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
                "forwardConceptsEmployeesLegalization": False,
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
                "legalizationConceptsRevolvingFund": False,
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
                "name": "A PROVEEDORES",
                "nationalApprenticeshipServiceContributions": False,
                "nature": "D",
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
                "payrollConcepts": True,
                "payrollEntity": False,
                "penaltyInterestPurchases": False,
                "pensionFundContributions": False,
                "pensionSolidarityFundContributions": False,
                "percentage": 0,
                "premiumsPayable": False,
                "productionExpenseLabor": False,
                "productionSpendingMachineHours": False,
                "provider": True,
                "providerAdvances": True,
                "provisionBonus": False,
                "provisionBonusExpense": False,
                "provisionCancelHolding": False,
                "provisionHolding": False,
                "provisionVacation": False,
                "provisionVacationExpense": False,
                "provisionlayoffs": False,
                "provisionlayoffsExpense": False,
                "pucClass": "1",
                "pucId": 84437,
                "pucSubClass": "3",
                "pucs": [],
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
                "subAccount": "05",
                "subAccountName": "DEUDORES - ANTICIPOS Y AVANCES",
                "subsistenceFundContributions": False,
                "taxExpenseIndustryCommerce": False,
                "technicalServiceFromAbroadWithoutAgreement": False,
                "third": False,
                "thirdRequiredDCNB": False,
                "typesCreditInventoryAdjustment": False,
                "typesDebitInventoryAdjustment": False,
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
              "pucId": 84437,
              "accountsBackward": 0,
              "total":500000
            }

        # Envio la creacion del avance sin short word
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 400)

        # Envio la creacion del avance con short word erroneo
        advance_third["shortWord"] = "XY"
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        self.assertIn("error", response.json)
        self.assertIn("message", response.json)
        self.assertEquals(response.status_code, 500)

        # Agrega el short word correcto
        advance_third["shortWord"] = "AP"
        # Crea un avance de tercero con un peso de diferencia en el credito
        advance_third['total'] = 500000.1
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0 = response.json['documentNumber']
        self.id0 = response.json['id']

        # Restaura el valor del avance
        advance_third['total'] = 500000
        advance_third['paymentReceipt']['paymentDetails'][2]['value'] = 200000.1
        # Crea un avance de tercero con un peso de diferencia en el debito
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))
        # Obtengo los datos para despues eliminar
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number0a = response.json['documentNumber']
        self.id0a = response.json['id']

        # Crea un avance de tercero correcto con valor exacto
        advance_third['total'] = 500000
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number = response.json['documentNumber']
        self.id = response.json['id']
        # TODO: la moneda por defecto podria no ser el peso
        # Guarda la moneda del objeto, en essta caso por defecto es PESOS Colombianos
        currency = advance_third['currency']
        # FIXME: podria consultar las monedas y obtener una
        # Establece una moneda distinta
        currency2 = {"code": "USD",
                      "currencyId": 2,
                      "isDeleted": 0,
                      "name": "DÓLAR AMERICANO",
                      "symbol": "$"}

        advance_third["currency"] = currency2
        advance_third["currencyId"] = 2
        # Crea el avance de tercero con una moneda extranjera
        response = self.request_post(advance_third)
        response.json = json.loads(response.data.decode("utf-8"))
        # Guarda los datos de este avance para la posterior eliminacion
        self.assertIn("documentNumber", response.json)
        self.assertIn("id", response.json)
        self.document_number2 = response.json['documentNumber']
        self.id2 = response.json['id']
        # Reestablece la moneda actual
        advance_third["currency"] = currency
        advance_third["currencyId"] = 4

        # Consulta el avance de tercero
        response = self.request_get('', '/search?branch_id=14&short_word=AP&document_number=' + self.document_number)
        self.assertEquals(response.status_code, 200)
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertNotEquals(response.json, {})
        # Verifico algunos de las claves de la respuesta
        self.assertIn("paymentReceipt", response.json)
        self.assertIn("total", response.json)
        self.assertIn("documentNumber", response.json)
        self.assertIn("division", response.json)
        self.assertIn("puc", response.json)

        advance_third2 = response.json
        # *********************UPDATE*************************
        #  Realizo una copia del avance de tercero consultado
        advance_copy = copy.deepcopy(advance_third2)
        # Cambio el total
        advance_copy['total'] = 800000
        # Envio a actulizar el avance de tercero
        response = self.request_put(advance_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("message", response.json)
        self.assertIn("error", response.json)
        self.assertIn("status", response.json)

        # Espero un error por descuadre...
        # FIXME: deberia establecer un error particular para este caso
        self.assertEquals(response.status_code, 500)
        self.assertIn("message", response.json)
        # Establece el valor correcto al avance de tercero
        advance_copy['total'] = 500000
        # Realiza un cambio del comentario
        advance_copy['comments'] = "Este es el test"
        # Peticion de actualizado para este avance
        response = self.request_put(advance_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Copio el ultimo de los detalles de pago
        payment_detail = advance_copy['paymentReceipt']['paymentDetails'][2]
        # Elimino esta posicion del arreglo
        del advance_copy['paymentReceipt']['paymentDetails'][2]
        # Cambio el valor total del avance
        advance_copy['total'] = 300000
        # Actualiza el avance de tercero
        response = self.request_put(advance_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Simula un nuevo detalle de pago con base al eliminado
        payment_detail.pop('paymentDetailId', None)
        advance_copy['paymentReceipt']['paymentDetails'].append(payment_detail)
        # Cambio el valor total del avance
        advance_copy['total'] = 500000
        advance_copy['comments'] = "Este es el test"
        # Actualizo nuevamente
        response = self.request_put(advance_copy, "/" + str(self.id))
        response.json = json.loads(response.data.decode("utf-8"))
        # Respuesta
        self.assertIn("ok", response.json)

        # Cambio el estado del documento
        advance_copy['annuled'] = 1
        # Envio a actualizar
        response = self.request_put(advance_copy, "/" + str(self.id))
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

        self.assertEqual('ADVANCE THIRD NOT FOUND', response.json['message'].upper(), 'incorrect response by bad request')