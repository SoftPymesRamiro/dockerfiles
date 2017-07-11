# -*- coding: utf-8 -*-
#########################################################
# Legalization Contract Module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

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

class LegalizationContractsAccounting(object):
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

    def do_account(self, document_header=None, document_details=None, payment_receipt =None):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            self.expenses = document_header.expenses if document_header.expenses is not None else 0
            # Recorrido de detalles
            if self.total_records > 0:
                for detail in document_details:
                    # Item o Activo
                    self.ret_value.append(
                        self.item_asset_contracted(document_header, detail, 0, "D")
                    )
            # Calculo de TOTALES
            [self.ret_value.append(self.close_contract(document_header, accounting, "C"))
            for accounting in document_header.accountingGeneralList]
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def item_asset_contracted(self, document_header=None, document_detail=None, decimal_values=None,
                            account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        if document_header.provider:
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
        accounting_record.providerId = document_header.providerId
        accounting_record.contractId = document_header.contractId
        # Datos de detalle
        accounting_record.costCenterId = document_detail.costCenterId
        accounting_record.divisionId = document_detail.divisionId
        accounting_record.sectionId = document_detail.sectionId
        accounting_record.dependencyId = document_detail.dependencyId
        if document_detail.itemId:
            accounting_record.itemId = document_detail.itemId
            accounting_record.pucId = document_detail.item.inventoryPUCId
            accounting_record.warehouseId = document_detail.detailWarehouseId
            accounting_record.lot = document_detail.lot
            accounting_record.dueDate = document_detail.dueDate
            accounting_record.sizeId = document_detail.sizeId
            accounting_record.colorId = document_detail.colorId
            accounting_record.measurementUnitId = document_detail.measurementUnitId
            accounting_record.allThirdId = document_detail.itemId
            accounting_record.allThirdType = 'IT'
        elif document_detail.asset:
            accounting_record.asset = document_detail.asset
            accounting_record.pucId = document_detail.asset.pucId
            accounting_record.allThirdId = document_detail.assetId
            accounting_record.allThirdType = 'AS'
        accounting_record.quantity = document_detail.quantity
        accounting_record.units = document_detail.units
        if account_type == "C":
            accounting_record.credit = document_detail.value
        else:
            accounting_record.debit = document_detail.value
        accounting_record.comments = document_detail.comments
        accounting_record.crossDocumentHeaderId = document_detail.crossDocumentHeaderId \
        if document_detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def close_contract(self,document_header=None, accounting_ar=None, account_type=None):
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        # Datos de detalle
        accounting_record.mainThirdId = accounting_ar.mainThirdId
        accounting_record.providerId = accounting_ar.providerId
        accounting_record.allThirdId = accounting_ar.providerId
        accounting_record.allThirdType = "PR"
        accounting_record.contractId = accounting_ar.contractId
        accounting_record.crossPrefix = accounting_ar.crossPrefix
        accounting_record.crossDocument = accounting_ar.crossDocument
        accounting_record.costCenterId = accounting_ar.costCenterId
        accounting_record.divisionId = accounting_ar.divisionId
        accounting_record.sectionId = accounting_ar.sectionId
        accounting_record.dependencyId = accounting_ar.dependencyId
        accounting_record.pucId = accounting_ar.pucId
        accounting_record.quantity = accounting_ar.quantity
        accounting_record.units = accounting_ar.units
        if account_type == "C":
            accounting_record.credit = accounting_ar.debit
        else:
            accounting_record.debit = accounting_ar.credit
        accounting_record.comments = accounting_ar.comments
        accounting_record.crossDocumentHeaderId = accounting_ar.crossDocumentHeaderId \
            if accounting_ar.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record