# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 29-11-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David, JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import _round
import copy

from ....exceptions import InternalServerError
from datetime import timedelta
from ..payment_accounting import PaymentAccounting
from .purchase_functions import PurchaseFunctions
from datetime import *

class PurchaseItemAccounting(object):
    """

    """
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
        self.p_functions = PurchaseFunctions(document_header, self.list_puc, self.default_value, self.general_parameter)

    @staticmethod
    def export_data(data):
        """
            Allow export an accounting record object
            :return:  Document header object in JSon format
        """
        return {
            'accountingRecordId': data.accountingRecordId,
            'customerId': data.customerId,
            'contractId': data.contractId,
            'payrollConceptId': data.payrollConceptId,
            'businessAgentId': data.businessAgentId,
            'productionOrderId': data.productionOrderId,
            'allThirdId': data.allThirdId,
            'otherThirdId': data.otherThirdId,
            'payrollEntityId': data.payrollEntityId,
            'dependencyId': data.dependencyId,
            'warehouseId': data.warehouseId,
            'mainThirdId': data.mainThirdId,
            'pucId': data.pucId,
            'importId': data.importId,
            'providerId': data.providerId,
            'measurementUnitId': data.measurementUnitId,
            'stageId': data.stageId,
            'sizeId': data.sizeId,
            'divisionId': data.divisionId,
            'cashRegisterId': data.cashRegisterId,
            'colorId': data.colorId,
            'partnerId': data.partnerId,
            'pieceId': data.pieceId,
            'itemId': data.itemId,
            'roleEmployeeId': data.roleEmployeeId,
            'bankAccountId': data.bankAccountId,
            'cashierId': data.cashierId,
            'employeeId': data.employeeId,
            'financialEntityId': data.financialEntityId,
            'documentTypeId': data.documentTypeId,
            'sourceDocumentTypeId': data.sourceDocumentTypeId,
            'branchId': data.branchId,
            'sectionId': data.sectionId,
            'costCenterId': data.costCenterId,
            'documentHeaderId': data.documentHeaderId,
            'crossDocumentHeaderId': data.crossDocumentHeaderId,
            'assetId': data.assetId,
            'accountingDate': data.accountingDate,
            'dueDate': data.dueDate,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'transfered': data.transfered,
            'ivaToCost': data.ivaToCost,
            'niif': data.niif,
            'consumptionToCost': data.consumptionToCost,
            'apportionment': data.apportionment,
            'foreignCurrency': data.foreignCurrency,
            'quantity': data.quantity,
            'simulatedQuantity': data.simulatedQuantity,
            'units': data.units,
            'balance': data.balance,
            'baseValue': data.baseValue,
            'percentage': data.percentage,
            'debit': data.debit,
            'simulatedDebit': data.simulatedDebit,
            'credit': data.credit,
            'simulatedCredit': data.simulatedCredit,
            'documentPrefix': data.documentPrefix,
            'documentNumber': data.documentNumber,
            'crossPrefix': data.crossPrefix,
            'crossDocument': data.crossDocument,
            'lot': data.lot,
            'sourcePrefix': data.sourcePrefix,
            'bankName': data.bankName,
            'cardNumber': data.cardNumber,
            'sign': data.sign,
            'sourceDocument': data.sourceDocument,
            'comments': data.comments,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'accountNumber': data.accountNumber,
            'bankCode': data.bankCode,
            'quoteNumber': data.quoteNumber,
            'provider': None if data.provider is None else data.provider.export_data_simple(data.provider),
            'item': None if data.item is None else data.item.export_simple(),
        }

    def add_days(self, date, days):
        for i in range(days):
            date += timedelta(days=1)

        return date

    def do_account(self, document_header=None, document_details=None, payment_receipt =None):
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
                    # Calcula el sobre costo y el descuento para el item
                    # los detalles
                    self.overcost = 0 if document_header.subtotal == 0 else _round(document_header.overCost * (detail.value /document_header.subtotal), self.round_decimals)
                    self.discount2 = 0 if document_header.subtotal == 0 else _round(document_header.disccount2Value * (detail.value /document_header.subtotal), self.round_decimals)

                    # Si es el ultimo registro debe acomodar el saldo
                    # re calcula el sobrecosto y el descuento para este item
                    # en la v1  es recordnumber < totalrecord
                    if detail == document_details[-1]:
                        self.overcost = document_header.overCost - total_cost
                        self.discount2 = document_header.disccount2Value - total_disccount2

                    # Calculo el valor del descuento
                    # El descuento afecta el detalle
                    if detail.item and detail.item.disccountToUnitValue:
                        self.discount = _round(detail.value * detail.disccount / 100, self.round_decimals)
                    else:
                        self.discount = 0

                    # Valida que la bodega
                    if detail.detailWarehouse.typeWarehouse == 'C' or detail.detailWarehouse.typeWarehouse == 'P':
                        # si es bodega cosignataria
                        # Articulo en consignacion
                        self.ret_value.append(self.sale_third_party(document_header=document_header,
                                                                    document_detail=detail,
                                                                    decimal_value=(detail.value + self.overcost - self.discount),
                                                                    account_type='D'))
                    # Inventario
                    else:
                        # Si el documento origen es RP, remision y el ShortWord es FRP (Remisión Global) y esto tiene sobrecostos.
                        if detail.sourceDocumentDetail is None or \
                                (detail.sourceDocumentDetail and (detail.sourceDocumentDetail.documentHeader.documentType is None
                                                                  or (detail.sourceDocumentDetail.documentHeader.documentType and
                                      not (detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RP" or
                                                   detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "FRP") and
                        not (document_header.sourceDocumentType.shortWord == "OP" and document_header.source.shortWord == "FRP")))):

                            self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                          document_detail=detail,
                                                                          decimal_value=(detail.value + self.overcost - self.discount),
                                                                          account_type="D"))
                        else:

                            if ((document_header.sourceDocumentType and
                                     (document_header.sourceDocumentType.shortWord == "RP" or
                                              document_header.sourceDocumentType.shortWord == "FRP")) and self.overcost > 0):
                                    self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                                  document_detail=detail,
                                                                                  decimal_value=self.overcost,
                                                                                  account_type="D"))

                            elif (detail.sourceDocumentDetail and (detail.sourceDocumentDetail.documentHeader.documentType and
                                                            (detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RP"
                                                             and document_header.source.shortWord == "FRP")) and self.overcost > 0):
                                self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                              document_detail=detail,
                                                                              decimal_value=self.overcost,
                                                                              account_type="D"))
                    # Cuando la FP es con base en una remisión, se debe enviar como parámetro el documentnumber de la remisión
                    # La fecha de contabiización debe quedar con la fecha de la FP y no de la remisión
                    if detail.sourceDocumentDetail and detail.sourceDocumentDetail.documentHeader \
                        and detail.sourceDocumentDetail.documentHeader.documentType \
                            and (detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "RP" or
                                     detail.sourceDocumentDetail.documentHeader.documentType.shortWord == "OP"
                                 and document_header.source.shortWord == "FRP"):

                        d_header = copy.copy(detail.sourceDocumentDetail.documentHeader)
                        d_header.documentDate = document_header.documentDate
                        self.ret_value.append(self.p_functions.provider_payable(document_header=d_header,
                                                                    decimal_value=(detail.value - self.discount),
                                                                    account_type="D", is_renumber=False))
                    # IVA en compras
                    if detail.item and detail.baseValue > 0 and detail.ivaPUC:
                        if detail.item.addIVAtoCost:
                            decimal_value = _round(detail.baseValue * (detail.iva / 100), self.round_decimals)
                            self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                          document_detail=detail,
                                                                          decimal_value=decimal_value,
                                                                          iva_tocost=True,
                                                                          account_type="D"))
                        else:
                            self.ret_value.append(self.detail_iva(document_header=document_header,
                                                                  document_detail=detail,
                                                                  overcost=self.overcost,
                                                                  discount=self.discount,
                                                                  discount2=self.discount2,
                                                                  decimal_values=self.round_decimals,
                                                                  account_type="D"))
                    # Impuesto al consumo
                    if detail.item and detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                        if detail.item.addIVAtoCost or detail.item.addConsumptionToCost:
                            decimal_value = _round(detail.consumptionTaxBase * (detail.consumptionTaxPercent / 100),
                                                   self.round_decimals)
                            self.ret_value.append(self.purchase_inventory(document_header=document_header,
                                                                          document_detail=detail,
                                                                          decimal_value=decimal_value,
                                                                          iva_tocost=True,
                                                                          account_type="D"))
                        else:
                            self.ret_value.append(self.purchase_consumptionTax(document_header=document_header,
                                                                               document_detail=detail,
                                                                               decimal_values=self.round_decimals,
                                                                               account_type="D"))

                    # Rete fuetne en compras
                    if detail.withholdingTax > 0 and (detail.value > 0):
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
                for detail in document_header.documentDetails:
                    if detail.item and detail.item.disccountToUnitValue:
                        discount_purchase += _round(detail.value * detail.disccount / 100, self.round_decimals)

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
                p_accounting.execute_payment(document_header=document_header, payment_receipt=payment_receipt,
                                             ret_value=self.ret_value, account_type="C")

            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def purchase_consumptionTax(self, document_header=None, document_detail=None,
                                decimal_values=None, account_type=None):
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # //Datos de Encabezado
        accounting_record.branch = document_header.branch
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenter = document_header.costCenter
        accounting_record.division = document_header.division
        accounting_record.section = document_header.section
        accounting_record.dependency = document_header.dependency

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
        accounting_record.item = document_detail.item
        accounting_record.asset = document_detail.asset
        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.size = document_detail.size
        accounting_record.color = document_detail.color
        accounting_record.measurementUnit = document_detail.measurementUnit
        accounting_record.baseValue = document_detail.consumptionTaxBase
        accounting_record.percentage = document_detail.consumptionTaxPercent
        accounting_record.puc = document_detail.item.consumptionPUC \
            if document_detail.item else document_detail.consumptionTaxPUC

        if account_type == "C":
            accounting_record.credit = float(
                _round(accounting_record.baseValue * (accounting_record.percentage / 100),
                       self.round_decimals))
        else:
            accounting_record.debit = float(
                _round(accounting_record.baseValue * (accounting_record.percentage / 100),
                       self.round_decimals))

        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId.documentHeaderId \
            if document_detail.crossDocumentHeader else document_header.documentHeaderId

        return accounting_record


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
            accounting_record.providerId = document_header.providerId
            accounting_record.allThirdId = document_header.providerId
            accounting_record.allThirdType = "PR"

        if document_header.customer:
            accounting_record.mainThirdId = document_header.customer.thirdPartyId
            accounting_record.customerId = document_header.customerId
            accounting_record.allThirdId = document_header.customerId
            accounting_record.allThirdType = "CU"

        if document_header.employee:
            accounting_record.mainThirdId = document_header.employee.thirdPartyId
            accounting_record.employeeId = document_header.employeeId
            accounting_record.allThirdId = document_header.employee.employeeId
            accounting_record.allThirdType = "EM"

        if document_header.otherThird:
            accounting_record.mainThirdId = document_header.otherThird.thirdPartyId
            accounting_record.otherThirdId = document_header.otherThirdId
            accounting_record.allThirdId = document_header.otherThirdId
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
            accounting_record.debit = float(document_header.total)
        else:
            accounting_record.credit = float(document_header.total)

        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId

        return accounting_record

    def purchase_inventory(self, document_header=None, document_detail=None, decimal_value=None,
                           iva_tocost=False, account_type=None):
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # FIXME accounting_record.branch = document_header.branch
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate

        # //Marcela
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

        # // Datos de detalle
        accounting_record.costCenter = document_detail.costCenter
        accounting_record.division = document_detail.division
        accounting_record.section = document_detail.section
        accounting_record.dependency = document_detail.dependency
        accounting_record.item = document_detail.item

        # //Tener en cuenta el inventario en consignación de proveedores
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            if document_detail.detailWarehouse and document_detail.detailWarehouse.typeWarehouse == "C":
                accounting_record.puc = [p for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            elif account_type == "C":
                if document_detail.detailWarehouse.typeWarehouse == "C":
                    accounting_record.puc = document_detail.item.inventoryPUC
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

        # //
        if document_detail.detailWarehouse.typeWarehouse == "C" \
                and document_header.documentType.shortWord == "DR" \
                and document_header.sourceDocumentHeader \
                and document_header.isConsignment:

            accounting_record.warehouse = self.default_value.sourceWarehouse
        else:
            accounting_record.warehouse = document_detail.detailWarehouse

        accounting_record.lot = document_detail.lot
        accounting_record.dueDate = document_detail.dueDate
        accounting_record.size = document_detail.size
        accounting_record.color = document_detail.color
        accounting_record.measurementUnit = document_detail.measurementUnit
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
                # TODO Guardar en el campo allThird  el tercero en caso de que sea un item de servicio

                accounting_record.allThirdId = accounting_record.providerId if accounting_record.provider else \
                    accounting_record.customerId if accounting_record.customer else \
                        accounting_record.otherThirdId if accounting_record.otherThird else \
                            accounting_record.mainThirdId if accounting_record.mainThirdId else \
                                accounting_record.item.itemId

                accounting_record.allThirdType = "PR" if accounting_record.provider else \
                    "CU" if accounting_record.customer else \
                        "OT" if accounting_record.otherThird else \
                            "TH" if accounting_record.mainThirdId else \
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
        """

        :return:
        """
        accounting_record = AccountingRecord()
        # Datos del encabezado
        accounting_record.branch = document_header.branch
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenter = document_header.costCenter
        accounting_record.division = document_header.division
        accounting_record.section = document_header.section

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
        accounting_record.businessAgent = document_header.businessAgent
        accounting_record.dueDate = document_header.documentDate
        # //Agregar el Proveedor cuando es item en consignacion --Alejandro //Adicionar traslado entre bodegas
        if document_header.documentType.shortWord == "TB" \
                and document_header.sourceWarehouse \
                and document_header.sourceWarehouse.typeWarehouse == "C":

            accounting_record.providerId = document_header.sourceWarehouse.provider
            accounting_record.mainThird = document_header.sourceWarehouse.provider.thirdParty
        else:
            accounting_record.providerId = document_detail.detailWarehouse.providerId \
                if document_detail.detailWarehouse.providerId else document_header.providerId
            accounting_record.mainThirdId = document_detail.detailWarehouse.provider.thirdPartyId \
                if document_detail.detailWarehouse.provider and document_detail.detailWarehouse.provider.thirdParty \
                else accounting_record.mainThirdId

        if document_detail.sourceDocumentDetail \
                and document_detail.sourceDocumentDetail.detailWarehouse \
                and document_detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":  # //Factura de una remisión con la bodega de proveedor consignatario
            accounting_record.providerId = document_detail.sourceDocumentDetail.detailWarehouse.providerId
            accounting_record.mainThird = document_detail.sourceDocumentDetail.detailWarehouse.provider.thirdParty

        # //Datos de detalle
        accounting_record.item = document_detail.item
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

    def detail_withholdingTax(self, document_header=None, document_detail=None, overcost=None, discount=None,
                              discount2=None, decimal_values=None, account_type=None):
        """

        :return:
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

            if document_header.source.shortWord in ("FPD", "FPI", "FPC", "FPA", "FM", "FME"):
                accounting_record.baseValue = \
                    _round(document_detail.baseValue - discount -
                           _round(document_detail.baseValue * document_detail.disccount / 100, self.round_decimals),
                           self.round_decimals)

        accounting_record.percentage = document_detail.withholdingTax
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

    def detail_iva(self, document_header=None, document_detail=None, overcost=None, discount=None,
                   discount2=None, decimal_values=None, account_type=None):
        """

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

        if not document_header.overCostTaxBase and not (
            document_detail.item and document_detail.item.disccountToUnitValue):

            if document_header.source.shortWord in ("FPD", "FPI", "FPC", "FPA", "FM", "FME"):
                accounting_record.baseValue = _round(document_detail.baseValue - discount -
                                                     _round(
                                                         document_detail.baseValue * document_detail.disccount / 100,
                                                         self.round_decimals),
                                                     self.round_decimals)

        accounting_record.percentage = document_detail.iva

        # //calculo de cuentas del iva cuando el documento es una factura de compras y gastos, y el valor total tiene un descuento
        # //calculo de cuentas del iva cuando el documento es consumo interno de articulos
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