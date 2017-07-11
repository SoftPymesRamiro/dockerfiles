# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 10-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["david"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import _round
from ....exceptions import ValidationError, InternalServerError
from datetime import datetime, timedelta
from .sale_functions import SaleFunctions


class CustomerNoteAccountingNC(object):
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

        self.date_cree_1828 = datetime(year=2013, month=9, day=1)
        self.s_functions = SaleFunctions(document_header, self.list_puc, self.default_value, self.general_parameter)

    def do_account(self, document_header, document_details, payment_receipt=None):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            # Recorrido de detalles
            if self.total_records > 0:
                total_value = 0
                total_disccount = 0
                total_disccount2 = 0
                document_header.booleanValue = False
                for detail in document_details:

                    # // Ingreso
                    if not (document_header.sourceDocumentHeader.source.shortWord == 'FS'
                            or document_header.sourceDocumentHeader.source.shortWord == 'AU'):
                        self.ret_value.append(self.income_inventory(document_header, detail, self.round_decimals, "D"))

                    # // Impuesto al Consumo
                    if detail.itemId is not None and detail.item.consumptionPercentage > 0 and detail.value > 0:
                        self.ret_value.append(
                            self.sales_consumption_tax(document_header, detail, self.round_decimals, "D"))

                    # Servicios profesionales
                    if document_header.sourceDocumentHeader.source.shortWord == 'FS' and (detail.comments is not None and detail.comments != ''):
                        self.ret_value.append(self.sales_income_concept(document_header, detail, self.round_decimals, "D"))

                    # Facturacion AIU
                    if document_header.sourceDocumentHeader.source.shortWord == 'AU' \
                            and (detail.comments is not None and detail.comments != '') and detail.puc is not None:
                        self.ret_value.append(self.sales_income_concept(document_header, detail, self.round_decimals, "D"))

                    # IVA en ventas
                    if detail.value > 0:
                        self.ret_value.append(self.detail_iva(document_header, detail, 0, 0, 0, self.round_decimals,
                                                              "D"))

                    # ICA en ventas
                    if detail.icaPercent and detail.icaPercent > 0 and detail.value > 0:
                        self.ret_value.append(self.sales_ica_tax(document_header, detail, self.round_decimals, 'D'))
                        self.ret_value.append(
                            self.sales_ica_expense(document_header, detail, self.round_decimals, 'C'))

                    # Retefuente en Ventas
                    if detail.value > 0:
                        self.ret_value.append(self.detail_withholding_tax(document_header, detail, 0, 0, 0,
                                                                          self.round_decimals, 'C'))
                        if document_header.branch.company.selfRetainingRete:
                            self.ret_value.append(self.self_detail_withholding_tax(document_header, detail, 0, 0, 0,
                                                                                   self.round_decimals, 'D'))

            # Calculo de TOTALES
            # Otros Descuentos
            if document_header.disccount2Value > 0:
                self.ret_value.append(self.s_functions.other_discount(document_header, self.round_decimals, 'C'))

            # ReteICA
            if document_header.reteICAValue > 0:
                self.ret_value.append(self.s_functions.rete_ica(document_header, 'C'))
                # Si es Autoretenedor de ICA
                if document_header.branch.company.selfRetainingICA:
                    self.ret_value.append(self.self_rete_ica(document_header, 'D'))

            # ReteIVA
            if document_header.reteIVAValue > 0:
                self.ret_value.append(self.s_functions.rete_iva(document_header, 'C'))

            # Retención CREE
            if document_header.valueCREE > 0:
                self.ret_value.append(self.s_functions.withholding_cree(document_header, 'C'))
                # Si es Autoretenedor del CREE
                if document_header.branch.company.selfRetainingRete \
                        or (document_header.branch.company.selfRetainingCREE
                            and document_header.documentDate.date() >= self.date_cree_1828.date()):
                    self.ret_value.append(self.self_withholding_cree(document_header, 'D'))

            self.ret_value.append(self.customer_receivable(document_header=document_header, credit_debit='C'))

            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def sales_income_concept(self, document_header=None, document_detail=None, round_decimals=None, account_type=None):
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

    def income_inventory(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId
        accounting_record.itemId = detail.itemId
        accounting_record.comments = detail.comments
        accounting_record.pucId = detail.item.incomingPUCId if detail.item is not None else None
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        accounting_record.measurementUnitId = detail.measurementUnitId

        if credit_debit == 'C':
            accounting_record.credit = _round((detail.value - _round(detail.value * detail.disccount / 100,
                                                                     self.round_decimals)), self.round_decimals)
        else:
            accounting_record.debit = _round((detail.value - _round(detail.value * detail.disccount / 100,
                                                                    self.round_decimals)), self.round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def detail_iva(self, document_header, detail, over_cost, discount, discount2, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = accounting_record.mainThirdId if accounting_record.mainThirdId is not None \
            else document_header.costCenter.branch.branchId
        accounting_record.allThirdType = 'TH' if accounting_record.mainThirdId is not None else 'BR'

        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = detail.ivaPUCId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId

        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.percentage = detail.iva

        if not document_header.overCostTaxBase and not (detail.itemId is not None and detail.item.disccountToUnitValue):
            accounting_record.baseValue = _round(detail.baseValue - discount, round_decimals)
        accounting_record.baseValue = detail.baseValue
        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * detail.iva / 100, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * detail.iva / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sales_ica_tax(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.industryAndCommerceTaxICA][0]
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = _round((detail.value - _round(detail.value * detail.disccount / 100,
                                                                    round_decimals)), round_decimals)
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue = _round((accounting_record.baseValue - _round(
                detail.value * document_header.disccount2 / 100, round_decimals)), round_decimals)

        accounting_record.percentage = detail.icaPercent
        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * detail.icaPercent / 1000, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * detail.icaPercent / 1000, round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sales_ica_expense(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.taxExpenseIndustryCommerce][0]
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = _round((detail.value - _round(detail.value * detail.disccount / 100,
                                                                    round_decimals)), round_decimals)

        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue = _round((accounting_record.baseValue -
                                                  _round(detail.value * document_header.disccount2 / 100,
                                                         round_decimals)), round_decimals)
        accounting_record.percentage = detail.icaPercent
        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * detail.icaPercent / 1000, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * detail.icaPercent / 1000, round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def detail_withholding_tax(self, document_header, detail, over_cost, discount, discount2, round_decimals, credit_debit):
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

        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = detail.withholdingTaxPUCId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = detail.baseValue

        if not document_header.overCostTaxBase:
            accounting_record.baseValue = _round(detail.baseValue - discount, round_decimals)
        accounting_record.percentage = detail.withholdingTax
        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * detail.withholdingTax / 100, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * detail.withholdingTax / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def self_detail_withholding_tax(self, document_header, detail, over_cost, discount, discount2, round_decimals, credit_debit):
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

        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.withholdingRetainingSale][0]
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = detail.baseValue

        if not document_header.overCostTaxBase:
            accounting_record.baseValue = _round(detail.baseValue - discount, round_decimals)
        accounting_record.percentage = detail.withholdingTax
        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * detail.withholdingTax / 100, round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * detail.withholdingTax / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def self_rete_ica(self, document_header, credit_debit):
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

        accounting_record.pucId = [a.pucId for a in self.list_puc if a.icaRetainingSale][0]
        if document_header.overCostTaxBase and document_header.overCost > 0:
            accounting_record.baseValue = document_header.reteICABase + document_header.overCost
        elif not document_header.overCostTaxBase:
            accounting_record.baseValue = document_header.reteICABase
        accounting_record.percentage = document_header.reteICAPercent

        if credit_debit == 'C':
            accounting_record.credit = abs(document_header.reteICAValue)
        else:
            accounting_record.debit = abs(document_header.reteICAValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def rete_iva(self, document_header, credit_debit):
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

        accounting_record.pucId = [a.pucId for a in self.list_puc if a.salesReteIVA][0]
        accounting_record.baseValue = document_header.reteIVABase
        accounting_record.percentage = document_header.reteIVAPercent
        if credit_debit == 'C':
            accounting_record.credit = abs(document_header.reteIVAValue)
        else:
            accounting_record.debit = abs(document_header.reteIVAValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def withholding_cree(self, document_header, credit_debit):
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

        if document_header.branch.withholdingCREEPUCId is None:
            raise ValueError('No se ha parametrizado la cuenta de autorretencion renta en la sucursal. '
                             'Favor parametrizarla antes de continuar')
        accounting_record.pucId = document_header.branch.withholdingCREEPUCId
        accounting_record.baseValue = document_header.baseCREE
        if document_header.percentageCREE is not None:
            accounting_record.percentage = document_header.percentageCREE
        if credit_debit == 'C':
            accounting_record.credit = document_header.valueCREE
        else:
            accounting_record.debit = document_header.valueCREE
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def self_withholding_cree(self, document_header, credit_debit):
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
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.creeRetainingSale][0]
        accounting_record.baseValue = document_header.baseCREE
        if document_header.percentageCREE is not None:
            accounting_record.percentage = document_header.percentageCREE
        if credit_debit == 'C':
            accounting_record.credit = document_header.valueCREE
        else:
            accounting_record.debit = document_header.valueCREE
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def customer_receivable(self, document_header, credit_debit):
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
        puc_id = [a.pucId for a in self.list_puc if a.paymentsForThirdParties]
        if not len(puc_id):
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.legalCurrencyAccountsReceivable][0]
        else:
            accounting_record.pucId = puc_id[0]

        accounting_record.crossPrefix = document_header.sourceDocumentHeader.prefix
        accounting_record.crossDocument = document_header.sourceDocumentHeader.documentNumber

        accounting_record.dueDate = document_header.documentDate + timedelta(days=int(document_header.termDays))

        if document_header.currencyId != self.default_value.currencyId:
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.foreignCurrencyAccountsreceivable][0]

        accounting_record.foreignCurrency = _round((document_header.total / document_header.exchangeRate), 2)

        if credit_debit == 'C':
            accounting_record.credit = document_header.total
        else:
            accounting_record.debit = document_header.total

        accounting_record.comments = document_header.comments

        accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeaderId
        return accounting_record

    def sales_consumption_tax(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        accounting_record.itemId = detail.itemId
        accounting_record.comments = detail.comments
        accounting_record.pucId = detail.item.consumptionPUCId if detail.item is not None else None
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.baseValue = detail.consumptionTaxBase
        accounting_record.percentage = detail.consumptionTaxPercent

        if credit_debit == 'C':
            accounting_record.credit = _round(accounting_record.baseValue * accounting_record.percentage / 100,
                                              self.round_decimals)
        else:
            accounting_record.debit = _round(accounting_record.baseValue * accounting_record.percentage / 100,
                                             self.round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record
