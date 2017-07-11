# coding=utf-8
#########################################################
# Advance Third Accounting Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ....utils.math_ext import _round
from ..payment_accounting import PaymentAccounting
from ..accounting_record import AccountingRecord

class AdvanceThirdAccounting(object):
    """

    """
    def __init__(self, document_header):
        """
        initialize all variables
        :param document_header:
        """
        # Obtiene lista de puc por comany id
        self.list_puc = PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]
        self.total_records = 0

        # Obtiene los valores por defecto por branch id
        self.default_value = DefaultValue.get_default_value_by_branch_id(document_header.branchId)

        # Obtiene los valores generales de la app
        self.general_parameter = GeneralParameter.get_general_parameter()

        # Obtiene valor de decimales de default values
        self.round_decimals = self.default_value.valueDecimals

        self.record_number = 1
        self.sum_value = 0
        self.total_value = 0
        self.over_cost = 0
        self.discount = 0
        self.discount2 = 0
        self.expenses = 0
        self.total_discount = 0
        self.total_discount2 = 0
        self.total_cost = 0
        self.expenses = 0
        self.ret_value = []

    def do_account(self, document_header, payment_receipt):
        p_accounting = PaymentAccounting(document_header)
        accounting_record = self.provider_advance(document_header)
        self.ret_value.append(accounting_record)
        p_accounting.execute_payment(document_header=document_header,
                                          payment_receipt=payment_receipt,
                                          ret_value=self.ret_value)
        return self.ret_value

    def provider_advance(self, document_header, account_type="D"):
        accounting_record = AccountingRecord()
        # Encabezado
        accounting_record.branch = document_header.branch
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenter = document_header.costCenter
        accounting_record.division = document_header.division
        accounting_record.section = document_header.section
        accounting_record.dependency = document_header.dependency
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = document_header.controlNumber
        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.provider = document_header.provider
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = "PR"
        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customer = document_header.customer
            accounting_record.allThirdId = document_header.customer.customerId
            accounting_record.allThirdType = "CU"
        if document_header.employee:
            accounting_record.mainThirdId = document_header.employee.thirdPartyId
            accounting_record.employee = document_header.employee
            accounting_record.allThirdId = document_header.employee.employeeId
            accounting_record.allThirdType = "EM"
        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThird = document_header.otherThird
            accounting_record.allThirdId = document_header.otherThird.otherThirdId
            accounting_record.allThirdType = "OT"
        if document_header.partner:
            accounting_record.mainThirdId = document_header.partner.thirdPartyId
            accounting_record.partner = document_header.partner
            accounting_record.allThirdId = document_header.partner.partnerId
            accounting_record.allThirdType = "PA"
        if document_header.third:
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"
        accounting_record.puc = document_header.puc
        if document_header.currencyId != self.default_value.currencyId:
            accounting_record.foreignCurrency = _round(document_header.total / document_header.exchangeRate, 2)
        if account_type is "D":
            accounting_record.debit = document_header.total
        else:
            accounting_record.credit = document_header.total
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record


