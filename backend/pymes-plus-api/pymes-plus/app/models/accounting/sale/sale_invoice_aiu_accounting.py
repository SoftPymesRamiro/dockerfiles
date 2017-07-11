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
from ...referential.branch import Branch
from ...referential.company import Company
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from datetime import *
from ..payment_accounting import PaymentAccounting
from .sale_functions import SaleFunctions
from ....utils.math_ext import _round

class SaleAIUAccounting(object):

    def __init__(self, document_header):
        # Obtiene lista de puc por comany id
        self.list_puc = PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]
        self.total_records = 0

        # Obtiene los valores por defecto por branch id
        self.default_value = DefaultValue.get_default_value_by_branch_id(document_header.branchId)
        self.selected_branch = Branch.get_branch_by_id(document_header.branchId)
        # self.selected_branch.company = Company.get_company_by_id(self.selected_branch.companyId)
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
        self.s_functions = SaleFunctions(document_header, self.list_puc, self.default_value, self.general_parameter)

    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        """
        Create accounting records
        :param document_header: document properties and a. i. u. datafinantialEntity
        :param document_details: details properties, can be several details
        :param payment_receipt: payment data
        :return:
        """
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            # Recorrido de detalles
            if self.total_records > 0:
                total_disccount2 = 0
                for detail in document_details:
                    self.discount2 = 0 if document_header.subtotal == 0 else _round(
                        float(document_header.disccount2Value) * (float(detail.value) / document_header.subtotal),
                        self.round_decimals)

                    if detail == document_details[-1]:
                        self.discount2 = document_header.disccount2Value - total_disccount2
                    # Concepto de income concept
                    self.ret_value.append(self.sales_income_concept(document_header=document_header,
                                                                    document_detail=detail,
                                                                    round_decimals=self.round_decimals,
                                                                    account_type='C'))
                    # Impuesto al Consumo
                    if document_header.consumptionTaxPercent and document_header.consumptionTaxPercent > 0:
                        self.ret_value.append(self.purchase_consumptionTaxFS(document_header=document_header,
                                                                             document_detail=detail,
                                                                             round_decimals=self.round_decimals,
                                                                             account_type='C'))
                    # // IVA en Ventas
                    if detail.baseValue> 0 and detail.value > 0:
                        self.ret_value.append(self.detail_iva(document_header=document_header,
                                                              document_detail=detail, overcost=0, disccount=0,
                                                              disccount2 = self.discount2,
                                                              round_decimals=self.round_decimals,
                                                              account_type='C'))
                    # //ICA en Ventas
                    if detail.icaPercent > 0 and detail.value > 0:
                        self.ret_value.append(self.sales_ica_tax(document_header=document_header,
                                                               document_detail=detail,
                                                               round_decimals=self.round_decimals,
                                                               account_type='C'))
                        self.ret_value.append(self.sales_ica_expense(document_header=document_header,
                                                                   document_detail=detail,
                                                                   round_decimals=self.round_decimals,
                                                                   account_type='D'))
                    # // Retefuente en Ventas
                    if detail.withholdingTax > 0 and detail.value > 0:
                        self.ret_value.append(self.detail_withholdingTax(document_header=document_header,
                                                                        document_detail=detail, overcost=0,
                                                                        discount=0,
                                                                        discount2 = self.discount2,
                                                                        round_decimals=self.round_decimals,
                                                                        account_type='D'))
                        if self.selected_branch.company.selfRetainingRete:
                            self.ret_value.append(self.self_detail_withholdingTax(document_header=document_header,
                                                                                document_detail=detail, overcost=0,
                                                                                discount=0,
                                                                                disccount2 = self.discount2,
                                                                                round_decimals=self.round_decimals,
                                                                                account_type='C'))
            # Calculo de TOTALES
            if document_header.ivaBase and document_header.ivaBase > 0 and document_header.ivaPUC is \
                    not None and document_header.ivaValue > 0:
                self.ret_value.append(self.s_functions.IVA(document_header, self.round_decimals, 'C'))
            # Otros Descuentos
            if document_header.disccount2Value > 0:
                self.ret_value.append(self.s_functions.other_discount(document_header, self.round_decimals, 'D'))
            # Fletes
            if document_header.freight and document_header.freight > 0:
                self.ret_value.append(self.s_functions.sales_freight(document_header, self.round_decimals, 'C'))
            # ReteICA
            if document_header.reteICAValue and document_header.reteICAValue > 0:
                self.ret_value.append(self.s_functions.rete_ica(document_header=document_header,
                                                               account_type="D"))
                # // Si es Autoretenedor de ICA
                if self.selected_branch.company.selfRetainingICA:
                    self.ret_value.append(self.self_rete_ica(document_header=document_header,
                                                             account_type="C"))
            # ReteIVA
            if document_header.reteIVAValue > 0:
                self.ret_value.append(self.s_functions.rete_iva(document_header=document_header,
                                                                account_type="D"))
            # Retención CREE
            if document_header.valueCREE > 0:
                self.ret_value.append(self.s_functions.withholding_cree(document_header, "D"))

                if (self.selected_branch.company.selfRetainingRete or
                        (self.selected_branch.company.selfRetainingCREE and
                                 document_header.documentDate >= self.s_functions.dateCree1828)):
                    self.ret_value.append(self.self_withholdingCREE(document_header, "C"))
            # Propina
            if document_header.tipValue > 0:
                self.ret_value.append(self.s_functions.tip(document_header, self.round_decimals, 'C'))

                # Ajuste al  peso
            if document_header.adjustment is not None:
                if document_header.adjustment < 0:
                    self.ret_value.append(
                        self.s_functions.adjustment_expense(document_header, document_header.adjustment, 'D'))
                else:
                    self.ret_value.append(
                        self.s_functions.adjustment_income(document_header, document_header.adjustment, 'C'))

                    # Cambio
            if document_header.cash and document_header.cash > 0:
                self.ret_value.append(self.s_functions.cash_deposit(document_header, document_header.cash, 'C'))
            if document_header.paymentTerm.needTermDays:
                # Pago a CREDITO
                self.ret_value.append(self.customer_receivable(document_header, payment_receipt=None,
                                                               payment_detail=None, account_type='D'))
            elif document_header.paymentTerm.quota:
                # Pago a cuotas
                if payment_receipt.firstValue > 0:
                    self.ret_value.append(self.customer_receivable(document_header=document_header,
                                                                   payment_receipt=payment_receipt,
                                                                   payment_detail=None,
                                                                   account_type='D'))

                for payment_detail in payment_receipt.paymentDetails:
                    self.ret_value.append(
                        self.customer_receivable(document_header=document_header, payment_receipt=None,
                                                 payment_detail=payment_detail, account_type='D'))
            else:
                # Pago de contado
                p_accounting = PaymentAccounting(document_header)
                p_accounting.execute_payment_sales(document_header=document_header,
                                                   payment_receipt=payment_receipt,
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

    def detail_iva(self,document_header=None, document_detail=None, overcost=0, disccount=0,
                   disccount2 = None, round_decimals=None, account_type='C'):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.allThirdId = accounting_record.mainThirdId if accounting_record.mainThirdId is not None \
            else document_header.costCenter.branch.branchId
        accounting_record.allThirdType = 'TH' if accounting_record.mainThirdId is not None else 'BR'
        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.ivaPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.baseValue
        if account_type == "C":
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.iva / 100, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.iva / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sales_ica_tax(self,document_header=None,document_detail=None,round_decimals=None, account_type='C'):
        accounting_record = AccountingRecord()
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
        accounting_record.businessAgentId = document_header.businessAgentId
        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.puc = [p for p in self.list_puc if p.industryAndCommerceTaxICA][0]
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = _round((document_detail.value -
                                              _round(document_detail.value * document_detail.disccount / 100,
                                                                    round_decimals)), round_decimals)
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue = _round((accounting_record.baseValue - _round(
                document_detail.value * document_header.disccount2 / 100, round_decimals)), round_decimals)

        accounting_record.percentage = document_detail.icaPercent
        if account_type == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.icaPercent / 1000,
                                              round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.icaPercent / 1000,
                                             round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sales_ica_expense(self, document_header=None,document_detail=None,round_decimals=None,account_type='D'):
        accounting_record = AccountingRecord()
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
        accounting_record.businessAgentId = document_header.businessAgentId
        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.puc = [p for p in self.list_puc if p.taxExpenseIndustryCommerce][0]
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = _round((document_detail.value - _round(document_detail.value *
                                                                             document_detail.disccount / 100,
                                                                    round_decimals)), round_decimals)
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue = _round((accounting_record.baseValue -
                                                  _round(document_detail.value * document_header.disccount2 / 100,
                                                         round_decimals)), round_decimals)
        accounting_record.percentage = document_detail.icaPercent
        if account_type == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.icaPercent / 1000,
                                              round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.icaPercent / 1000,
                                             round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def detail_withholdingTax(self,document_header=None,document_detail=None, overcost=0, discount=0,
                              discount2 = None,round_decimals=None,account_type='D'):
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdParty.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.withholdingTaxPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.baseValue
        if not document_header.overCostTaxBase:
            accounting_record.baseValue = _round(document_detail.baseValue - discount, round_decimals)
        accounting_record.percentage = document_detail.withholdingTax
        if account_type == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def self_detail_withholdingTax(self, document_header=None, document_detail=None, overcost=0,
                                   discount=0, disccount2 = None, round_decimals=None, account_type='C'):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.withholdingRetainingSale][0]
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.baseValue
        if not document_header.overCostTaxBase:
            accounting_record.baseValue = _round(document_detail.baseValue - discount, round_decimals)
        accounting_record.percentage = document_detail.withholdingTax
        if account_type == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100,
                                              round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100,
                                             round_decimals)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sales_income_concept(self, document_header=None, document_detail=None,
                             round_decimals=None, account_type=None):
        """

        :param document_header:
        :param document_detail:
        :param decimal_value:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()
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
        accounting_record.businessAgentId = document_header.businessAgentId

        # //Datos de detalle
        accounting_record.pucId = document_detail.pucId
        if account_type == "C":
            accounting_record.credit = _round(document_detail.value -
                                              _round(document_detail.value *
                                                     float(document_detail.disccount) / 100, round_decimals), round_decimals)
        else:
            accounting_record.debit = _round(document_detail.value -
                                             _round(document_detail.value *
                                                    float(document_detail.disccount) / 100, round_decimals), round_decimals)

        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = "CU"
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def purchase_consumptionTaxFS(self, document_header=None, document_detail=None,
                                  round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()

        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.allThirdId = document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId

        # //Datos de detalle
        accounting_record.baseValue = float(document_header.consumptionTaxBase)
        accounting_record.percentage = float(document_header.consumptionTaxPercent)
        accounting_record.puc = (document_header.consumptionTaxPUC)

        if account_type == "C":
            accounting_record.credit = _round(accounting_record.baseValue * (accounting_record.percentage / 100), round_decimals)
        else:
            accounting_record.debit =_round(accounting_record.baseValue * (accounting_record.percentage / 100), round_decimals)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def self_rete_ica(self, document_header=None, account_type=None):
        """

        :param document_header:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()

        # //Datos de Encabezado
        accounting_record.branch = document_header.branch
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.puc = [p for p in self.list_puc if p.icaRetainingSale][0]
        if document_header.overCostTaxBase and document_header.overCost > 0:
            accounting_record.baseValue = document_header.reteICABase + float(document_header.overCost)
        elif (not(document_header.overCostTaxBase)):
            accounting_record.baseValue = document_header.reteICABase
        accounting_record.percentage = document_header.reteICAPercent
        if account_type == "C":
            accounting_record.credit = abs(document_header.reteICAValue)
        else:
            accounting_record.debit = abs(document_header.reteICAValue)

        accounting_record.crossDocumentHeaderId =document_header.documentHeaderId
        return accounting_record

    def self_withholdingCREE(self, document_header=None, account_type=None):
        """

        :param document_header:
        :param account_type:
        :return:
        """
        accounting_record = AccountingRecord()

        # //Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.creeRetainingSale][0]
        accounting_record.baseValue = document_header.baseCREE

        if document_header.percentageCREE != None:
            accounting_record.percentage = document_header.percentageCREE

        if account_type == "C":
            accounting_record.credit = document_header.valueCREE
        else:
            accounting_record.debit = document_header.valueCREE

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def customer_receivable(self, document_header=None, payment_receipt=None,
                            payment_detail=None, account_type=None):
        if payment_receipt:
            accounting_record = AccountingRecord()
            # //Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = 'CU'
            accounting_record.customerId = document_header.customerId
            accounting_record.providerId = document_header.providerId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.businessAgentId = document_header.businessAgentId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.puc = [p for p in self.list_puc if p.legalCurrencyAccountsReceivable][0]

            accounting_record.crossPrefix = document_header.prefix
            accounting_record.crossDocument = "RENUMBER"
            accounting_record.dueDate = payment_receipt.firstQuota

            if account_type == "C":
                accounting_record.credit = payment_receipt.firstValue
            else:
                accounting_record.debit = payment_receipt.firstValue

            accounting_record.comments = document_header.comments
            if document_header.currency.currencyId != self.default_value.currency.currencyId:
                accounting_record.puc = [p for p in self.list_puc if p.foreignCurrencyAccountsreceivable][0]
            accounting_record.foreignCurrency = _round((payment_receipt.firstValue / document_header.exchangeRate), 2)
            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
            return accounting_record

        elif payment_detail:
            accounting_record = AccountingRecord()

            # //Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.allThirdId = accounting_record.customerId
            accounting_record.allThirdType = "CU"
            accounting_record.customerId = document_header.customerId
            accounting_record.providerId = document_header.providerId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.financialEntityId = document_header.financialEntityId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.puc = [p for p in self.list_puc if p.legalCurrencyAccountsReceivable][0]
            accounting_record.crossPrefix = document_header.prefix

            accounting_record.crossDocument = "RENUMBER"
            accounting_record.dueDate = payment_detail.dueDate
            accounting_record.quoteNumber = payment_detail.quoteNumber
            if account_type == "C":
                accounting_record.credit = payment_detail.value
            else:
                accounting_record.debit = payment_detail.value

            accounting_record.comments = payment_detail.comments

            if document_header.currency.currencyId != self.default_value.currency.currencyId:
                accounting_record.puc = [p for p in self.list_puc if p.foreignCurrencyAccountsreceivable][0]

            accounting_record.foreignCurrency = _round((payment_detail.value / document_header.exchangeRate), 2)
            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
            return accounting_record
        else:
            accounting_record = AccountingRecord()

            # //Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"
            accounting_record.customerId = document_header.customerId
            accounting_record.providerId = document_header.providerId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.businessAgentId = document_header.businessAgentId
            accounting_record.puc = [p for p in self.list_puc if p.legalCurrencyAccountsReceivable][0]
            accounting_record.crossPrefix = document_header.prefix
            accounting_record.crossDocument = "RENUMBER"
            accounting_record.dueDate =  self.add_days(document_header.documentDate, int(document_header.termDays))
            if account_type == "C":
                accounting_record.credit = document_header.total
            else:
                accounting_record.debit = document_header.total

            accounting_record.comments = document_header.comments
            if document_header.currency.currencyId != self.default_value.currency.currencyId:
                accounting_record.puc = [p for p in self.list_puc if p.foreignCurrencyAccountsreceivable][0]

            accounting_record.foreignCurrency = _round((document_header.total / document_header.exchangeRate), 2)
            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
            return accounting_record
