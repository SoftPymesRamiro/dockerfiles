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

class AdvanceCustomerAccounting(object):

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
            # // Retefuente
            if document_header.withholdingTaxValue > 0:
                self.ret_value.append(self.withholding_tax(document_header, "D"))

            # // ReteICA
            if document_header.reteICAValue > 0:
                self.ret_value.append(self.rete_ica(document_header, "D"))
            #
            # // ReteIVA
            if document_header.reteIVAValue > 0:
                self.ret_value.append(self.rete_iva(document_header, "D"))
            #
            # # // Total Avance
            self.ret_value.append(self.customer_advance(document_header, "C"))
            # Pago del avance
            p_accounting = PaymentAccounting(document_header)
            p_accounting.execute_payment(document_header=document_header, payment_receipt=payment_receipt,
                                         ret_value=self.ret_value, account_type="D")
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def rete_ica(self,document_header = None, account_type=None):
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
        if document_header.reteIVABase > 0:
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

    def withholding_tax(self, document_header=None, account_type=None):
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

        accounting_record.baseValue = document_header.withholdingTaxBase
        if document_header.disccount2TaxBase and document_header.disccount2Value > 0:
            accounting_record.baseValue -= document_header.disccount2Value

        if document_header.withholdingTaxPercent:
            accounting_record.percentage = document_header.withholdingTaxPercent

        elif not document_header.withholdingTaxPercent and accounting_record.puc.Ppercentage != 0:
            accounting_record.Percentage = accounting_record.puc.Percentage

        if account_type == "C":
            accounting_record.credit = float(document_header.withholdingTaxValue)
        else:
            accounting_record.debit = float(document_header.withholdingTaxValue)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def customer_advance(self,document_header=None, account_type=None):
        """

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
        accounting_record.pucId = document_header.pucId
        accounting_record.crossPrefix = document_header.prefix
        accounting_record.crossDocument = "RENUMBER"

        accounting_record.foreignCurrency = round((document_header.subtotal / document_header.exchangeRate), 2)
        if account_type == "C":
            accounting_record.credit = document_header.subtotal
        else:
            accounting_record.debit = document_header.subtotal

        accounting_record.allThirdId = document_header.customer.customerId
        accounting_record.allThirdType = "CU"

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record
