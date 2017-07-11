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
from ..document_detail import DocumentDetail
from ....utils.math_ext import _round
from ....exceptions import ValidationError, InternalServerError
import datetime as datetime_delta
from datetime import datetime, timedelta
from .... import session
from ..payment_accounting import PaymentAccounting
from .sale_functions import SaleFunctions
import decimal


class CustomerRefundAccounting(object):
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
                    if document_header.sourceDocumentHeader is None \
                            or document_header.sourceDocumentHeader.destinyWarehouse is None \
                            or document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse not in 'C~P'.split(
                                '~'):
                        if detail.item.typeItem == 'A':
                            if (detail.detailWarehouse.typeWarehouse == "C" and detail.booleanValue) \
                                    or detail.detailWarehouse.typeWarehouse != "C":
                                self.ret_value.append(self.sales_inventory(document_header, detail, "D"))
                            else:
                                if document_header.sourceDocumentHeader is not None \
                                        and document_header.sourceDocumentHeader.documentType is not None \
                                        and document_header.sourceDocumentHeader.documentType.shortWord == "RM":
                                    self.ret_value.append(self.sale_third_party(document_header, detail,
                                                                                _round(detail.cost * detail.units, 2),
                                                                                "D"))
                                    self.ret_value.append(self.assets_consigning(document_header, detail, "C"))
                                    self.ret_value.append(self.inventory_consigning(document_header, detail, "D"))
                            self.ret_value.append(self.cost_inventory(document_header, detail, "C"))
                    else:
                        # Inventario en consignacion
                        if document_header.sourceDocumentType is not None and document_header.sourceDocumentType.shortWord == "RM":
                            # Devolver la cuenta 84 y la 94
                            if document_header.sourceDocumentHeader is not None \
                                    and document_header.sourceDocumentHeader.destinyWarehouse is not None \
                                    and document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P":
                                document_header.booleanValue = True
                                self.ret_value.append(self.assets_consigning(document_header, detail, "D"))
                                self.ret_value.append(self.inventory_consigning(document_header, detail, "C"))
                                if document_header.documentType.shortWord == "DL" \
                                        and document_header.sourceDocumentHeader.documentType.shortWord == "RM" \
                                        and not detail.booleanValue \
                                        and document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P" \
                                        and detail.sourceDocumentDetail.detailWarehouse.typeWarehouse != "C":
                                    self.ret_value.append(self.sales_inventory(document_header, detail, "D"))
                                    detail.booleanValue = True
                                    self.ret_value.append(self.sales_inventory(document_header, detail, "C"))
                                    detail.booleanValue = False
                                else:
                                    document_header.booleanValue = False
                                    self.ret_value.append(self.assets_consigning(document_header, detail, "C"))
                                    self.ret_value.append(self.inventory_consigning(document_header, detail, "D"))
                            else:
                                if document_header.sourceDocumentHeader is not None and document_header.sourceDocumentHeader.documentType is not None and document_header.sourceDocumentHeader.documentType.shortWord == "RM" and detail.detailWarehouse is not None and detail.detailWarehouse.typeWarehouse == "C":
                                    self.ret_value.append(self.sales_inventory(document_header, detail, "D"))

                        if document_header.sourceDocumentType is not None and document_header.sourceDocumentType.shortWord == "FC":
                            # // Devolver la cuenta 84 y la 94
                            if document_header.sourceDocumentHeader is not None \
                                    and document_header.sourceDocumentHeader.destinyWarehouse is not None \
                                    and document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P":
                                document_header.BooleanValue = True
                                if document_header.sourceDocumentHeader is not None \
                                        and document_header.sourceDocumentHeader.sourceDocumentHeader is not None \
                                        and document_header.sourceDocumentHeader.sourceDocumentHeader.documentType is not None \
                                        and document_header.sourceDocumentHeader.sourceDocumentHeader.documentType.shortWord == "RM" \
                                        and (detail.booleanValue or detail.detailWarehouse.typeWarehouse == "G"):
                                    # No segenran los movimeintos de la cuenta 84
                                    self.ret_value.append(self.sales_inventory(document_header, detail, "D"))
                                    # Costo de Ventas
                                    self.ret_value.append(self.cost_inventory(document_header, detail, "C"))

                                document_header.booleanValue = False

                    if document_header.sourceDocumentType is not None and document_header.sourceDocumentType.shortWord != "RM":
                        # Ingreso
                        if document_header.sourceDocumentHeader.source is not None \
                                and document_header.sourceDocumentHeader.source.shortWord == "VT" \
                                and detail.sourceDocumentDetail is not None \
                                and detail.sourceDocumentDetail.provider is not None:
                            # Devoluciones de facturas por cuenta de tercero
                            self.ret_value.append(self.income_for_others(document_header, detail, self.round_decimals,
                                                                         "D", detail.value))
                        else:
                            self.ret_value.append(
                                self.returning_sales(document_header, detail, self.round_decimals, "D"))

                        # Articulo en consignacion
                        if detail.detailWarehouse.typeWarehouse == "C":
                            if document_header.sourceDocumentHeader is not None \
                                    and document_header.sourceDocumentHeader.documentType is not None \
                                    and document_header.sourceDocumentHeader.documentType.shortWord == "FC" \
                                    and document_header.sourceDocumentHeader.destinyWarehouse is not None \
                                    and document_header.sourceDocumentHeader.destinyWarehouse.typeWarehouse == "P" \
                                    and document_header.sourceDocumentHeader.sourceDocumentHeader.documentType.shortWord != "RM":
                                # Costo de Ventas
                                self.ret_value.append(self.cost_inventory(document_header, detail, "C"))
                                # Inventario
                                self.ret_value.append(self.sales_inventory(document_header, detail, "D"))
                            else:
                                # Se deben contabilizar las cuentas 28, 91 y 94 cuando NO SE HA LEGALIZADO
                                # la mercancia del proveedor. detail.BooleanValue me dice si ese detalle ya está legalizado
                                if (detail.detailWarehouse.typeWarehouse == "C" and not detail.booleanValue) \
                                        or detail.detailWarehouse.typeWarehouse != "C":
                                    if not detail.booleanValue:
                                        self.ret_value.append(self.sale_third_party(document_header, detail,
                                                                                    _round(detail.Cost * detail.Units,
                                                                                           2), "D"))
                                        if ((document_header.sourceDocumentHeader is None and document_header.sourceDocumentHeader.destinyWarehouse is not None)
                                            or document_header.sourceDocumentHeader.destinyWarehouse is not None
                                            and (document_header.SourceDocumentHeader.DestinyWarehouse.TypeWarehouse in "C~P".split('~'))):
                                            self.ret_value.append(self.cost_inventory(document_header, detail, "C"))
                                        document_header.booleanValue = False
                                        self.ret_value.append(self.assets_consigning(document_header, detail, "C"))
                                        self.ret_value.append(self.inventory_consigning(document_header, detail, "D"))
                                        document_header.booleanValue = True
                                    else:
                                        self.ret_value.append(self.sale_third_party(document_header, detail,
                                                                                    _round(detail.cost * detail.units, 2), "D"))
                                        self.ret_value.append(self.assets_consigning(document_header, detail, "C"))
                                        self.ret_value.append(self.inventory_consigning(document_header, detail, "D"))

                        # // Es un obsequio
                        if detail.unitValue == 0 and detail.item.typeItem == 'A':
                            if not detail.ivaCustomer:
                                self.ret_value.append(
                                    self.incurred_expense(document_header, detail, self.round_decimals, "C"))
                                self.ret_value.append(
                                    self.incurred_iva_tax(document_header, detail, self.round_decimals, "D"))
                            else:
                                self.ret_value.append(
                                    self.incurred_iva_tax(document_header, detail, self.round_decimals, "D"))

                        # // Impuesto al Consumo
                        if detail.consumptionTaxPercent > 0 and detail.consumptionTaxBase > 0:
                            self.ret_value.append(
                                self.sales_consumption_tax(document_header, detail, self.round_decimals, "D"))
                        # IVA en ventas
                        if detail.baseValue > 0 and detail.value > 0:
                            self.ret_value.append(self.detail_iva(document_header, detail, 0, 0, self.discount2,
                                                                  self.round_decimals, "D"))
                        # ICA en ventas
                        if detail.icaPercent and detail.icaPercent > 0 and detail.value > 0:
                            self.ret_value.append(
                                self.sales_ica_tax(document_header, detail, self.round_decimals, 'D'))
                            self.ret_value.append(
                                self.sales_ica_expense(document_header, detail, self.round_decimals, 'C'))

                        # Retefuente en Ventas
                        if detail.withholdingTax and detail.withholdingTax > 0 and detail.value > 0:
                            self.ret_value.append(
                                self.detail_withholding_tax(document_header, detail, 0, 0, self.discount2,
                                                            self.round_decimals, 'C'))
                            if document_header.branch.company.selfRetainingRete:
                                self.ret_value.append(
                                    self.self_detail_withholding_tax(document_header, detail, 0, 0, self.discount2,
                                                                     self.round_decimals, 'D'))
                    detail.booleanValue = False

            if document_header.sourceDocumentType is None or document_header.sourceDocumentType.shortWord != "RM":
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

                # Propina
                if document_header.tipValue > 0:
                    self.ret_value.append(self.s_functions.tip(document_header, self.round_decimals, 'D'))

                # Ajuste al  peso
                if document_header.adjustment is not None:
                    if document_header.adjustment < 0:
                        self.ret_value.append(
                            self.s_functions.adjustment_expense(document_header, document_header.adjustment, 'C'))
                    else:
                        self.ret_value.append(
                            self.s_functions.adjustment_income(document_header, document_header.adjustment, 'D'))

                self.ret_value.append(self.customer_receivable(document_header, payment_receipt=None,
                                                               payment_detail=None, credit_debit='C'))

            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def sales_inventory(self, document_header, detail, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        # Datos del detalle
        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId
        accounting_record.itemId = detail.itemId
        accounting_record.pucId = detail.item.inventoryPUCId

        # Se lleva el inventario a la bodega del cliente consignatario - Roger
        # TODO: Bodega de cliente consignatario
        accounting_record.warehouseId = detail.detailWarehouseId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        accounting_record.measurementUnitId = detail.measurementUnitId

        if credit_debit == "C":
            accounting_record.credit = _round(detail.cost * detail.units, 2)
            accounting_record.sign = '-' if detail.quantity > 0 and detail.value == 0 else '+'

        else:
            accounting_record.debit = _round(detail.cost * detail.units, 2)
        accounting_record.allThirdId = detail.itemId
        accounting_record.allThirdType = 'IT'
        accounting_record.comments = detail.comments

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def sale_third_party(self, document_header, detail, value, credit_debit):
        accounting_record = AccountingRecord()
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
        accounting_record.dueDate = document_header.documentDate

        accounting_record.providerId = detail.detailWarehouse.providerId \
            if detail.detailWarehouse.providerId is not None \
            else document_header.providerId
        accounting_record.mainThird = detail.detailWarehouse.provider.thirdPartyId \
            if detail.detailWarehouse.providerId is not None \
               and detail.detailWarehouse.provider.thirdPartyId is not None \
            else accounting_record.mainThird
        # Factura de una remisión con la bodega de proveedor consignatario
        if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.detailWarehouseId is not None \
                and detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == 'C':
            accounting_record.providerId = detail.sourceDocumentDetail.detailWarehouse.providerId
            accounting_record.mainThirdId = detail.sourceDocumentDetail.detailWarehouse.provider.thirdPartyId

        accounting_record.itemId = detail.itemId
        accounting_record.crossPrefix = detail.SourceDocumentPrefix \
            if detail.sourceDocumentPrefix is not None else document_header.prefix

        accounting_record.crossDocument = detail.SourceDocumentNumber if detail.sourceDocumentNumber is not None else "RENUMBER"
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.saleByThirdParties][0]

        if credit_debit == 'C':
            accounting_record.credit = value
        else:
            accounting_record.debit = value
        accounting_record.allThirdId = accounting_record.mainThirdId
        accounting_record.comments = detail.comments
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def assets_consigning(self, document_header, detail, credit_debit):
        accounting_record = AccountingRecord()
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
        accounting_record.providerId = detail.detailWarehouse.providerId \
            if detail.detailWarehouse.providerId is not None \
            else document_header.providerId
        accounting_record.mainThird = detail.detailWarehouse.provider.thirdPartyId \
            if detail.detailWarehouse.providerId is not None \
               and detail.detailWarehouse.provider.thirdPartyId is not None \
            else accounting_record.mainThird
        accounting_record.itemId = detail.itemId

        if ((document_header.destinyWarehouse is not None and document_header.destinyWarehouse.TypeWarehouse == 'P'
             and document_header.booleanValue) or (detail.sourceDocumentDetail is not None
                                                   and detail.sourceDocumentDetail.documentHeader is not None
                                                   and detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
                                                   and detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == 'P'
                                                   and document_header.booleanValue)
            or (detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeader is not None
                and detail.sourceDocumentDetail.documentHeader.documentType is not None
                and detail.sourceDocumentDetail.documentHeader.documentType.shortWord == 'RM'
                and detail.item.typeItem == 'A')):
            accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                if detail.sourceDocumentDetail.documentHeader.customerId is not None \
                   and detail.sourceDocumentDetail.documentHeader.customer.thirdPartyId is not None \
                else accounting_record.mainThirdId
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.assetsConsigningCustomer][0]
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.assetsConsigning][0]

        if credit_debit == 'C':
            accounting_record.credit = _round(detail.cost * detail.units, 2)
        else:
            accounting_record.credit = _round(detail.cost * detail.units, 2)
        accounting_record.allThirdId = accounting_record.mainThirdId
        accounting_record.allThirdType = 'TH'
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def inventory_consigning(self, document_header, detail, credit_debit):
        accounting_record = AccountingRecord()
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

        accounting_record.allThirdId = detail.itemId
        accounting_record.allThirdType = 'IT'
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        accounting_record.warehouseId = detail.detailWarehouseId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId

        if ((document_header.destinyWarehouse is not None and document_header.destinyWarehouse.TypeWarehouse == 'P'
             and document_header.documentType.shortWord == 'RM' and document_header.booleanValue)
            or (
                                    detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
                        and detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == 'P'
                    and document_header.booleanValue)):

            accounting_record.warehouseId = detail.sourceDocumentDetail.documentHeader.destinyWarehouseId \
                if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeader is not None \
                   and detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None \
                else document_header.destinyWarehouseId

            accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                if document_header.customer is not None and document_header.customer.thirdParty is not None \
                else accounting_record.mainThirdId

            # Las facturas de cliente con base en una remisión de cliente consignatario y la bodega es del detalle es de
            # un proveedor consignatario, se debe grabar el proveedor en la contabilidad
            if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.detailWarehouse is not None \
                    and detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == "C":
                accounting_record.providerId = detail.sourceDocumentDetail.detailWarehouse.providerId
        else:
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.billingConceptsInventoryConsignment][0]

        if credit_debit == 'C':
            accounting_record.credit = _round(detail.cost * detail.units, 2)
        else:
            accounting_record.debit = _round(detail.cost * detail.units, 2)

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def cost_inventory(self, document_header, detail, credit_debit):
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

        # Datos de detalle
        accounting_record.itemId = detail.itemId
        accounting_record.pucId = detail.item.costPUCId
        accounting_record.itemId = detail.itemId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId

        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units

        if credit_debit == 'C':
            accounting_record.credit = _round(detail.cost * detail.units, 2)
        else:
            accounting_record.debit = _round(detail.cost * detail.units, 2)
        accounting_record.comments = detail.comments
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
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

    def incurred_expense(self, document_header, detail, round_decimals, credit_debit):
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
        accounting_record.pucId = [a.pucId for a in self.list_puc if a.incurredTax][0]

        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'

        if credit_debit == 'C':
            accounting_record.credit = _round(detail.baseValue * detail.iva / 100, self.round_decimals)
        else:
            accounting_record.debit = _round(detail.baseValue * detail.iva / 100, self.round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def incurred_iva_tax(self, document_header, detail, round_decimals, credit_debit):
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
        accounting_record.pucId = detail.ivaPUCId
        accounting_record.baseValue = detail.baseValue
        accounting_record.percentage = detail.iva

        if credit_debit == 'C':
            accounting_record.credit = _round(detail.baseValue * detail.iva / 100, self.round_decimals)
        else:
            accounting_record.debit = _round(detail.baseValue * detail.iva / 100, self.round_decimals)
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        if detail.unitValue == 0 and detail.item.typeItem == "A":
            if detail.ivaCustomer:
                accounting_record.sign = 'C'
            else:
                accounting_record.sign = 'O'
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

    def detail_withholding_tax(self, document_header, detail, over_cost, discount, discount2, round_decimals,
                               credit_debit):
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

    def self_detail_withholding_tax(self, document_header, detail, over_cost, discount, discount2, round_decimals,
                                    credit_debit):
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

    def income_for_others(self, document_header, detail, round_decimals, credit_debit, value):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.allThirdId = detail.providerId if detail.providerId else document_header.customerId
        accounting_record.allThirdType = 'PR' if detail.providerId else 'CU'
        accounting_record.customerId = document_header.customerId
        accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId
        accounting_record.itemId = detail.itemId

        accounting_record.comments = detail.comments
        accounting_record.pucId = detail.pucId if detail.pucId is not None \
            else detail.puc.pucId if detail.puc else \
            [p.pucId for p in self.list_puc if p.saleByThirdParties][0]
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        accounting_record.measurementUnitId = detail.measurementUnitId

        if not (document_header.sourceDocumentHeader is None):
            accounting_record.crossPrefix = document_header.sourceDocumentHeader.prefix
            accounting_record.crossDocument = document_header.sourceDocumentHeader.documentNumber
        else:
            accounting_record.crossPrefix = document_header.prefix
            accounting_record.crossDocument = "RENUMBER"
        accounting_record.dueDate = self.add_days(document_header.documentDate, int(document_header.termDays))

        if credit_debit == 'C':
            accounting_record.credit = _round((value -
                                               _round(value * (detail.disccount / 100), self.round_decimals)),
                                              self.round_decimals) \
                                       + _round(detail.baseValue * (detail.iva / 100), self.round_decimals) \
                                       - _round(detail.baseValue * (detail.withholdingTax / 100), self.round_decimals)
        else:
            accounting_record.debit = _round((value -
                                              _round(value * (detail.disccount / 100), self.round_decimals)),
                                             self.round_decimals) \
                                      + _round(detail.baseValue * (detail.iva / 100), self.round_decimals) \
                                      - _round(detail.baseValue * (detail.withholdingTax / 100), self.round_decimals)

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def add_days(self, date, days):
        for i in range(days):
            date += timedelta(days=1)
        return date

    def customer_receivable(self, document_header, payment_receipt, payment_detail, credit_debit):
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

        accounting_record.dueDate = document_header.documentDate + timedelta(days=int(document_header.termDays))
        if not document_header.isChangeNoted:
            if ((document_header.source is not None and document_header.source.shortWord == "VT") or
                                    document_header.documentType.shortWord in "DL~NC~ND"
                            and document_header.sourceDocumentHeader is not None
                        and document_header.sourceDocumentHeader.source is not None
                    and document_header.sourceDocumentHeader.source.shortWord == "VT"):
                puc_id = [a.pucId for a in self.list_puc if a.paymentsForThirdParties]
                if not len(puc_id):
                    accounting_record.pucId = [a.pucId for a in self.list_puc if a.legalCurrencyAccountsReceivable][0]
                else:
                    accounting_record.pucId = [a.pucId for a in self.list_puc if a.paymentsForThirdParties][0]
            else:
                accounting_record.pucId = [a.pucId for a in self.list_puc if a.legalCurrencyAccountsReceivable][0]
        else:
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.changeNote][0]

        accounting_record.sourceDocumentTypeId = document_header.sourceDocumentTypeId
        if document_header.sourceDocumentHeaderId is not None:
            accounting_record.crossPrefix = document_header.sourceDocumentHeader.prefix
            accounting_record.crossDocument = document_header.sourceDocumentHeader.documentNumber
        else:
            accounting_record.crossPrefix = document_header.sourcePrefix
            accounting_record.crossDocument = document_header.sourceDocument

        if credit_debit == 'C':
            accounting_record.credit = document_header.total
        else:
            accounting_record.debit = document_header.total
        accounting_record.foreignCurrency = _round((document_header.total / document_header.exchangeRate), 2)

        accounting_record.comments = document_header.comments
        if document_header.currencyId != self.default_value.currencyId:
            accounting_record.pucId = [a.pucId for a in self.list_puc if a.foreignCurrencyAccountsreceivable][0]

        accounting_record.crossDocumentHeaderId = document_header.sourceDocumentHeader.documentHeaderId
        return accounting_record

    def returning_sales(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.customer.thirdPartyId
        accounting_record.allThirdId = document_header.customerId
        accounting_record.allThirdType = 'CU'
        accounting_record.customerId = document_header.customerId
        accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId

        accounting_record.pucId = [a.pucId for a in self.list_puc if a.returningCustomer][0]

        accounting_record.itemId = detail.itemId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        accounting_record.measurementUnitId = detail.measurementUnitId

        if credit_debit == 'C':
            accounting_record.credit = _round(
                (detail.value - _round(detail.value * detail.disccount / 100, round_decimals)), round_decimals)
        else:
            accounting_record.debit = _round(
                (detail.value - _round(detail.value * detail.disccount / 100, round_decimals)), round_decimals)

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record