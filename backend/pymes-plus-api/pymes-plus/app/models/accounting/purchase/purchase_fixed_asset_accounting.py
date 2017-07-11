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

class PurchaseFixedAssetAccounting(object):
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
        self.p_functions = PurchaseFunctions(document_header, self.list_puc, self.default_value, self.general_parameter)


    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            self.expenses = document_header.expenses if document_header.expenses is not None else 0
            # Recorrido de detalles
            if self.total_records > 0:
                total_cost = 0
                total_disccount = 0
                total_disccount2 = 0
                for detail in document_details:
                    # Calcula el sobre costo y el descuento para el activo
                    # los detalles
                    self.overcost = 0 if document_header.subtotal == 0 else _round(
                        float(document_header.overCost) * (detail.value / document_header.subtotal), self.round_decimals)
                    self.discount2 = 0 if document_header.subtotal == 0 else _round(
                        float(document_header.disccount2Value) * (detail.value / document_header.subtotal),
                        self.round_decimals)
                    # Si es el ultimo registro debe acomodar el saldo
                    # re calcula el sobrecosto y el descuento para este activo
                    # en la v1  es recordnumber < totalrecord
                    if detail == document_details[-1]:
                        self.overcost = document_header.overCost - total_cost
                        self.discount2 = document_header.disccount2Value - total_disccount2

                    self.discount = 0
                    # Activos
                    self.ret_value.append(self.purchase_asset(document_header=document_header,
                                                                 document_detail=detail,
                                                                 decimal_value=(detail.value + self.overcost - self.discount),
                                                                 account_type='D'))

                    # IVA en compras
                    if detail.value and detail.value > 0 and detail.ivaPUC:
                        self.ret_value.append(self.detail_iva(document_header=document_header,
                                                              document_detail=detail,
                                                              overcost=self.overcost,
                                                              discount=self.discount,
                                                              discount2=self.discount2,
                                                              decimal_values=self.round_decimals,
                                                              account_type="D"))
                    # Impuesto al Consumo
                    if detail.consumptionTaxPercent and detail.consumptionTaxBase and \
                            detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                        self.ret_value.append(self.purchase_consumptionTax(document_header=document_header,
                                                                           document_detail=detail,
                                                                           decimal_values=self.round_decimals,
                                                                           account_type="D"))
                    # Retefuente en compras
                    if detail.withholdingTax and detail.value and \
                                    detail.withholdingTax > 0 and (detail.value > 0):
                        self.ret_value.append(self.detail_withholdingTax(document_header=document_header,
                                                                         document_detail=detail,
                                                                         overcost=self.overcost,
                                                                         discount=self.discount,
                                                                         discount2=self.discount2,
                                                                         decimal_values=self.round_decimals,
                                                                         account_type="C"))

                total_cost += self.overcost
                total_disccount += self.discount
                total_disccount2 += self.discount2
            # TODO calculo de TOTALES
            #  descuento en compras
            if document_header.disccount and document_header.disccount > 0:
                discount_purchase = 0
                self.ret_value.append(self.p_functions.purchase_discount(document_header=document_header,
                                                                         discount_purchase=discount_purchase,
                                                                         round_decimals=self.round_decimals,
                                                                         account_type="C"))
            # descuento en compras 2
            if document_header.disccount2Value and document_header.disccount2Value > 0:
                self.ret_value.append(self.p_functions.purchase_other_discount(document_header=document_header,
                                                                              round_decimals=self.round_decimals,
                                                                              account_type="C"))
            # intereses
            if document_header.interest and document_header.interest > 0:
                self.ret_value.append(self.p_functions.interest_expense(document_header=document_header,
                                                                        account_type="D"))
            # seguros
            if document_header.insurance and document_header.insurance > 0:
                self.ret_value.append(self.p_functions.insurance_expense(document_header=document_header,
                                                                         account_type="D"))
            # fletes
            if document_header.freight and document_header.freight > 0:
                self.ret_value.append(self.p_functions.freight_expense(document_header=document_header,
                                                                       account_type="D"))
            # Retefuente
            if document_header.withholdingTaxPUC and document_header.withholdingTaxValue > 0:
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


    def purchase_asset(self, document_header=None, document_detail=None, decimal_value=None,
                           iva_tocost=False, account_type=None):
        """

        :param document_header:
        :param document_detail:
        :param decimal_value:
        :param iva_tocost:
        :param account_type:
        :return: accounting record object
        """
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate

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

        accounting_record.assetId = document_detail.assetId
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.quantity = document_detail.quantity
        accounting_record.pucId = document_detail.asset.pucId
        accounting_record.units = document_detail.units

        if account_type == "C":
            accounting_record.credit = decimal_value
        else:
            accounting_record.debit = decimal_value

        accounting_record.allThirdId = document_detail.assetId
        accounting_record.allThirdType = 'AS'
        accounting_record.comments = document_detail.comments

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record


    def detail_iva(self, document_header=None, document_detail=None, overcost=None, discount=None,
                   discount2=None, decimal_values=None, account_type=None):
        """

        :param document_header:
        :param document_detail:
        :param overcost:
        :param discount:
        :param discount2:
        :param decimal_values:
        :param account_type:
        :return: accounting record object
        """
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
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

        # // Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.pucId = document_detail.ivaPUCId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId

        if not document_header.overCostTaxBase:
                accounting_record.baseValue = _round(document_detail.baseValue - discount -
                                            _round(document_detail.baseValue * document_detail.disccount / 100,
                                                   self.round_decimals),
                                                     self.round_decimals)

        accounting_record.percentage = document_detail.iva
        # accounting_record.baseValue = document_detail.baseValueIVA
        accounting_record.baseValue = document_detail.baseValue

        if account_type == "C":
            accounting_record.credit = float(
                _round(accounting_record.baseValue * document_detail.iva / 100, self.round_decimals))
        else:
            accounting_record.debit = float(
                _round(accounting_record.baseValue * document_detail.iva / 100, self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record

    def detail_withholdingTax(self, document_header=None, document_detail=None, overcost=None, discount=None,
                                  discount2=None, decimal_values=None, account_type=None):
        """

        :param document_header:
        :param document_detail:
        :param overcost:
        :param discount:
        :param discount2:
        :param decimal_values:
        :param account_type:
        :return: accounting record object
        """
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

        # //Datos de detalle
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

                accounting_record.baseValue = _round(document_detail.baseValue - discount - \
                           _round(document_detail.baseValue * document_detail.disccount / 100, self.round_decimals),
                           self.round_decimals)

        accounting_record.percentage = document_detail.withholdingTax
        # accounting_record.baseValue = document_detail.baseValueIVA
        accounting_record.baseValue = document_detail.baseValue

        if account_type == "C":
            accounting_record.credit = float(
                _round(accounting_record.baseValue * document_detail.withholdingTax / 100, self.round_decimals))
        else:
            accounting_record.debit = float(
                _round(accounting_record.baseValue * document_detail.withholdingTax / 100, self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record


    def purchase_consumptionTax(self, document_header=None, document_detail=None,
                                decimal_values=None, account_type=None):
        """

        :param document_header:
        :param document_detail:
        :param decimal_values:
        :param account_type:
        :return: accounting record object
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

        # //Datos de detalle
        accounting_record.itemId = document_detail.itemId
        accounting_record.assetId = document_detail.assetId
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.sizeId = document_detail.sizeId
        accounting_record.colorId = document_detail.colorId
        accounting_record.measurementUnitId = document_detail.measurementUnitId
        accounting_record.baseValue = document_detail.consumptionTaxBase
        accounting_record.percentage = document_detail.consumptionTaxPercent
        accounting_record.pucId =  document_detail.consumptionTaxPUCId

        if account_type == "C":
            accounting_record.credit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                    self.round_decimals))
        else:
            accounting_record.debit = float(_round(accounting_record.baseValue * (accounting_record.percentage / 100),
                                                   self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record