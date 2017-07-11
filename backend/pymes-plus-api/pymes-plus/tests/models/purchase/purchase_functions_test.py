#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
# app
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
import unittest
from datetime import datetime
from app.models.accounting.purchase.purchase_functions import PurchaseFunctions
from app.models.referential.puc import PUC
from app.models import DocumentHeader, DocumentDetail, Contract, Provider
"""
This module shows various methods and function by allow
handled asset
"""
class PurchaseFunctionsTest(unittest.TestCase):
    """
    This Class is a  Test Case for Purchase Functions
    """
    def setUp(self):
        self.document_header = {
          "shortWord": "RP",
          "sourceShortWord":"RP",
          "anNoneed": False,
          "dayClosed": False,
          "termDays": 0,
          "contractId": 1,
          "providerId": 1,
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
              "costCenterId": 1,
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
              "itemId": 1,
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
          "withholdingTaxPUCId": 85677,
          "dependencyId": 6,
          "reteIVAValue": 200000,
          "reteICAValue": 200000,
          "retentionValue": 200000,
          "insurance": 200000,
          "freight": 200000,
          "interest": 200000,
          "exchangeRate": 1,
          "sourceDocumentOrigin": "1",
          "paymentBy": "1",
          "providerId": 1,
          "branchId": 1
        }
        self.detail = self.document_header['documentDetails'][0]
        document_header = DocumentHeader()
        document_header.import_data(self.document_header)
        document_detail = DocumentDetail()
        self.detail = document_detail.import_data(self.detail)
        self.document_header = document_header
        self.document_header.provider = Provider.get_by_id(self.document_header.providerId)
        self.document_header.contract =  Contract.get_by_id(1)
        self.document_header.contractId = self.document_header.contract.contractId

        self.list_puc =None
        self.default_value =None
        self.general_parameter =None
        self.list_puc = PUC.get_list_puc(1)
        self.list_puc = [p for p in self.list_puc]
        self.p_functions = PurchaseFunctions(self.document_header, list_puc=self.list_puc)

    def test_add_days(self):
        date = datetime(2000, 1, 20)
        days = 12
        date_result = self.p_functions.add_days(date, days)
        self.assertEquals(date_result, datetime(2000, 2, 1))

    def test_accounting_record_iva(self):
        ar = self.p_functions.IVA(self.document_header, 2, "C")
        ar = self.p_functions.IVA(self.document_header, 2, "D")

    def test_accounting_record_contract_provider(self):
        self.document_header.contract =  Contract.get_by_id(1)
        self.document_header.contractId = self.document_header.contract.contractId

        ar = self.p_functions.contract_provider(self.document_header, 2, "C")
        ar = self.p_functions.contract_provider(self.document_header, 2, "D")

    def test_accounting_record_purchase_discount(self):
        ar = self.p_functions.purchase_discount(self.document_header, 2, 2, "C")
        ar = self.p_functions.purchase_discount(self.document_header, 2, 2, "D")

    def test_accounting_record_purchase_other_discount(self):
        ar = self.p_functions.purchase_other_discount(self.document_header, 2, "C")
        ar = self.p_functions.purchase_other_discount(self.document_header, 2, "D")

    def test_accounting_record_interest_expense(self):
        ar = self.p_functions.interest_expense(self.document_header, "C")
        ar = self.p_functions.interest_expense(self.document_header, "D")

    def test_accounting_record_insurance_expense(self):
        ar = self.p_functions.insurance_expense(self.document_header, "C")
        ar = self.p_functions.insurance_expense(self.document_header, "D")

    def test_accounting_record_freight_expense(self):
        ar = self.p_functions.freight_expense(self.document_header, "C")
        ar = self.p_functions.freight_expense(self.document_header, "D")

    # def test_accounting_record_detail_iva(self):
    #     ar = self.p_functions.detail_iva(self.document_header, self.detail, 2, 2, 2, 2, "C")
    #     ar = self.p_functions.detail_iva(self.document_header, self.detail, 2, 2, 2, 2, "D")

    # def test_accounting_record_purchase_consumptionTax(self):
    #     ar = self.p_functions.purchase_consumptionTax(self.document_header, self.detail, 2, 2, 2, "C")
    #     ar = self.p_functions.purchase_consumptionTax(self.document_header, self.detail, 2, 2, 2, "D")

    # def test_accounting_record_detail_withholdingTax(self):
    #     ar = self.p_functions.detail_withholdingTax(self.document_header, self.detail, 2, 2, 2, "C")
    #     ar = self.p_functions.detail_withholdingTax(self.document_header, self.detail, 2, 2, 2, "D")

    def test_accounting_record_provider_payable(self):
        ar = self.p_functions.provider_payable(self.document_header, self.detail, 2, 2, 2, "C")
        ar = self.p_functions.provider_payable(self.document_header, self.detail, 2, 2, 2, "D")

    # def test_accounting_record_purchase_inventory(self):
    #     ar = self.p_functions.purchase_inventory(self.document_header, self.detail, 2, "C")
    #     ar = self.p_functions.purchase_inventory(self.document_header, self.detail, 2, "D")

    # def test_accounting_record_sale_third_party(self):
    #     ar = self.p_functions.sale_third_party(self.document_header, self.detail, 2, "C")
    #     ar = self.p_functions.sale_third_party(self.document_header, self.detail, 2, "D")

    def test_accounting_record_rete_ica(self):
        ar = self.p_functions.rete_ica(self.document_header, "C")
        ar = self.p_functions.rete_ica(self.document_header, "D")

    def test_accounting_record_rete_iva(self):
        ar = self.p_functions.rete_iva(self.document_header, "C")
        ar = self.p_functions.rete_iva(self.document_header, "D")

    def test_accounting_record_assumed_iva(self):
        ar = self.p_functions.assumed_iva(self.document_header, "C")
        ar = self.p_functions.assumed_iva(self.document_header, "D")

    def test_accounting_record_withholding_tax(self):
        self.document_header.withholdingTaxPUC = [p for p in self.list_puc if p.withholdingTaxPurchase][0]
        ar = self.p_functions.withholding_tax(self.document_header, "C")
        ar = self.p_functions.withholding_tax(self.document_header, "D")

    # def test_accounting_record_withholding_cree(self):
    #     ar = self.p_functions.withholding_cree(self.document_header, "C")
    #     ar = self.p_functions.withholding_cree(self.document_header, "D")

    # def test_accounting_record_direct_iva(self):
    #     ar = self.p_functions.direct_iva(self.document_header, "C")
    #     ar = self.p_functions.direct_iva(self.document_header, "D")

    def test_accounting_record_other_retentions(self):
        ar = self.p_functions.other_retentions(self.document_header, "C")
        ar = self.p_functions.other_retentions(self.document_header, "D")

    def test_accounting_record_expenses_puc(self):
        puc = [p for p in self.list_puc if p.insurance][0]
        ar = self.p_functions.expenses_puc(puc,self.document_header, self.document_header.costCenter,
                                           self.document_header.division, self.document_header.section,
                                           self.document_header.dependency)
        ar = self.p_functions.expenses_puc(puc, self.document_header, self.document_header.costCenter,
                                           self.document_header.division, self.document_header.section,
                                           self.document_header.dependency)


