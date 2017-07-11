# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 10-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from datetime import *
from ..payment_accounting import PaymentAccounting

class GiftVoucherAccounting(object):

    def __init__(self, document_header):
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

    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        try:
            self.ret_value.append(self.customer_gift_voucher(document_header, "C"))
            # Pago de la Tarjeta
            p_accounting = PaymentAccounting(document_header)
            p_accounting.execute_payment(document_header=document_header, payment_receipt=payment_receipt,
                                         ret_value=self.ret_value, account_type="D")
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def add_days(self, date, days):
        for i in range(days):
            date += timedelta(days=1)

        return date

    def customer_gift_voucher(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos del encabezado

        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.giftVoucher][0]
        accounting_record.crossPrefix = document_header.prefix
        # //accounting_record.crossDocument = document_header.documentNumber
        accounting_record.crossDocument = "RENUMBER"
        accounting_record.dueDate = self.add_days(document_header.documentDate, document_header.termDays)

        if account_type == "C":
            accounting_record.credit = document_header.total
        else:
            accounting_record.debit = document_header.total
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"

        # //accounting_record.crossDocumentHeader = document_header
        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId

        return accounting_record