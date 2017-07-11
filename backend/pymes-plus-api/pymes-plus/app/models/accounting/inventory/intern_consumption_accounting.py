# coding=utf-8
#########################################################
# Intern Consumption Accounting module
#########################################################
__author__ = "SoftPymes"
__credits__ = ["JAPeTo"]

from ...referential.default_value import DefaultValue
from ...referential.puc import PUC
from ..purchase.purchase_functions import PurchaseFunctions
from ...referential.general_parameter import GeneralParameter
from ..accounting_record import AccountingRecord
from ....exceptions import InternalServerError
from ....utils.math_ext import _round

class InternConsumptionAccounting(object):

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
                    # Artículo en consignación
                    if detail.detailWarehouse.typeWarehouse == "C":
                        self.ret_value.append(self.sale_third_party(document_header, detail,
                                                                    _round(detail.cost * detail.units,
                                                                           2), "C"))
                        self.ret_value.append(self.assets_consigning(document_header, detail, "D"))
                        self.ret_value.append(self.inventory_consigning(document_header, detail, "C"))
                    else:
                        self.ret_value.append(self.outcome_inventory(document_header, detail,
                                                                     self.round_decimals, "C"))
                    if detail.value > 0:
                        self.ret_value.append(self.detail_iva(document_header, detail, 0,
                                                              0, 0, self.round_decimals, "C"))
                        self.ret_value.append(self.incurred_expense(document_header,
                                                                    detail, self.round_decimals, "D"))
                # Consumo Interno de Inventarios
                self.ret_value.append(self.internal_consumption(document_header, "D"))
            # Retorna la lista
            return self.ret_value
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    def sale_third_party(self, document_header, detail, value, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = None
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
        if detail.sourceDocumentDetail is not None \
                and detail.sourceDocumentDetail.detailWarehouseId is not None \
                and detail.sourceDocumentDetail.detailWarehouse.typeWarehouse == 'C':
            accounting_record.providerId = detail.sourceDocumentDetail.detailWarehouse.providerId
            accounting_record.mainThirdId = detail.sourceDocumentDetail.detailWarehouse.provider.thirdPartyId
        accounting_record.itemId = detail.itemId
        accounting_record.crossPrefix = detail.sourceDocumentPrefix \
            if detail.sourceDocumentPrefix is not None else document_header.prefix
        accounting_record.crossDocument = detail.sourceDocumentNumber if \
            detail.sourceDocumentNumber is not None else "RENUMBER"
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.saleByThirdParties][0]
        if credit_debit == 'C':
            accounting_record.credit = value
        else:
            accounting_record.debit = value
        accounting_record.allThirdId = accounting_record.mainThirdId
        accounting_record.allThirdType = "TH"
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
        accounting_record.mainThirdId = None
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
            accounting_record.debit = _round(detail.cost * detail.units, 2)
        accounting_record.allThirdId = accounting_record.mainThirdId
        accounting_record.allThirdType = "TH"
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
        accounting_record.mainThirdId = None
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
            or (detail.sourceDocumentDetail is not None
                and detail.sourceDocumentDetail.documentHeader.destinyWarehouse is not None
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

    def outcome_inventory(self,document_header, detail, round_decimals, credit_debit):
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
        accounting_record.warehouseId = detail.detailWarehouseId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.quantity = detail.quantity
        accounting_record.units = detail.units
        if credit_debit == "C":
            accounting_record.credit = _round(detail.cost * detail.units, 2)
        else:
            accounting_record.debit = _round(detail.cost * detail.units, 2)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def detail_iva(self, document_header, detail, over_cost, discount, discount2, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.customerId = document_header.customerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.mainThirdId = None
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.allThirdId = document_header.costCenter.branchId
        accounting_record.allThirdType =  'BR'
        accounting_record.itemId = detail.itemId
        accounting_record.assetId = detail.assetId
        accounting_record.pucId = detail.ivaPUCId
        accounting_record.lot = detail.lot
        accounting_record.dueDate = detail.dueDate
        accounting_record.sizeId = detail.sizeId
        accounting_record.colorId = detail.colorId
        accounting_record.measurementUnitId = detail.measurementUnitId
        accounting_record.percentage = detail.iva
        accounting_record.baseValue = detail.baseValueIVA
        if credit_debit == 'C':
            accounting_record.credit = _round((accounting_record.baseValue * detail.iva) / 100, round_decimals)
        else:
            accounting_record.debit = _round((accounting_record.baseValue * detail.iva) / 100, round_decimals)
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def incurred_expense(self,document_header, detail, round_decimals, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.mainThirdId = None
        accounting_record.customerId = document_header.customerId
        accounting_record.providerId = document_header.providerId
        accounting_record.employeeId = document_header.employeeId
        accounting_record.businessAgentId = document_header.businessAgentId
        accounting_record.itemId = detail.itemId
        accounting_record.pucId = [p.pucId for p in self.list_puc if p.incurredTax][0]
        if credit_debit == "C":
            accounting_record.credit = _round(detail.baseValueIVA * detail.iva / 100, round_decimals)
        else:
            accounting_record.debit = _round(detail.baseValueIVA * detail.iva / 100, round_decimals)
        accounting_record.allThirdId = document_header.costCenter.branchId
        accounting_record.allThirdType = 'BR'
        accounting_record.crossDocumentHeaderId = detail.crossDocumentHeader.documentHeaderId \
            if detail.crossDocumentHeader else document_header.documentHeaderId
        return accounting_record

    def internal_consumption(self,document_header, credit_debit):
        accounting_record = AccountingRecord()
        accounting_record.branchId = document_header.branchId
        accounting_record.accountingDate = document_header.documentDate
        accounting_record.costCenterId = document_header.costCenterId
        accounting_record.divisionId = document_header.divisionId
        accounting_record.sectionId = document_header.sectionId
        accounting_record.dependencyId = document_header.dependencyId
        accounting_record.puc = [p for p in self.list_puc if p.expensesInternalConsumption][0]
        accounting_record.puc = self.p_functions.expenses_puc(accounting_record.puc,
                                                              document_header,
                                                              document_header.costCenter,
                                                              document_header.division,
                                                              document_header.section,
                                                              document_header.dependency)
        if credit_debit == "C":
            accounting_record.credit = document_header.subtotal
        else:
            accounting_record.debit = document_header.subtotal
        accounting_record.allThirdId = document_header.costCenter.branchId
        accounting_record.allThirdType = "BR"
        accounting_record.comments = document_header.comments
        accounting_record.crossDocumentHeaderId = document_header.documentHeaderId
        return accounting_record