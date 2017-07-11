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
from ...referential.depreciation import Depreciation
from .... import session
from sqlalchemy import func, between, and_
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from datetime import *
from ..payment_accounting import PaymentAccounting
from .sale_functions import SaleFunctions
from ....utils.math_ext import _round

class SaleInvoiceAssetAccounting(object):

    def __init__(self, document_header):
        # Obtiene lista de puc por comany id
        self.list_puc = PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]
        self.list_depreciation = Depreciation.get_list_deprecation(document_header.branch.companyId)
        self.list_depreciation = [dep for dep in self.list_depreciation]
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
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)

            if self.total_records > 0:
                total_value = 0
                total_disccount = 0
                total_disccount2 = 0
                document_header.booleanValue = False
                for detail in document_details:
                    total_value = detail.value
                    # Calcula el sobre costo y el descuento para el item
                    # los detalles
                    self.discount2 = 0 if document_header.subtotal == 0 else _round(
                        document_header.disccount2Value * (detail.value / document_header.subtotal),
                        self.round_decimals)
                    # Si es el ultimo registro debe acomodar el saldo
                    # re calcula el sobrecosto y el descuento para este item
                    # en la v1  es recordnumber < totalrecord
                    if detail == document_details[-1]:
                        self.discount2 = document_header.disccount2Value - total_disccount2
                    #Impuesto al Consumo
                    if detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                        self.ret_value.append(
                            self.purchase_consumption_tax(document_header, detail, self.round_decimals, "C"))

                    #Valor del libro en activo
                    detail.bookValue = session.query(func.sum(AccountingRecord.debit - AccountingRecord.credit)) \
                        .filter(and_(AccountingRecord.pucId == detail.asset.pucId,
                                     AccountingRecord.assetId == detail.assetId,
                                     between(AccountingRecord.accountingDate, datetime(1900, 1, 1) ,document_header.documentDate))) \
                        .scalar()

                    detail.bookValue = detail.bookValue if detail.bookValue else 0
                    sum_value = detail.bookValue
                    self.ret_value.append(self.sale_asset(document_header, detail, sum_value, "C"))
                    total_value += (sum_value * (-1))
                    #Depreciacion del activo
                    detail.depreciation = session.query(func.sum(AccountingRecord.debit - AccountingRecord.credit)) \
                        .filter(and_(AccountingRecord.pucId.in_([p.pucId for p in self.list_puc if p.depreciationFixedAssetsAccount]),
                                     AccountingRecord.assetId == detail.assetId,
                                     between(AccountingRecord.accountingDate, datetime(1900, 1, 1) ,document_header.documentDate))) \
                        .scalar()
                    detail.depreciation = detail.depreciation if detail.depreciation else 0
                    depreciationPUCId = [puc.depreciationPUCId for puc in self.list_depreciation if puc.assetPUCId == detail.asset.pucId]
                    if depreciationPUCId is None or len(depreciationPUCId) == 0:
                        raise InternalServerError("No existe la cuenta de depreciación para el activo " + detail.asset.name \
                              + " con la cuenta :" + detail.asset.puc.pucClass + detail.asset.puc.pucSubClass \
                              + detail.asset.puc.account + detail.asset.puc.subAccount + detail.asset.puc.auxiliary1 \
                              + " " + detail.asset.puc.name)
                    depreciationPUCId = depreciationPUCId[0]
                    sum_value = detail.depreciation
                    self.ret_value.append(self.sale_asset_depreciation(document_header, detail, depreciationPUCId, sum_value, "D"))
                    total_value += (sum_value * (-1))

                    if total_value > 0:
                        # Utilidad en venta de Activo
                        self.ret_value.append(self.sale_asset_profit(document_header, detail, total_value, "C"))
                    else:
                        # Perdida en venta de Activo
                        self.ret_value.append(self.sale_asset_loss(document_header, detail, total_value, "D"))
                    #IVA en Ventas
                    if detail.baseValue> 0 and detail.value > 0:
                        self.ret_value.append(self.detail_iva(document_header=document_header,
                                                              document_detail=detail, overcost=0, disccount=0,
                                                              disccount2 = self.discount2,
                                                              round_decimals=self.round_decimals,
                                                              account_type='C'))
                    #ICA en Ventas
                    if detail.icaPercent > 0 and detail.value > 0:
                        self.ret_value.append(self.sales_ica_tax(document_header=document_header,
                                                               document_detail=detail,
                                                               round_decimals=self.round_decimals,
                                                               account_type='C'))
                        self.ret_value.append(self.sales_ica_expense(document_header=document_header,
                                                                   document_detail=detail,
                                                                   round_decimals=self.round_decimals,
                                                                   account_type='D'))
                    #Retefuente en Ventas
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
                    total_disccount2 += self.discount2
            # Calculo de TOTALES
            # IVA General, en documentHeader
            if not(document_header.ivaPUCId is None) and document_header.ivaValue and document_header.ivaValue > 0:
                self.ret_value.append(self.s_functions.IVA(document_header, self.round_decimals, 'C'))

            # FACTURA DE VENTA ACTIVOS FIJOS
            #Descuentos
            if document_header.disccount > 0:
                self.ret_value.append(self.s_functions.sale_discount(document_header, self.round_decimals, 'D'))
            # Impuesto al consumo en la factura de venta de activos
            if not(document_header.consumptionTaxPUCId is None) and document_header.consumptionTaxPercent > 0 and \
                            document_header.consumptionTaxBase > 0:
                self.ret_value.append(self.s_functions.sales_consumption_tax(document_header, self.round_decimals, 'D'))

            # Retefuente en Ventas
            if not(document_header.withholdingTaxPUCId is None) and document_header.withholdingTaxValue > 0 \
                    and document_header.withholdingTaxPercent and document_header.withholdingTaxPercent > 0 \
                    and document_header.withholdingTaxBase and document_header.withholdingTaxBase > 0:
                self.ret_value.append(self.s_functions.withholding_tax(document_header=document_header,
                                                                 account_type='D'))
                if self.selected_branch.company.selfRetainingRete:
                    self.ret_value.append(self.s_functions.self_withholding_tax(document_header=document_header,
                                                                          account_type='C'))
            # GENERALES DEL DOCUMENTO
            # Otros Descuentos
            if document_header.disccount2Value > 0:
                self.ret_value.append(self.s_functions.other_discount(document_header, self.round_decimals, 'D'))
            # Fletes
            if document_header.freight and document_header.freight > 0:
                self.ret_value.append(self.s_functions.sales_freight(document_header, self.round_decimals, 'C'))
            # ReteICA
            if document_header.reteICAValue > 0:
                self.ret_value.append(self.s_functions.rete_ica(document_header, 'D'))
                # Si es Autoretenedor de ICA
                if document_header.branch.company.selfRetainingICA:
                    self.ret_value.append(self.self_rete_ica(document_header, 'C'))
            # ReteIVA
            if document_header.reteIVAValue > 0:
                self.ret_value.append(self.s_functions.rete_iva(document_header, 'D'))
            # Retención CREE
            if document_header.valueCREE > 0:
                self.ret_value.append(self.s_functions.withholding_cree(document_header, 'D'))
                # Si es Autoretenedor del CREE
                if document_header.branch.company.selfRetainingRete \
                        or (document_header.branch.company.selfRetainingCREE
                            and document_header.documentDate.date() >= self.s_functions.dateCree1828):
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
                p_accounting.execute_payment_sales(document_header=document_header, payment_receipt=payment_receipt,
                                                   ret_value=self.ret_value, account_type="D")
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def sale_asset(self, document_header=None, document_detail=None, sum_vale=None, account_type="C"):
        accounting_record = AccountingRecord()
        # documento
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
        # detalle
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.asset.pucId
        if account_type == 'C':
            accounting_record.credit = abs(sum_vale)
        else:
            accounting_record.debit = abs(sum_vale)
        accounting_record.allThirdId = document_detail.assetId
        accounting_record.allThirdType = 'AS'
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sale_asset_depreciation(self, document_header=None, document_detail=None, depreciationPUCId=None,
                                sum_vale=None, account_type="C"):
        accounting_record = AccountingRecord()
        # documento
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
        # detalle
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = depreciationPUCId
        if account_type == 'C':
            accounting_record.credit = abs(sum_vale)
        else:
            accounting_record.debit = abs(sum_vale)
        accounting_record.allThirdId = document_detail.assetId
        accounting_record.allThirdType = 'AS'
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sale_asset_profit(self, document_header=None, document_detail=None, total_value=None, account_type="C"):
        accounting_record = AccountingRecord()
        # documento
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
        # detalle
        accounting_record.assetId = document_detail.assetId
        if document_detail.asset.puc.billingConceptsFixedAssetsIntangibles:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.assetUtility and p.Account == "48"][0]
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.assetUtility and
                                       p.subAccount == str(document_detail.asset.puc.account)][0]
        if account_type == 'C':
            accounting_record.credit = abs(total_value)
        else:
            accounting_record.debit = abs(total_value)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sale_asset_loss(self, document_header=None, document_detail=None, total_value=None, account_type="C"):
        accounting_record = AccountingRecord()
        # documento
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
        # detalle
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.lossFixedAssets][0]
        if account_type == 'C':
            accounting_record.credit = abs(total_value)
        else:
            accounting_record.debit = abs(total_value)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def customer_receivable(self, document_header, payment_receipt, payment_detail, account_type):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.customerId = document_header.customerId
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.legalCurrencyAccountsReceivable][0]
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = 'RENUMBER'
        if payment_receipt:
            accounting_record.dueDate = payment_receipt.firstQuota
            if account_type == 'C':
                accounting_record.credit = payment_receipt.firstValue
            else:
                accounting_record.debit = payment_receipt.firstValue
            accounting_record.foreignCurrency = _round((payment_receipt.firstValue / document_header.exchangeRate), 2)
        elif payment_detail:
            accounting_record.dueDate = payment_detail.dueDate
            accounting_record.quoteNumber = payment_detail.quoteNumber
            if account_type == 'C':
                accounting_record.credit = payment_detail.value
            else:
                accounting_record.debit = payment_detail.value
            accounting_record.foreignCurrency = _round((payment_detail.value / document_header.exchangeRate), 2)
        else:
            accounting_record.dueDate = document_header.documentDate + timedelta(days=int(document_header.termDays))

            if account_type == 'C':
                accounting_record.credit = document_header.total
            else:
                accounting_record.debit = document_header.total
            accounting_record.foreignCurrency = _round((document_header.total / document_header.exchangeRate), 2)

        accounting_record.comments = document_header.comments
        if document_header.currencyId != self.default_value.currencyId:
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.foreignCurrencyAccountsreceivable][0]

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def self_withholdingCREE(self, document_header=None, account_type=None):
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

    def self_rete_ica(self, document_header=None, account_type=None):
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
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.icaRetainingSale][0]
        if document_header.overCostTaxBase and document_header.overCost > 0:
            accounting_record.baseValue = document_header.reteICABase + float(document_header.overCost)
        elif (not (document_header.overCostTaxBase)):
            accounting_record.baseValue = document_header.reteICABase
        accounting_record.percentage = document_header.reteICAPercent
        if account_type == "C":
            accounting_record.credit = abs(document_header.reteICAValue)
        else:
            accounting_record.debit = abs(document_header.reteICAValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def purchase_consumption_tax(self, document_header, detail, round_decimals, account_type):
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
        # Detalle
        accounting_record.assetId = detail.assetId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = detail.consumptionTaxBase
        accounting_record.percentage = detail.consumptionTaxPercent
        accounting_record.comments = detail.comments
        accounting_record.pucId = detail.consumptionTaxPUCId

        if account_type == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                              self.round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                             self.round_decimals)

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def detail_iva(self, document_header=None, document_detail=None, overcost=0, disccount=0,
                   disccount2=None, round_decimals=None, account_type='C'):
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

    def sales_ica_tax(self, document_header=None, document_detail=None, round_decimals=None, account_type='C'):
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

    def sales_ica_expense(self, document_header=None, document_detail=None, round_decimals=None, account_type='D'):
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

    def detail_withholdingTax(self, document_header=None, document_detail=None, overcost=0, discount=0,
                              discount2=None, round_decimals=None, account_type='D'):
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
            accounting_record.credit = _round(accounting_record.baseValue * (document_detail.withholdingTax / 100),
                                              round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * (document_detail.withholdingTax / 100),
                                             round_decimals)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeader.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def self_detail_withholdingTax(self, document_header=None, document_detail=None, overcost=0,
                                   discount=0, disccount2=None, round_decimals=None, account_type='C'):
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
        accounting_record.pucId = [p for p in self.list_puc if p.withholdingRetainingService][0]
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.percentage = document_detail.withholdingTax
        if account_type == "C":
            accounting_record.credit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100,
                                              round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * document_detail.withholdingTax / 100,
                                             round_decimals)
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record
