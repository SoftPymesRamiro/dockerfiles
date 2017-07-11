# -*- coding: utf-8 -*-
#########################################################
# Inventary Adjust Accounting module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["david"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ..purchase.purchase_functions import PurchaseFunctions
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from ....utils.math_ext import _round


class InventoryArchingAccounting(object):

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
        self.p_functions = PurchaseFunctions(document_header, list_puc=self.list_puc)

    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            if self.total_records > 0:
                document_header.booleanValue = False
                for detail in document_details:
                    if detail.balance != detail.quantity:
                        self.ret_value.append(
                            self.outcome_inventory(document_header, detail,
                                                   self.round_decimals, "D" if detail.balance-detail.quantity < 0 else "C"))
                        if (detail.balance - detail.quantity) < 0:
                            self.ret_value.append(self.income_inventory_adjustment(document_header, detail, "C"))
                        else:
                            self.ret_value.append(self.cost_inventory(document_header, detail, "D"))
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def outcome_inventory(self, document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.allThirdId = detail.itemId
        accounting_record.allThirdType = 'IT'

        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId
        accounting_record.itemId = detail.itemId
        accounting_record.pucId = detail.item.inventoryPUCId
        accounting_record.warehouseId = document_header.sourceWarehouseId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId

        accounting_record.quantity = abs(detail.balance - detail.quantity)
        accounting_record.units = abs(detail.balance - detail.units)
        if credit_debit == "C":
            accounting_record.credit = abs(_round(detail.cost * (detail.balance - detail.units), 2))
        else:
            accounting_record.debit = abs(_round(detail.cost * (detail.balance - detail.units), 2))

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def income_inventory_adjustment(self, document_header, detail, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId

        accounting_record.pucId = [p.pucId for p in self.list_puc if p.typesDebitInventoryAdjustment][0]
        accounting_record.allThirdId = accounting_record.branchId
        accounting_record.allThirdType = 'BR'

        accounting_record.itemId = detail.itemId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId

        accounting_record.quantity = abs(detail.balance - detail.quantity)
        accounting_record.units = abs(detail.balance - detail.units)
        if credit_debit == "C":
            accounting_record.credit = abs(_round(detail.cost * (detail.balance - detail.units), 2))
        else:
            accounting_record.debit = abs(_round(detail.cost * (detail.balance - detail.units), 2))

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def cost_inventory(self, document_header, detail, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId

        accounting_record.pucId = detail.item.costPUCId

        accounting_record.itemId = detail.itemId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId

        accounting_record.quantity = abs(detail.balance - detail.quantity)
        accounting_record.units = abs(detail.balance - detail.units)
        if credit_debit == "C":
            accounting_record.credit = abs(_round(detail.cost * (detail.balance - detail.units), 2))
        else:
            accounting_record.debit = abs(_round(detail.cost * (detail.balance - detail.units), 2))
        accounting_record.comments = detail.comments
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record
