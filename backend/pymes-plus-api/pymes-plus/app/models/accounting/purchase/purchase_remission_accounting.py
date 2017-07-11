# coding=utf-8
#########################################################
# Purchase Remission Accounting module
# Date: 10-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = ["David"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....utils.math_ext import  _round
from ....exceptions import ValidationError, InternalServerError
import datetime as datetime_delta
from datetime import datetime

class PurchaseRemissionAccounting(object):

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

    def do_account(self, document_header, document_details):
        try:
            # Almacena el numero de registros que hay en el document details
            if document_details and len(document_details):
                self.total_records = len(document_details)
            self.expenses = document_header.expenses if document_header.expenses is not None else 0
            # Recorrido de detalles
            if self.total_records > 0:
                for detail in document_details:
                    if detail.item.disccountToUnitValue:
                        self.discount = _round(detail.value * detail.disccount / 100, self.round_decimals)
                    else:
                        self.discount = 0

                    # Articulo en consginacion
                    if detail.detailWarehouse.typeWarehouse == 'C':
                        self.total_cost -= detail.value
                        self.ret_value.append(self.inventory_consigning(document_header, detail, 'D'))
                        self.ret_value.append(self.assets_consigning(document_header, detail, 'C'))
                    else:
                        # Inventario
                        self.ret_value.append(self.purchase_inventory(document_header, detail,
                                                                      detail.value - self.discount, 0, 'D'))

                        # Impuesto al consumo
                        if detail.item.consumptionPercentage > 0 and detail.baseValue > 0:
                            if detail.item.addIVAtoCost:
                                self.ret_value.append(
                                    self.purchase_inventory(document_header, detail,
                                                            _round(detail.baseValue *
                                                                   (detail.item.consumptionPercentage / 100),
                                                                   self.round_decimals), 1, 'D'))
                                self.over_cost = _round(detail.value * (detail.item.consumptionPercentage / 100),
                                                        self.round_decimals)
                                self.total_cost += self.over_cost
            # Totales
            self.ret_value.append(self.provider_payable(document_header,
                                                        document_header.subtotal + self.total_cost - self.total_discount,
                                                        'C', True))
            # Validacion para cuadrar los valores si tienen diferencia de 1 peso
            if len(self.ret_value) > 0:
                debit = sum(d.debit or 0 for d in self.ret_value)
                credit = sum(d.credit or 0 for d in self.ret_value)
                if debit - credit != 0 and abs(debit - credit) <= 1:
                    if debit > credit:
                        sorted(
                            [r for r in self.ret_value if r.credit > 0],
                            key=lambda ar: ar.credit
                        )[0].credit += debit - credit
                    else:
                        sorted(
                            [r for r in self.ret_value if r.debit > 0],
                            key=lambda ar: ar.debit
                        )[0].debit += credit - debit
            # Recorrido de registros para verificar si el documento presenta un descuadre (creditos - debitos) debe ser 0
            d = 0
            c = 0
            for ar in self.ret_value:
                c += (ar.credit or 0)
                d += (ar.debit or 0)

                # Marcacion para registros niif
                if self.general_parameter.cDate:
                    ar.niif = True
                ar.documentHeaderId = document_header.documentHeaderId
                ar.documentNumber = document_header.documentNumber
                ar.documentTypeId = document_header.documentTypeId
                ar.documentPrefix = document_header.prefix
                ar.createdBy = document_header.createdBy
                ar.updateBy = document_header.updateBy
                ar.creationDate = datetime.now()
                ar.updateDate = datetime.now()
            if c != d:
                raise InternalServerError('Descuadre')
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def inventory_consigning(self, document_header, detail, credit_debit):
        try:
            accounting_record = AccountingRecord()
            # Datos de encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            # Datos del detalle
            accounting_record.allThirdId = detail.itemId
            accounting_record.allThirdType = 'IT'
            accounting_record.itemId = detail.itemId
            accounting_record.measurementUnitId = detail.measurementUnitId
            accounting_record.quantity = detail.quantity
            accounting_record.units = detail.units
            accounting_record.warehouseId = detail.warehouseId
            accounting_record.lot = detail.lot
            accounting_record.dueDate = detail.dueDate
            accounting_record.size = detail.size
            accounting_record.color = detail.color
            if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeader.destinyWarehouseId \
                    is not None and detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == 'P':

                accounting_record.warehouseId = detail.sourceDocumentDetail.documentHeader.destinyWarehouseId \
                    if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeader is not None \
                       and detail.sourceDocumentDetail.documentHeader.destinyWarehouseId is not None \
                    else document_header.destinyWarehouse

                accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                    if document_header.customerId is not None and document_header.customer.thirdPartyId is not None \
                    else accounting_record.mainThirdId

                accounting_record.pucId = [p.pucId for p in self.list_puc if p.billingConceptsInventoryConsignmentCustomer][0]

                if detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.detailWarehouse is not None \
                        and detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == 'C':
                    accounting_record.providerId = detail.sourceDocumentDetail.detailWarehouse.providerId
            else:
                accounting_record.pucId = [p.pucId for p in self.list_puc if p.billingConceptsInventoryConsignment][0]
            if credit_debit == 'C':
                accounting_record.credit = _round(detail.cost * detail.units, 2)
            else:
                accounting_record.debit = _round(detail.cost * detail.units, 2)
            accounting_record.crossDocumentHeaderId = detail.crossDocumentHeaderId \
                if detail.crossDocumentHeaderId is not None else document_header.documentHeaderId
            return accounting_record
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def assets_consigning(self, document_header, detail, credit_debit):
        try:
            accounting_record = AccountingRecord()
            # Datos de encabezado
            accounting_record.branchId = document_header.branchId
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = detail.detailWarehouse.providerId \
                if detail.detailWarehouse.providerId is not None else document_header.providerId
            accounting_record.mainThirdId = detail.detailWarehouse.provider.thirdPartyId \
                if detail.detailWarehouse.provider.thirdPartyId is not None else accounting_record.mainThirdId
            # Datos del detalle
            accounting_record.itemId = detail.itemId
            if ((document_header.destinyWarehouse is not None and document_header.destinyWarehouse.typeWarehouse == 'P') or
                    (detail.sourceDocumentDetail is not None and detail.sourceDocumentDetail.documentHeaderId is not None
                     and detail.sourceDocumentDetail.documentHeader.destinyWarehouseId is not None
                     and detail.sourceDocumentDetail.documentHeader.destinyWarehouse.typeWarehouse == 'P')):
                accounting_record.mainThirdId = document_header.customer.thirdPartyId \
                    if detail.sourceDocumentDetail.documentHeader.customerId is not None \
                       and detail.sourceDocumentDetail.documentHeader.customer.thirdPartyId is not None \
                    else accounting_record.mainThirdId
                accounting_record.pucId = [p.pucId for p in self.list_puc if p.AssetsConsigningCustomer][0]
            if credit_debit == 'C':
                accounting_record.credit = _round(detail.cost * detail.units, 2)
            else:
                accounting_record.debit = _round(detail.cost * detail.units, 2)
            accounting_record.allThirdId = accounting_record.mainThird.thirdPartyId
            accounting_record.allThirdType = 'TH'
            accounting_record.crossDocumentHeaderId = detail.crossDocumentHeaderId \
                if detail.crossDocumentHeaderId is not None else document_header.documentHeaderId
            return accounting_record
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def purchase_inventory(self, document_header, detail, value, iva_to_cost, credit_debit):
        try:
            accounting_record = AccountingRecord()
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.providerId = document_header.providerId
            accounting_record.costCenterId = detail.costCenterId
            accounting_record.divisionId = detail.divisionId
            accounting_record.sectionId = detail.sectionId
            accounting_record.dependencyId = detail.dependencyId
            accounting_record.itemId = detail.itemId
            accounting_record.pucId = detail.item.inventoryPUCId
            accounting_record.warehouseId = detail.detailWarehouseId
            accounting_record.lot = detail.lot
            accounting_record.dueDate = detail.dueDate
            accounting_record.size = detail.size
            accounting_record.color = detail.color
            accounting_record.measurementUnitId = detail.measurementUnitId
            accounting_record.ivaToCost = iva_to_cost
            accounting_record.ConsumptionToCost = detail.item.addConsumptionToCost
            accounting_record.BaseValue = detail.baseValue
            accounting_record.quantity = detail.quantity if iva_to_cost == 0 else 0
            accounting_record.units = detail.units if iva_to_cost == 0 else 0
            if credit_debit == 'C':
                accounting_record.credit = value
                accounting_record.sign = '-' if detail.quantity > 0 and detail.value == 0 else '+'
            else:
                accounting_record.debit = value
            if detail.itemId is not None:
                # Guardar en el campo AllThird el tercero en caso de que sea un item de servicio
                if detail.item.typeItem == "S":
                    accounting_record.allThirdId = accounting_record.providerId
                    accounting_record.allThirdType = 'PR'
                else:
                    accounting_record.allThirdId = detail.item.itemId
                    accounting_record.allThirdType = 'IT'
            accounting_record.comments = detail.comments
            accounting_record.crossDocumentHeaderId = detail.crossDocumentHeaderId \
                if detail.crossDocumentHeaderId is not None else document_header.documentHeaderId
            return accounting_record
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def provider_payable(self, document_header, value, credit_debit, is_renumber):
        try:
            accounting_record = AccountingRecord()
            accounting_record.branchId = document_header.branchId
            accounting_record.accountingDate = document_header.documentDate
            accounting_record.costCenterId = document_header.costCenterId
            accounting_record.divisionId = document_header.divisionId
            accounting_record.sectionId = document_header.sectionId
            accounting_record.dependencyId = document_header.dependencyId
            accounting_record.mainThirdId = document_header.provider.thirdPartyId
            accounting_record.allThirdId = document_header.provider.providerId
            accounting_record.allThirdType = 'PR'
            accounting_record.providerId = document_header.providerId
            accounting_record.pucId = [p.pucId for p in self.list_puc if p.accountsPayableNationalProvider][0]
            # accounting_record.pucId = self.list_puc.filter(PUC.accountsPayableNationalProvider == 1).first().pucId
            accounting_record.sourceDocumentTypeId = document_header.sourceDocumentTypeId
            if not is_renumber:
                accounting_record.crossPrefix = document_header.prefix
                accounting_record.crossDocument = document_header.documentNumber
            elif document_header.sourceDocumentTypeId is not None and document_header.sourceDocumentType.shortWord == 'RP':
                accounting_record.crossPrefix = document_header.sourceDocumentHeader.prefix
                accounting_record.crossDocument = document_header.sourceDocumentHeader.documentNumber
            else:
                accounting_record.crossPrefix = document_header.prefix
                accounting_record.crossDocument = 'RENUMBER'
            # accounting_record.dueDate = document_header.documentDate + datetime_delta.timedelta(days=document_header.termDays)
            accounting_record.dueDate = document_header.dateTo
            if credit_debit == 'C':
                accounting_record.credit = value
            else:
                accounting_record.debit = value
            accounting_record.comments = document_header.comments
            if document_header.currencyId != self.default_value.currencyId:
                accounting_record.pucId = [p.pucId for p in self.list_puc if p.accountsPayableForeignProvider][0]
            accounting_record.foreignCurrency = _round(document_header.total / document_header.exchangeRate, 2)
            accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
            return accounting_record
        except Exception as e:
            print(e)
            raise InternalServerError(e)

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




