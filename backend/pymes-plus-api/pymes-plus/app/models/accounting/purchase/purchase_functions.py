# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
#
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import _round
from datetime import timedelta

class PurchaseFunctions(object):
    """

    """
    def __init__(self, document_header, list_puc = None, default_value =None, general_parameter =None):
        """
        Allow call methods and functions by documents
        :param document_header:  document
        :param list_puc:  puc
        :param default_value: data default values
        :param general_parameter:  several parameters
        """
        # Obtiene lista de puc por comany id
        self.list_puc = list_puc if list_puc else PUC.get_list_puc(document_header.branch.companyId)
        self.list_puc = [p for p in self.list_puc]
        # Obtiene los valores por defecto por branch id
        self.default_value = default_value if default_value else \
            DefaultValue.get_default_value_by_branch_id(document_header.branchId)
        # Obtiene los valores generales de la app
        self.general_parameter = general_parameter if general_parameter \
            else GeneralParameter.get_general_parameter()
        # Obtiene valor de decimales de default values
        self.round_decimals = self.default_value.valueDecimals
        self.total_records = 0
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

    def add_days(self, date, days):
        """
        Allow add days to a date
        :param date: input date
        :param days: days to agregate
        :return:
        """
        for i in range(days):
            date += timedelta(days=1)
        return date

    def IVA(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
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
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = document_header.ivaPUCId
        accounting_record.baseValue = document_header.ivaBase
        accounting_record.percentage = document_header.ivaPercent
        if account_type == "C":
            accounting_record.credit = float(_round(document_header.ivaValue, self.round_decimals))
        else:
            accounting_record.debit = float(_round(document_header.ivaValue, self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def contract_provider(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.contractId = document_header.contract.contractId
        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = document_header.pucId
        if account_type == "C":
            accounting_record.credit = float(_round(document_header.subtotal, self.round_decimals))
        else:
            accounting_record.debit = float(_round(document_header.subtotal, self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def purchase_discount(self, document_header=None, discount_purchase=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
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
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.discountPurchases][0]
        if account_type == "C":
            accounting_record.credit = float(_round(document_header.disccount - discount_purchase
                                                    if discount_purchase else document_header.disccount,
                                                    self.round_decimals))
        else:
            accounting_record.debit = float(_round(document_header.disccount - discount_purchase
                                                   if discount_purchase else document_header.disccount,
                                                   self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def purchase_other_discount(self, document_header=None, round_decimals=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
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
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.discountPurchases][0]
        if account_type == "C":
            accounting_record.credit = float(_round(document_header.disccount2Value, self.round_decimals))
        else:
            accounting_record.debit = float(_round(document_header.disccount2Value, self.round_decimals))
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def interest_expense(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = document_header.providerId
        if document_header.provider:
            accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.allThirdId = document_header.provider.thirdPartyId
        accounting_record.allThirdId = "TH"
        accounting_record.puc = [p for p in self.list_puc if p.penaltyInterestPurchases][0]
        if account_type == "C":
            accounting_record.credit = float(document_header.interest)
        else:
            accounting_record.debit = float(document_header.interest)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def insurance_expense(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.insurance][0]
        if account_type == "C":
            accounting_record.credit = float(document_header.insurance)
        else:
            accounting_record.debit = float(document_header.insurance)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def freight_expense(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.freightPurchases][0]
        if account_type == "C":
            accounting_record.credit = float(document_header.freight)
        else:
            accounting_record.debit = float(document_header.freight)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def detail_iva(self, document_header=None, document_detail=None, overcost=None, discount=None,
                   discount2=None, decimal_values=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate

        if document_header.source.shortWord in ("LA", "LC", "LF", "LG"):
            accounting_record.costCenter = document_detail.costCenter
            accounting_record.division = document_detail.division
            accounting_record.section = document_detail.section
            accounting_record.dependency = document_detail.dependency

            accounting_record.mainThirdId = document_detail.customer.thirdPartyId \
                if document_detail.customer else \
                document_detail.provider.thirdPartyId if document_detail.provider else \
                    document_detail.otherThird.thirdPartyId if document_detail.otherThird else \
                        document_detail.employee.thirdPartyId if document_detail.employee else \
                            document_detail.third.thirdPartyId if document_detail.third else None

            accounting_record.customerId = document_detail.customerId
            accounting_record.providerId = document_detail.providerId
            accounting_record.employeeId = document_detail.employeeId
            accounting_record.allThirdId = document_detail.third.thirdPartyId
            accounting_record.allThirdType = "TH"

        else:
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.third.thirdPartyId if document_header.third else None

            accounting_record.customerId = document_header.customerId
            accounting_record.providerId = document_header.providerId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.businessAgent = document_header.businessAgent

            accounting_record.allThirdId = document_header.customer.thirdPartyId \
                if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.third.thirdPartyId if document_header.third else None \
                                if accounting_record.mainThird else document_header.costCenter.branch.branchId

            # accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        #  Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.ivaPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId

        accounting_record.measurementUnitId = document_detail.measurementUnitId

        if not document_header.overCostTaxBase and not (document_detail.item and document_detail.item.disccountToUnitValue):

            if document_header.source.shortWord in ("FPD", "FPI", "FPC", "FPA", "FM", "FME"):
                accounting_record.baseValue = _round(document_detail.baseValue - discount -
                                                     _round(document_detail.baseValue * document_detail.disccount / 100,
                                                            self.round_decimals),
                                                     self.round_decimals)
            elif not (document_header.source.shortWord in ("FPI", "FPA", "FPD", "FPC", "FP", "DR")):
                accounting_record.baseValue = _round(document_detail.baseValue - discount, self.round_decimals)

        if (document_header.disccount2TaxBase and document_header.disccount2Value > 0) \
                and (document_header.source.shortWord in ("FM", "FME")):
            accounting_record.baseValue -= _round(discount2, self.round_decimals)

        accounting_record.percentage = document_detail.iva

        # calculo de cuentas del iva cuando el documento es una factura de compras y gastos, y el valor total tiene un descuento
        # calculo de cuentas del iva cuando el documento es consumo interno de articulos
        if not document_header.source.shortWord in ("CI", "FPC", "FPD", "FPI", "FPA"):
            accounting_record.baseValue = document_detail.baseValue
        else:
            accounting_record.baseValue = document_detail.baseValueIVA

        if account_type == "C":
            accounting_record.credit = float(
                _round(accounting_record.baseValue * document_detail.iva / 100, self.round_decimals))
        else:
            accounting_record.debit = float(
                _round(accounting_record.baseValue * document_detail.iva / 100, self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def purchase_consumptionTax(self, document_header=None, document_detail=None,
                                decimal_values=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
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
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId

        # Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.consumptionTaxBase
        accounting_record.percentage = document_detail.consumptionTaxPercent
        accounting_record.puc = document_detail.item.consumptionPUC \
            if document_detail.item else document_detail.consumptionTaxPUC

        if account_type == "C":
            accounting_record.credit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                    self.round_decimals))
        else:
            accounting_record.debit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                   self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def detail_withholdingTax(self, document_header=None, document_detail=None, overcost=None, discount=None,
                              discount2=None, decimal_values=None, account_type=None):
        accounting_record = AccountingRecord()
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
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.BusinessAgent = document_header.businessAgent

        # Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.withholdingTaxPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.baseValue = document_detail.baseValue
        accounting_record.measurementUnitId = document_detail.measurementUnitId

        if not document_header.overCostTaxBase \
                and document_detail.item \
                and not document_detail.item.disccountToUnitValue:

            if document_header.source.shortWord in ("FPD", "FPI", "FPC", "FPA", "FM", "FME"):
                accounting_record.baseValue = \
                    _round(document_detail.baseValue - discount -
                           _round(document_detail.baseValue * document_detail.disccount / 100, self.round_decimals),
                           self.round_decimals)

            elif not document_header.source.shortWord in ("FPI", "FPA", "FPD", "FPC", "FP",
                                                          "DR"):  # if (!"FPI~FPA~FPD~FPC~FP~DR".Split('~').Contains(document_header.source.shortWord)) # != "FPI" and document_header.source.shortWord != "FPA" and document_header.source.shortWord != "FPD" and document_header.source.shortWord != "FPC")
                accounting_record.baseValue = _round(document_detail.baseValue - discount, self.round_decimals)

        if (document_header.disccount2TaxBase and document_header.disccount2Value > 0) \
                and document_header.source.shortWord == ("FM", "FME"):
            accounting_record.baseValue -= _round(discount2, self.round_decimals)
        accounting_record.percentage = document_detail.withholdingTax
        if document_header.source.shortWord in ("CI", "FPC", "FPD", "FPI", "FPA"):
            accounting_record.baseValue = document_detail.baseValueIVA
        if account_type == "C":
            accounting_record.credit = float(
                _round(accounting_record.baseValue * document_detail.withholdingTax / 100, self.round_decimals))
        else:
            accounting_record.debit = float(
                _round(accounting_record.baseValue * document_detail.withholdingTax / 100, self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def provider_payable(self, document_header=None, decimal_value=None, account_type=None, is_renumber=None,
                         payment_receipt=None, payment_details=None):
        if document_header and decimal_value and account_type and not is_renumber is None:
            accounting_record = AccountingRecord()
            # Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId
            accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

            accounting_record.allThirdId = document_header.providerId if document_header.provider else \
                document_header.customerId if document_header.customer else \
                    document_header.otherThirdId if document_header.otherThird else \
                        document_header.employeeId if document_header.employee else \
                            document_header.partnerId if document_header.partner else \
                                document_header.financialEntityId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

            accounting_record.allThirdType = "PR" if document_header.provider else \
                "CU" if document_header.customer else \
                    "OT" if document_header.otherThird else \
                        "EM" if document_header.employee else \
                            "PA" if document_header.partner else \
                                "FE" if document_header.financialEntity else \
                                    "TH" if document_header.third else None

            accounting_record.providerId = document_header.providerId
            accounting_record.customerId = document_header.customerId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]
            accounting_record.sourceDocumentType = document_header.sourceDocumentType
            if not is_renumber:
                accounting_record.crossPrefix = document_header.prefix
                accounting_record.crossDocument = document_header.documentNumber

            elif document_header.sourceDocumentType and document_header.sourceDocumentType.shortWord == "RP":
                accounting_record.crossPrefix = document_header.sourceDocumentHeader.prefix
                accounting_record.crossDocument = document_header.sourceDocumentHeader.documentNumber
            else:

                accounting_record.crossPrefix = document_header.prefix
                # accounting_record.CrossDocument = document_header.documentNumber
                accounting_record.crossDocument = "RENUMBER"

            # accounting_record.dueDate = document_header.documentDate.AddDays(float(document_header.TermDays))
            accounting_record.dueDate = self.add_days(document_header.documentDate, int(document_header.termDays))
            if account_type == "C":
                accounting_record.credit = decimal_value
            else:
                accounting_record.debit = decimal_value
            accounting_record.comments = document_header.comments

            if document_header.currencyId != self.default_value.currencyId and document_header.documentType.shortWord != "FPC":
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableForeignProvider][0]

            accounting_record.foreignCurrency = _round(document_header.total / document_header.exchangeRate, 2)

            # if ((document_header.SourceDocumentHeader != null) && ("DR~DP~CP~RP".Contains(document_header.SourceDocumentHeader.documentType.shortWord)))
            if ((document_header.sourceDocumentHeader) and (document_header.documentType.shortWord =="DR" or
                                                                   document_header.documentType.shortWord =="DP" or
                                                                   document_header.documentType.shortWord =="CP")):
                # accounting_record.CrossDocumentHeader = document_header.SourceDocumentHeader
                accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeader.documentHeaderId
            else:
                # accounting_record.CrossDocumentHeader = document_header
                accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

            return accounting_record
        elif document_header and account_type and decimal_value is None \
                and is_renumber is None and payment_details is None and payment_receipt:
            # ProviderPayable(DocumentHeader documentHeader, PaymentReceipt paymentreceipt, string creditdebit)
            accounting_record = AccountingRecord()
            # Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.third if document_header.third else None

            accounting_record.allThirdId = document_header.providerId if document_header.provider else \
                document_header.customer.customerId if document_header.customer else \
                    document_header.otherThird.otherThirdId if document_header.otherThird else \
                        document_header.employee.employeeId if document_header.employee else \
                            document_header.partner.partnerId if document_header.partner else \
                                document_header.financialEntity.financialEntityId if document_header.financialEntity else \
                                    document_header.third if document_header.third else None

            accounting_record.allThirdType = "PR" if document_header.provider else \
                "CU" if document_header.customer else \
                    "OT" if document_header.otherThird else \
                        "EM" if document_header.employee else \
                            "PA" if document_header.partner else \
                                "FE" if document_header.financialEntity else \
                                    "TH" if document_header.third else None

            accounting_record.providerId = document_header.providerId
            accounting_record.customerId = document_header.customerId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.employeeId = document_header.employeeId
            if document_header.paymentTerm.quota == True and document_header.documentType and "FP" == document_header.documentType.shortWord:
                accounting_record.crossPrefix = document_header.controlPrefix
                accounting_record.crossDocument = document_header.controlNumber
            else:
                accounting_record.crossDocument = document_header.sourceDocument

            accounting_record.DueDate = payment_receipt.firstQuota

            if account_type == "C":
                accounting_record.credit = payment_receipt.firstValue
            else:
                accounting_record.debit = payment_receipt.firstValue

            accounting_record.comments = document_header.comments

            accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]

            if document_header.currency.currencyId != self.default_value.currency.currencyId:
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableForeignProvider][0]


            accounting_record.foreignCurrency =_round((float)(payment_receipt.firstValue / document_header.exchangeRate), 2)

            # if (documentHeader.SourceDocumentHeader != null and "DR~DP~CP~RP".Contains(documentHeader.SourceDocumentHeader.documentType.shortWord))
            accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeader.documentHeaderId \
                if document_header.sourceDocumentHeader and document_header.documentType.shortWord in (
            "DR", "DP", "CP") \
                else document_header.documentHeaderId
            return accounting_record

        elif document_header and account_type and decimal_value is None \
                and is_renumber is None and payment_details is None and payment_receipt is None:
            #(document_header=document_header, account_type="C")
            accounting_record = AccountingRecord()
            # Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

            accounting_record.allThirdId = document_header.providerId if document_header.provider else \
                document_header.customer.customerId if document_header.customer else \
                    document_header.otherThird.otherThirdId if document_header.otherThird else \
                        document_header.employee.employeeId if document_header.employee else \
                            document_header.partner.partnerId if document_header.partner else \
                                document_header.financialEntity.financialEntityId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

            accounting_record.allThirdType = "PR" if document_header.provider else \
                "CU" if document_header.customer else \
                    "OT" if document_header.otherThird else \
                        "EM" if document_header.employee else \
                            "PA" if document_header.partner else \
                                "FE" if document_header.financialEntity else \
                                    "TH" if document_header.third else None

            accounting_record.providerId = document_header.providerId
            accounting_record.customerId = document_header.customerId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.employeeId = document_header.employeeId

            if document_header.source.shortWord in ("FRP", "FPA", "FP", "FPD", "FPI", "FT", "RP", "FM") or \
                    (
                                    document_header.currency.currencyId == self.default_value.currency.currencyId
                            and document_header.source.shortWord == "FM"):
                #  Si NO ES Costos y Gastos por pagar va a la cuenta de Proveedores (2205)
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]
            # else if (documentHeader.source.shortWord == "FPC")
            elif document_header.sourceDocumentHeader and \
                    document_header.sourceDocumentHeader.source and \
                            document_header.sourceDocumentHeader.source.shortWord == "FPC":
                #  Si ES Costos y Gastos por pagar va a esa cuenta (2335)
                accounting_record.puc = document_header.puc
            elif document_header.documentType.shortWord in ("IV", "IC", "PD", "RF"):
                #  Si ES pago de IVA o de Retefuente (2335-95-005)
                accounting_record.puc = [p for p in self.list_puc if p.legalizationLowerBox][0]
            elif document_header.documentType.shortWord in ("DR", "CP", "DP"):
                #  Si ES una Devolución a Proveedor
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]
            else:
                #  Si ES Costos y Gastos por pagar va a esa cuenta (2335)
                accounting_record.puc = document_header.puc

            if document_header.documentType.shortWord != "FP" and document_header.sourceDocumentHeader:
                accounting_record.sourceDocumentType = document_header.sourceDocumentType
                accounting_record.crossPrefix = document_header.sourceDocumentHeader.controlPrefix
                accounting_record.crossDocument = document_header.sourceDocumentHeader.controlNumber
                accounting_record.dueDate = self.add_days(document_header.documentDate, int(document_header.termDays))
            #
            # Cuando sea pago de impuestos el CrossDocument es el mismo numero de documento - Alejandro
            elif document_header.documentType.shortWord in ("IV", "IC", "PD", "RF"):
                accounting_record.crossPrefix = document_header.pºrefix
                accounting_record.crossDocument = document_header.documentNumber
                accounting_record.dueDate = self.add_days(document_header.documentDate, int(document_header.termDays))

            else:
                accounting_record.crossPrefix = document_header.controlPrefix
                accounting_record.crossDocument = document_header.controlNumber
                accounting_record.dueDate = self.add_days(document_header.documentDate, int(document_header.termDays))

            if account_type == "C":
                accounting_record.credit = float(document_header.total)
            else:
                accounting_record.debit = float(document_header.total)

            accounting_record.comments = document_header.comments

            if (document_header.currency.currencyId != self.default_value.currency.currencyId and \
                            document_header.documentType.shortWord != "FPC"):
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableForeignProvider][0]

            accounting_record.foreignCurrency = _round(
                float(document_header.total) / float(document_header.exchangeRate), 2)

            accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeader.documentHeaderId \
                if document_header.sourceDocumentHeader and document_header.documentType.shortWord in ("DR", "DP", "CP") \
                else document_header.documentHeaderId
            return accounting_record
        elif document_header and payment_receipt and account_type and is_renumber is None and payment_details is None:
            accounting_record = AccountingRecord()
            # Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None

            accounting_record.allThirdId = document_header.providerId if document_header.provider else \
                document_header.customer.customerId if document_header.customer else \
                    document_header.otherThird.otherThirdId if document_header.otherThird else \
                        document_header.employee.employeeId if document_header.employee else \
                            document_header.partner.partnerId if document_header.partner else \
                                document_header.financialEntity.financialEntityId if document_header.financialEntity else \
                                    document_header.thirdId if document_header.third else None


            accounting_record.allThirdType = "PR" if document_header.provider else \
                "CU" if document_header.customer else \
                    "OT" if document_header.otherThird else \
                        "EM" if document_header.employee else \
                            "PA" if document_header.partner else \
                                "FE" if document_header.financialEntity else \
                                    "TH" if document_header.third else None

            accounting_record.providerId = document_header.providerId
            accounting_record.customerId = document_header.customerId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.employeeId = document_header.employeeId

            accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]
            accounting_record.sourceDocumentTypeId = document_header.sourceDocumentTypeId
            accounting_record.crossPrefix = document_header.sourcePrefix

            if document_header.paymentTerm.quota and document_header.documentType \
                    and document_header.documentType.shortWord == "FP":
                accounting_record.crossDocument = document_header.controlNumber
            else:
                accounting_record.crossDocument = document_header.sourceDocument

            accounting_record.dueDate = payment_receipt.firstQuota

            if account_type == "C":
                accounting_record.credit = float(payment_receipt.firstValue)
            else:
                accounting_record.debit = float(payment_receipt.firstValue)

            accounting_record.comments = document_header.comments

            if document_header.currency.currencyId != self.default_value.currency.currencyId:
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableForeignProvider][0]

            accounting_record.foreignCurrency = _round(
                float(payment_receipt.firstValue) / float(document_header.exchangeRate), 2)

            accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeader.documentHeaderId \
                if document_header.sourceDocumentHeader and document_header.documentType.shortWord in ("DR", "DP", "CP") \
                else document_header.documentHeaderId
            return accounting_record
        elif document_header and payment_details and account_type and is_renumber is None:
            accounting_record = AccountingRecord()
            # Datos de Encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId if document_header.customer else \
                document_header.provider.thirdPartyId if document_header.provider else \
                    document_header.otherThird.thirdPartyId if document_header.otherThird else \
                        document_header.employee.thirdPartyId if document_header.employee else \
                            document_header.partner.thirdPartyId if document_header.partner else \
                                document_header.financialEntity.thirdPartyId if document_header.financialEntity else \
                                    document_header.third if document_header.third else None

            accounting_record.allThirdId = document_header.providerId if document_header.provider else \
                document_header.customer.customerId if document_header.customer else \
                    document_header.otherThird.otherThirdId if document_header.otherThird else \
                        document_header.employee.employeeId if document_header.employee else \
                            document_header.partner.partnerId if document_header.partner else \
                                document_header.financialEntity.financialEntityId if document_header.financialEntity else \
                                    document_header.third if document_header.third else None

            accounting_record.allThirdType = "PR" if document_header.provider else \
                "CU" if document_header.customer else \
                    "OT" if document_header.otherThird else \
                        "EM" if document_header.employee else \
                            "PA" if document_header.partner else \
                                "FE" if document_header.financialEntity else \
                                    "TH" if document_header.third else None

            accounting_record.providerId = document_header.providerId
            accounting_record.customerId = document_header.customerId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.employeeId = document_header.employeeId

            if document_header.source.shortWord != "FPC":
                #  Si NO ES Costos y Gastos por pagar va a la cuenta de Proveedores (2205)
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableNationalProvider][0]
            else:
                #  Si ES Costos y Gastos por pagar va a esa cuenta (2335)
                accounting_record.puc = document_header.puc

            accounting_record.crossPrefix = document_header.controlPrefix
            accounting_record.crossDocument = document_header.controlNumber
            accounting_record.dueDate = payment_details.dueDate
            accounting_record.quoteNumber = payment_details.quoteNumber
            if account_type == "C":
                accounting_record.credit = float(payment_details.value)
            else:
                accounting_record.debit = float(payment_details.value)

            accounting_record.comments = payment_details.comments

            if (document_header.currency.currencyId != self.default_value.currency.currencyId \
                        and document_header.documentType.shortWord != "FPC"):
                accounting_record.puc = [p for p in self.list_puc if p.accountsPayableForeignProvider][0]

            accounting_record.foreignCurrency = _round(
                float(payment_details.value) / float(document_header.exchangeRate), 2)

            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

            return accounting_record

    def purchase_inventory(self, document_header=None, document_detail=None, decimal_value=None,
                           iva_tocost=False, account_type=None):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate

        # Marcela
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
            accounting_record.mainThirdId = document_header.third.thirdPartyId
            accounting_record.allThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.productionOrder = document_header.productionOrder

        #  Datos de detalle
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        accounting_record.itemId = document_detail.itemId

        # Tener en cuenta el inventario en consignación de proveedores
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            if document_detail.detailWarehouse and document_detail.detailWarehouse.typeWarehouse == "C":
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            elif account_type == "C":
                if document_detail.detailWarehouse.typeWarehouse == "C":
                    accounting_record.puc = document_detail.item.InventoryPUC
                else:
                    accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            else:
                accounting_record.puc = document_detail.item.inventoryPUC

        elif document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "P":

            if not document_detail.booleanValue:
                accounting_record.puc = document_detail.item.inventoryPUC
            else:
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignmentcustomer][0]

        elif document_header.documentType.shortWord == "FU" and document_detail.search == "Cost":
            accounting_record.puc = document_detail.item.costPUC
        else:
            accounting_record.puc = document_detail.item.inventoryPUC

        #
        if document_detail.detailWarehouse.typeWarehouse == "C" \
                and document_header.documentType.shortWord == "DR" \
                and document_header.sourceDocumentHeader \
                and document_header.isConsignment:

            accounting_record.warehouse = self.default_value.sourceWarehouse
        else:
            accounting_record.warehouse = document_detail.detailWarehouse

        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.ivaToCost = int(iva_tocost)
        accounting_record.consumptionToCost = document_detail.item.addConsumptionToCost
        accounting_record.baseValue = document_detail.baseValue

        if document_header.documentType.shortWord != "DR" \
                and document_header.sourceDocumentHeader \
                and document_header.sourceDocumentHeader.source.shortWord != "DR" \
                and document_detail.sourceDocumentDetail \
                and document_detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RP":

            accounting_record.quantity = 0
            accounting_record.units = 0
        else:

            accounting_record.quantity = 0 if iva_tocost else document_detail.quantity  # (IVAtocost == false ? document_detail.Quantity : 0)
            accounting_record.units = 0 if iva_tocost else document_detail.units  # (IVAtocost == false ? document_detail.Units : 0)

        if account_type == "C":
            accounting_record.credit = float(decimal_value)
            accounting_record.sign = "-" if document_detail.quantity > 0 and document_detail.value == 0 else "+"

            if document_header.documentType.shortWord == "TB" \
                    or document_header.documentType.shortWord == "TS":
                accounting_record.warehouse = document_header.sourceWarehous

        else:
            if document_header.documentType.shortWord == "TB":
                accounting_record.warehouse = document_detail.detailWarehouse

            if document_header.documentType.shortWord == "TS":
                accounting_record.warehouse = document_detail.detailWarehouse
                accounting_record.branch = document_header.destinyBranch

            accounting_record.debit = float(decimal_value)

        if document_detail.item:
            if document_detail.item.typeItem == "S":
                accounting_record.allThirdId = accounting_record.providerId if accounting_record.provider else \
                    accounting_record.customer.customerId if accounting_record.customer else \
                        accounting_record.otherThird.otherThirdId if accounting_record.otherThird else \
                            accounting_record.mainThird.thirdPartyId if accounting_record.mainThird else \
                                accounting_record.item.itemId

                accounting_record.allThirdType = "PR" if accounting_record.provider else \
                    "CU" if accounting_record.customer else \
                        "OT" if accounting_record.otherThird else \
                            "TP" if accounting_record.mainThird else \
                                "IT"
            else:
                accounting_record.allThirdId = document_detail.item.itemId
                accounting_record.itemId = document_detail.item.itemId
                accounting_record.allThirdType = "IT"

        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def sale_third_party(self, document_header=None, document_detail=None, decimal_value=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos del encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId

        accounting_record.dependency = document_header.dependency
        accounting_record.mainThird = document_header.financialEntity.thirdParty \
            if document_header.financialEntity else \
            document_header.customer.thirdParty if document_header.customer else \
                document_header.provider.thirdParty if document_header.provider else \
                    document_header.otherThird.thirdParty if document_header.otherThird else \
                        document_header.employee.thirdParty if document_header.employee else \
                            document_header.partner.thirdParty if document_header.partner else \
                                document_header.financialEntity.thirdParty if document_header.financialEntity else \
                                    document_header.third if document_header.third else None

        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.dueDate = document_header.documentDate
        # Agregar el Proveedor cuando es item en consignacion --Alejandro Adicionar traslado entre bodegas
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            accounting_record.providerId = document_header.sourceWarehouse.providerId
            accounting_record.mainThirdId = document_header.sourceWarehouse.provider.thirdPartyId
        else:
            accounting_record.providerId = document_detail.detailWarehouse.providerId \
                if document_detail.detailWarehouse.provider else document_header.providerId
            accounting_record.mainThirdId = document_detail.DetailWarehouse.provider.thirdPartyId \
                if document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty \
                else accounting_record.mainThirdId

        if document_detail.sourceDocumentDetail \
                and document_detail.sourceDocumentDetail.detailWarehouse \
                and document_detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":  # Factura de una remisión con la bodega de proveedor consignatario
            accounting_record.providerId = document_detail.sourceDocumentDetail.detailWarehouse.providerId
            accounting_record.mainThirdId = document_detail.sourceDocumentDetail.detailWarehouse.provider.thirdPartyId

        # Datos de detalle
        accounting_record.itemId = document_detail.item.itemId
        accounting_record.crossPrefix = document_detail.sourceDocumentPrefix \
            if document_detail.sourceDocumentPrefix else document_header.prefix
        accounting_record.crossDocument = document_detail.sourceDocumentNumber \
            if document_detail.sourceDocumentNumber else "RENUMBER"
        accounting_record.puc = [p for p in self.list_puc if p.saleByThirdParties][0]

        if account_type is "D":
            accounting_record.debit = float(document_header.total)
        else:
            accounting_record.credit = float(document_header.total)

        accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId
        accounting_record.allThirdType = "TP"
        accounting_record.comments = document_detail.comments

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def rete_ica(self,document_header = None, account_type=None):
        accounting_record = AccountingRecord()

        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThird = document_header.otherThird.thirdParty
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.allThirdId= document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        if document_header.financialEntity:
            accounting_record.mainThird = document_header.financialEntity.thirdParty
            accounting_record.allThirdId= document_header.financialEntity.thirdParty.thirdPartyId
            accounting_record.financialEntityId = document_header.financialEntityId
            accounting_record.allThirdType = "FE"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        # accounting_record.puc = document_header.reteICAPUC
        accounting_record.puc = [p for p in self.list_puc if p.reteICAPurchase][0]

        if document_header.overCostTaxBase and document_header.overCost > 0:
            accounting_record.baseValue = document_header.reteICABase + float(document_header.overCost)
        elif not document_header.overCostTaxBase:
            accounting_record.baseValue = document_header.reteICABase

        accounting_record.percentage = document_header.reteICAPercent
        if account_type == "C":
            accounting_record.credit = float(abs(document_header.reteICAValue))
        else:
            accounting_record.debit = float(abs(document_header.reteICAValue))

        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId
        return accounting_record

    def rete_iva(self,document_header = None, account_type=None):
        accounting_record = AccountingRecord()

        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdParty.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.allThirdId = document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        if document_header.financialEntity:
            accounting_record.mainThirdId = document_header.financialEntity.thirdParty.thirdPartyId
            accounting_record.allThirdId = document_header.financialEntity.thirdParty.thirdPartyId
            accounting_record.financialEntity = document_header.financialEntity
            accounting_record.allThirdType = "FE"


        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgent = document_header.businessAgent

        accounting_record.baseValue = document_header.reteIVABase
        accounting_record.percentage = document_header.reteIVAPercent

        # accounting_record.puc = document_header.reteIVAPUC
        if document_header.reteIVABase and document_header.reteIVABase > 0:
            if document_header.provider.thirdParty.ivaType and \
                            document_header.provider.thirdParty.ivaType.code == "C":
                accounting_record.puc = [p for p in self.list_puc if p.dianIVAChargeOfCommon][0]
            else:
                accounting_record.puc = [p for p in self.list_puc if p.dianIVAPurchasesOrServicesSimplifiedSystem][0]

        if account_type == "C":
            accounting_record.credit = float(abs(document_header.reteIVAValue))
        else:
            accounting_record.debit = float(abs(document_header.reteIVAValue))

        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId
        return accounting_record

    def assumed_iva(self,document_header = None, account_type=None):
        accounting_record = AccountingRecord()

        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId

        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.otherThird:
            accounting_record.mainThird = document_header.otherThird.thirdParty
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
            accounting_record.allThirdType = "OT"

        if document_header.third:
            accounting_record.allThirdId = document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdType = "TH"

        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.salesTaxPaidSimplifiedRegimen][0]

        accounting_record.baseValue = document_header.reteIVABase
        accounting_record.Percentage = document_header.reteIVAPercent
        if account_type == "C":
            accounting_record.credit = float(document_header.reteIVAValue)
        else:
            accounting_record.debit = float(document_header.reteIVAValue)

        accounting_record.crossDocumentHeaderId =  document_header.documentHeaderId
        return accounting_record

    def withholding_tax(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"
        if document_header.customer:
            accounting_record.mainThird = document_header.customer.thirdParty
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId= document_header.customerId
            accounting_record.allThirdType = "CU"
        if document_header.otherThird:
            accounting_record.mainThird = document_header.otherThird.thirdParty
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId= document_header.otherThirdId
            accounting_record.allThirdType = "OT"
        if document_header.third:
            accounting_record.allThirdId= document_header.third.thirdPartyId
            accounting_record.mainThirdId = document_header.thirdId
            accounting_record.allThirdTyope = "TH"
        if document_header.financialEntity:
            accounting_record.mainThird = document_header.financialEntity.thirdParty
            accounting_record.allThirdId= document_header.financialEntity.thirdParty.thirdPartyId
            accounting_record.financialEntity = document_header.financialEntity
            accounting_record.allThirdtype = "FE"
        if document_header.employee:
            if document_header.search != "RC":
                accounting_record.mainThird = document_header.employee.thirdParty
                accounting_record.allThirdId= document_header.employee.thirdParty.thirdPartyId

                accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = document_header.withholdingTaxPUCId
        accounting_record.puc = document_header.withholdingTaxPUC
        accounting_record.baseValue = document_header.withholdingTaxBase
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue -= document_header.disccount2Value
        if document_header.withholdingTaxPercent:
            accounting_record.percentage = document_header.withholdingTaxPercent
        elif not document_header.withholdingTaxPercent and accounting_record.puc.percentage != 0:
            accounting_record.percentage = accounting_record.puc.percentage
        if account_type == "C":
            accounting_record.credit = float(document_header.withholdingTaxValue)
        else:
            accounting_record.debit = float(document_header.withholdingTaxValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def withholding_cree(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId= document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = document_header.withholdingCREEPUCId
        accounting_record.baseValue = document_header.baseCREE
        if document_header.percentageCREE:
            accounting_record.percentage = document_header.percentageCREE
        if account_type == "C":
            accounting_record.credit = float(document_header.valueCREE)
        else:
            accounting_record.debit = float(document_header.valueCREE)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def direct_iva(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThird = document_header.provider.thirdPartyId
        accounting_record.providerId = document_header.providerId
        accounting_record.importId = document_header.importId
        if document_header.ivaPUC:
            accounting_record.puc = document_header.ivaPUC
        else:
            accounting_record.puc = [p for p in self.list_puc if p.importsIVA][0]
        accounting_record.baseValue = ((document_header.directIVA * 100) / (document_header.directIVAPercent))
        accounting_record.percentage = document_header.directIVAPercent
        if account_type == "C":
            accounting_record.credit = float(document_header.directIVA)
        else:
            accounting_record.debit = float(document_header.directIVA)
        accounting_record.allThirdId = document_header.providerId
        accounting_record.allThirdType = "PR"
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def other_retentions(self, document_header=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.prefix = document_header.prefix
        # accounting_record.crossDocument = documentHeader.documentNumber
        accounting_record.crossDocument = "RENUMBER"
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        if document_header.provider:
            accounting_record.mainThird = document_header.provider.thirdParty
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.pucId = document_header.retentionPUCId
        accounting_record.baseValue = document_header.retentionBase
        accounting_record.percentage = document_header.retentionPercent
        if account_type == "C":
            accounting_record.credit = float(document_header.retentionValue)
        else:
            accounting_record.debit = float(document_header.retentionValue)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def expenses_puc(self, puc_exp=None, document_header=None, *params):
        if puc_exp and puc_exp.deferredInterest and puc_exp.deferredIncome:
            return puc_exp
        if len(params) < 1:
            return puc_exp
        level = self.default_value.branch.company.expenseLevel
        puc =  {
            'D':params[1].puc if len(params) > 1 and params[1] else None, # División
            'S':params[2].puc if len(params) > 2 and params[2] else None, # Sección
            'P':params[3].puc if len(params) > 3 and params[3] else None, # Dependencia
        }.get(level)
        if puc:
            pu = [p for p in self.list_puc if p.costCenter and
                  p.pucClass + p.pucSubClass == puc_exp.pucClass + puc_exp.pucSubClass]
            if pu and len(pu) > 0:
                oPUC = [p for p in self.list_puc if
                        p.pucClass == puc.pucClass and p.pucSubClass == puc.pucSubClass and
                        p.account == puc_exp.account and p.subAccount == puc_exp.subAccount and
                        p.auxiliary1 == puc_exp.auxiliary1]
                if oPUC and len(oPUC) > 0:
                    return oPUC[0]
                else:
                    error ={
                        2: ValueError("Centro C: " + params[0].Name + "\n División: " + params[1].Name +
                                      "\nNo se ha encontrado la cuenta: "+puc.PUCClass + puc.PUCSubclass +
                                      puc_exp.Account + puc_exp.Subaccount + puc_exp.Auxiliary1 + " - " + puc_exp.Name+
                                      "\nNo se puede guardar el documento. Verifique la parametrización\n\n"),

                        3: ValueError("Centro C: " + params[0].Name + "\n División: " + params[1].Name +
                                      "\nSección:  " + params[2].Name + "\nNo se ha encontrado la cuenta: " +
                                      puc.PUCClass + puc.PUCSubclass + puc_exp.Account + puc_exp.Subaccount +
                                      puc_exp.Auxiliary1 + " - " + puc_exp.Name+
                                      "\nNo se puede guardar el documento. Verifique la parametrización\n\n"),

                        4: ValueError("Centro C: " + params[0].Name + "\n División: " + params[1].Name +
                                      "\nSección:  " + params[2].Name + "\nDependencia: " + params[3].Name +
                                      "\nNo se ha encontrado la cuenta: "+puc.PUCClass + puc.PUCSubclass +
                                      puc_exp.Account + puc_exp.Subaccount + puc_exp.Auxiliary1 + " - " + puc_exp.Name+
                                      "\nNo se puede guardar el documento. Verifique la parametrización\n\n"),
                    }
                    raise error.get(len(params))