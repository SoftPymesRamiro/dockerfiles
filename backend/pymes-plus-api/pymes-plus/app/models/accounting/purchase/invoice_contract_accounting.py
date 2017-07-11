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
from ....utils.math_ext import _round
from ..payment_accounting import PaymentAccounting
from .purchase_functions import PurchaseFunctions
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError

class InvoiceContractAccounting(object):
    """ """
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
        self.p_functions = PurchaseFunctions(document_header, list_puc = self.list_puc)

    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        try:
            # Calculo de TOTALES
            if document_header.subtotal > 0:
                self.ret_value.append(self.contract_provider(document_header=document_header,
                                                             round_decimals=self.round_decimals,
                                                             account_type="D"))
            #  descuento en compras
            if document_header.disccount and document_header.disccount > 0:
                discount_purchase = 0
                for detail in document_header.documentDetails:
                    if detail.item and detail.item.disccountToUnitValue:
                        discount_purchase += _round(detail.value * detail.disccount / 100, self.round_decimals)
                self.ret_value.append(self.p_functions.purchase_discount(document_header=document_header,
                                                                         discount_purchase=discount_purchase,
                                                                         round_decimals=self.round_decimals,
                                                                         account_type="C"))
            # descuento en compras 2
            if document_header.disccount2Value and float(document_header.disccount2Value) > 0:
                self.ret_value.append(self.p_functions.purchase_other_discount(document_header=document_header,
                                                                              round_decimals=self.round_decimals,
                                                                              account_type="C"))
            # intereses
            if document_header.interest and float(document_header.interest) > 0:
                self.ret_value.append(self.p_functions.interest_expense(document_header=document_header,
                                                                        account_type="D"))
            # seguros
            if document_header.insurance and float(document_header.insurance) > 0:
                self.ret_value.append(self.insurance_expense(document_header=document_header,account_type="D"))
            # fletes
            if document_header.freight and float(document_header.freight) > 0:
                self.ret_value.append(self.freight_expense(document_header=document_header,account_type="D"))
            # IVA
            if document_header.ivaValue and float(document_header.ivaValue) > 0:
                self.ret_value.append(self.p_functions.IVA(document_header=document_header,
                                               round_decimals=self.round_decimals, account_type="D"))
            # Retefuente
            if document_header.withholdingTaxPUCId and document_header.withholdingTaxValue \
                    and document_header.withholdingTaxValue > 0:
                self.ret_value.append(self.p_functions.withholding_tax(document_header=document_header,
                                                                       account_type="C"))
            # ReteICA
            if document_header.reteICAValue and document_header.reteICAValue > 0:
                self.ret_value.append(self.p_functions.rete_ica(document_header=document_header,
                                                          account_type="C"))
            # ReteIVA
            if document_header.reteIVAValue and document_header.reteIVAValue > 0:
                if not document_header.assumedIVA:
                    self.ret_value.append(self.p_functions.rete_iva(document_header=document_header,
                                                          account_type="C"))
                else:
                    # // IVA Asumido Régimen Simplificado
                    # if document_header.reteIVAPUC:
                    self.ret_value.append(self.p_functions.rete_iva(document_header=document_header,
                                                                    account_type="C"))
                    self.ret_value.append(self.p_functions.assumed_iva(document_header=document_header,
                                                                       account_type="D"))
            # // IVA Directo
            if document_header.directIVA and document_header.directIVA > 0:
                self.ret_value.append(self.p_functions.direct_iva(document_header=document_header,
                                                          account_type="D"))
            # // Otras Retenciones
            if document_header.retentionValue and document_header.retentionValue > 0:
                self.ret_value.append(self.p_functions.other_retentions(document_header=document_header,
                                                          account_type="C"))
            # // Retención CREE
            if document_header.valueCREE > 0:
                self.ret_value.append(self.p_functions.withholding_cree(document_header=document_header,
                                                          account_type="C"))
            if document_header.paymentTerm and document_header.paymentTerm.needTermDays:
                # // Pago a CREDITO
                self.ret_value.append(self.p_functions.provider_payable(document_header=document_header,
                                                            account_type="C"))
            elif document_header.paymentTerm and document_header.paymentTerm.quota:
                if payment_receipt.firstValue and payment_receipt.firstValue > 0:
                    self.ret_value.append(self.p_functions.provider_payable(document_header=document_header,
                                                          payment_receipt=payment_receipt,
                                                          account_type="C"))
                # // Pago por CUOTAS
                for paymentdetail in payment_receipt.paymentDetails:
                    self.ret_value.append(self.p_functions.provider_payable(document_header=document_header,
                                                                            payment_details=paymentdetail,
                                                                            account_type="C"))
            else:
                # // Pago de CONTADO
                p_accounting = PaymentAccounting(document_header)
                p_accounting.execute_payment(document_header=document_header,
                                          payment_receipt=payment_receipt,
                                          ret_value=self.ret_value)
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def contract_provider(self, document_header=None, round_decimals=None, account_type=None):
        """

        :param document_header:
        :param round_decimals:
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

    def insurance_expense(self, document_header=None, account_type=None):
        """

        :param document_header:
        :param account_type:
        :return:
        """
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
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.insurance][0]
        accounting_record.puc = self.p_functions.expenses_puc(accounting_record.puc,
                                                              document_header,
                                                              document_header.costCenter,
                                                              document_header.division,
                                                              document_header.section,
                                                              document_header.dependency)
        if account_type == "C":
            accounting_record.credit = float(document_header.insurance)
        else:
            accounting_record.debit = float(document_header.insurance)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record

    def freight_expense(self, document_header=None, account_type=None):
        """

        :param document_header:
        :param account_type:
        :return:
        """
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
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"
        accounting_record.employeeId = document_header.employeeId
        accounting_record.puc = [p for p in self.list_puc if p.freightPurchases][0]
        accounting_record.puc = self.p_functions.expenses_puc(accounting_record.puc,
                                                              document_header,
                                                              document_header.costCenter,
                                                              document_header.division,
                                                              document_header.section,
                                                              document_header.dependency)
        if account_type == "C":
            accounting_record.credit = float(document_header.freight)
        else:
            accounting_record.debit = float(document_header.freight)
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record
