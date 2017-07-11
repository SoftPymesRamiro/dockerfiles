# coding=utf-8
#########################################################
# ClosePurchaseImportAccounting module
# Date: 29-11-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David, JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import _round
from ....exceptions import InternalServerError
from datetime import timedelta
from ..payment_accounting import PaymentAccounting
from .purchase_functions import PurchaseFunctions
from decimal import Decimal


class ClosePurchaseImportAccounting(object):
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

    def do_account(self, document_header=None, document_details=None, payment_receipt=None):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)

            self.expenses = document_header.expenses if document_header.expenses is not None else 0

            # Recorrido de detalles
            if self.total_records > 0:

                for i, detail in enumerate(document_details):
                    self.expenses -= 0 if document_header.subtotal == 0 else Decimal(_round(
                        ((detail.value / document_header.subtotal) * (
                        0 if document_header.expenses is None else document_header.expenses)), self.round_decimals))

                    if i == self.total_records and self.expenses != 0 and document_header.closingType:
                        self.over_cost = self.expenses
                    else:
                        self.over_cost = 0

                    self.ret_value.append(self.item_asset_imported(document_header, detail, self.over_cost, 'D'))

            # calculo de TOTALES
            dec_sum = 0
            for i, accounting in enumerate(document_header.accountingGeneralList):
                if i == len(document_header.accountingGeneralList)-1:
                    self.ret_value.append(self.close_importation(document_header, accounting, 'C', dec_sum, True))
                else:
                    self.ret_value.append(self.close_importation(document_header, accounting, 'C', dec_sum, False))
                dec_sum += Decimal(self.ret_value[-1].decimalValue)
                self.ret_value[-1].decimalValue = 0

            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def item_asset_imported(self, document_header=None, detail=None, difference=None, credit_debit=None):
        """
        This method allow account the total's import's close
        :param document_header: document header object
        :param detail: document detail object
        :param difference: difference
        :param credit_debit: credit or debit mark
        :return: accounting record object
        """
        accounting_record = AccountingRecord()
        # Datos de Encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.mainThirdId = document_header.provider.thirdPartyId
        accounting_record.providerId = document_header.providerId
        accounting_record.importId = document_header.importId
        accounting_record.contractId = document_header.contractId

        # Datos de detalle
        accounting_record.costCenterId = detail.costCenterId
        accounting_record.divisionId = detail.divisionId
        accounting_record.sectionId = detail.sectionId
        accounting_record.dependencyId = detail.dependencyId

        if not detail.itemId is None:
            accounting_record.itemId = detail.itemId
            accounting_record.pucId = detail.item.inventoryPUCId
            accounting_record.warehouseId = detail.detailWarehouseId
            accounting_record.lot = detail.lot
            accounting_record.dueDate = detail.dueDate
            accounting_record.sizeId = detail.sizeId
            accounting_record.colorId = detail.colorId
            accounting_record.measurementUnitId = detail.measurementUnitId
            accounting_record.allThirdId = detail.itemId
            accounting_record.allThirdType = 'IT'
        elif not detail.assetId is None:
            accounting_record.assetId = detail.assetId
            accounting_record.pucId = detail.asset.pucId
            accounting_record.allThirdId = detail.assetId
            accounting_record.allThirdType = 'AS'

        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        if credit_debit == 'C':
            accounting_record.credit = detail.value + (0 if document_header.subtotal == 0 else Decimal(_round(
                ((detail.value / document_header.subtotal) * document_header.expenses),
                self.round_decimals))) + difference
        else:
            accounting_record.debit = detail.value + (0 if document_header.subtotal == 0 else Decimal(_round(
                ((detail.value / document_header.subtotal) * (
                0 if document_header.expenses is None else document_header.expenses)),
                self.round_decimals))) + difference

        accounting_record.comments = detail.comments

        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeaderId \
            if detail.crossDocumentHeaderId is not None else document_header.documentHeaderId

        return accounting_record

    def close_importation(self, document_header=None, ar=None, credit_debit=None, dec_sum=None, last_rec_no=None):
        accounting_record = AccountingRecord()
        # Datos de encabezado
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate

        # Datos de detalle
        accounting_record.mainThirdId = None if ar.provider is None else ar.provider.thirdPartyId
        accounting_record.providerId = ar.providerId
        accounting_record.allThirdId = None if ar.provider is None else ar.provider.thirdPartyId
        accounting_record.allThirdType = 'TH'
        accounting_record.importId = ar.importId
        accounting_record.crossPrefix = ar.crossPrefix
        accounting_record.crossDocument = ar.crossDocument
        accounting_record.costCenterId = ar.costCenterId
        accounting_record.divisionId = ar.divisionId
        accounting_record.sectionId = ar.sectionId
        accounting_record.dependencyId = ar.dependencyId
        accounting_record.pucId = ar.pucId
        accounting_record.quantity = ar.quantity
        accounting_record.units = ar.units

        round = 0

        if credit_debit == 'C':
            round = _round(ar.debit * Decimal(document_header.total / document_header.importationValue), self.round_decimals)

            if last_rec_no:
                round = document_header.total - Decimal(dec_sum)
            if round < 0:
                accounting_record.debit = abs(round)
            else:
                accounting_record.credit = abs(round)

        else:
            round = _round(ar.credit * Decimal(document_header.total / document_header.importationValue), self.round_decimals)
            if last_rec_no:
                round = document_header.total - Decimal(dec_sum)
            accounting_record.debit = round

        accounting_record.decimalValue = round
        accounting_record.comments = ar.comments

        accounting_record.crossDocumentHeaderId = ar.crossDocumentHeaderId \
            if ar.crossDocumentHeaderId is not None else document_header.documentHeaderId

        return accounting_record
