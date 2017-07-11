# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from ... import Base, session
from sqlalchemy import Integer, ForeignKey, String, Column, DECIMAL, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from datetime import datetime
from ...utils import converters
from ...exceptions import ValidationError, InternalServerError
from flask import g
from .. import Warehouse


class DocumentDetail(Base):
    """DocumentDetail as a public model class.

    note::

    """
    __tablename__ = 'documentdetails'

    documentDetailId = Column(Integer, primary_key=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    crossDocumentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    assetId = Column(ForeignKey(u'assets.assetId'), index=True)
    sourceDocumentDetailId = Column(ForeignKey(u'documentdetails.documentDetailId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    financialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    kitLaborId = Column(ForeignKey(u'kitlabors.kitLaborId'), index=True)
    importConceptId = Column(ForeignKey(u'importconcepts.importConceptId'), index=True)
    cashRegisterId = Column(ForeignKey(u'cashregisters.cashRegisterId'), index=True)
    kitItemId = Column(ForeignKey(u'kititems.kitItemId'), index=True)
    detailDocumentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    sourceDocumentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    colorId = Column(ForeignKey(u'colors.colorId'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    pieceId = Column(ForeignKey(u'pieces.pieceId'), index=True)
    employeeId = Column(ForeignKey(u'employees.employeeId'), index=True)
    payrollEntityId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    sizeId = Column(ForeignKey(u'sizes.sizeId'), index=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    measurementUnitId = Column(ForeignKey(u'measurementunits.measurementUnitId'), index=True)
    kitAssetId = Column(ForeignKey(u'kitassets.kitAssetId'), index=True)
    consumptionTaxPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    thirdId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    detailWarehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    otherThirdId = Column(ForeignKey(u'otherthirds.otherThirdId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    ivaPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    withholdingTaxPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    businessAgentId = Column(ForeignKey(u'businessagents.businessAgentId'), index=True)
    payrollConceptId = Column(ForeignKey(u'payrollconcepts.payrollConceptId'), index=True)
    detailDate = Column(DateTime, default=datetime.now())
    dueDate = Column(DateTime)
    initialDate = Column(DateTime)
    finalDate = Column(DateTime)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    selected = Column(Integer)
    isDeleted = Column(Integer, default=0)
    ivaCustomer = Column(Integer)
    reteICA = Column(Integer)
    quantity = Column(DECIMAL(18, 5), default=0.0)
    units = Column(DECIMAL(18, 5), default=0.0)
    unitValue = Column(DECIMAL(18, 4), default=0.0)
    availableStock = Column(DECIMAL(18, 4), default=0.0)
    amount = Column(DECIMAL(18, 4), default=0.0)
    balance = Column(DECIMAL(18, 4), default=0.0)
    consumptionTaxBase = Column(DECIMAL(18, 4), default=0.0)
    consumptionTaxValue = Column(DECIMAL(18, 4), default=0.0)
    quantityRefund = Column(DECIMAL(18, 4), default=0.0)
    overCost = Column(DECIMAL(18, 4), default=0.0)
    percentCost = Column(DECIMAL(6, 3), default=0.0)
    withholdingValue = Column(DECIMAL(16, 4), default=0.0)
    interest = Column(DECIMAL(18, 4), default=0.0)
    consumptionTaxPercent = Column(DECIMAL(6, 2), default=0.0)
    globalTax = Column(DECIMAL(5, 2), default=0.0)
    surcharge = Column(DECIMAL(18, 2), default=0.0)
    mainUnitValue = Column(DECIMAL(18, 4), default=0.0)
    conversionFactor = Column(DECIMAL(16, 4), default=0.0)
    icaPercent = Column(DECIMAL(6, 3), default=0.0)
    reteICAPercent = Column(DECIMAL(6, 3), default=0.0)
    cost = Column(DECIMAL(18, 6), default=0.0)
    baseValue = Column(DECIMAL(18, 4), default=0.0)
    disccount = Column(DECIMAL(6, 2), default=0.0)
    iva = Column(DECIMAL(6, 2), default=0.0)
    withholdingTax = Column(DECIMAL(6, 2), default=0.0)
    value = Column(DECIMAL(18, 4), default=0.0)
    detailPrefix = Column(String(5))
    detailDocument = Column(String(10))
    lot = Column(String(50))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    checkNumber = Column(String(10))
    physicalLocation = Column(String(100))
    sourceDocumentPrefix = Column(String(5))
    sourceDocumentNumber = Column(String(10))
    bankCode = Column(String(3))
    bankName = Column(String(50))
    accountNumber = Column(String(50))
    authorizationNumber = Column(String(20))
    partnerId = Column(String(36))
    quoteNumber = Column(TINYINT)

    asset = relationship(u'Asset')
    bankAccount = relationship(u'BankAccount')
    businessAgent = relationship(u'BusinessAgent')
    cashRegister = relationship(u'CashRegister')
    color = relationship(u'Color')
    consumptionTaxPUC = relationship(u'PUC', primaryjoin='DocumentDetail.consumptionTaxPUCId == PUC.pucId')
    costCenter = relationship(u'CostCenter')
    crossDocumentHeader = relationship(u'DocumentHeader',
                                       primaryjoin='DocumentDetail.crossDocumentHeaderId == '
                                                   'DocumentHeader.documentHeaderId')
    customer = relationship(u'Customer')
    dependency = relationship(u'Dependency')
    detailDocumentType = relationship(u'DocumentType',
                                      primaryjoin='DocumentDetail.detailDocumentTypeId == DocumentType.documentTypeId')
    detailWarehouse = relationship(u'Warehouse')
    division = relationship(u'Division')
    documentHeader = relationship(u'DocumentHeader',
                                  primaryjoin='DocumentDetail.documentHeaderId == DocumentHeader.documentHeaderId')
    employee = relationship(u'Employee')
    financialEntity = relationship(u'FinancialEntity')
    ivaPUC = relationship(u'PUC', primaryjoin='DocumentDetail.ivaPUCId == PUC.pucId')
    importConcept = relationship(u'ImportConcept')
    item = relationship(u'Item', lazy='joined')
    kitAsset = relationship(u'KitAsset')
    kitItem = relationship(u'KitItem')
    kitLabor = relationship(u'KitLabor')
    measurementUnit = relationship(u'MeasurementUnit', lazy='joined')
    otherThird = relationship(u'OtherThird')
    puc = relationship(u'PUC', primaryjoin='DocumentDetail.pucId == PUC.pucId')
    payrollConcept = relationship(u'PayrollConcept')
    payrollEntity = relationship(u'PayrollEntity')
    piece = relationship(u'Piece')
    provider = relationship(u'Provider')
    section = relationship(u'Section')
    size = relationship(u'Size')
    sourceDocumentDetail = relationship(u'DocumentDetail', remote_side=[documentDetailId])
    sourceDocumentType = relationship(u'DocumentType',
                                      primaryjoin='DocumentDetail.sourceDocumentTypeId == DocumentType.documentTypeId')
    thirdParty = relationship(u'ThirdParty')
    third = relationship(u'ThirdParty', foreign_keys=[thirdId])
    withholdingTaxPUC = relationship(u'PUC', primaryjoin='DocumentDetail.withholdingTaxPUCId == PUC.pucId')
    serialDetail = relationship(u'SerialDetail', lazy='dynamic',
                                primaryjoin='DocumentDetail.documentDetailId == SerialDetail.documentDetailId')
    serialAdjustment = relationship(u'SerialAdjustment', lazy='dynamic',
                                    primaryjoin='DocumentDetail.documentDetailId == SerialAdjustment.documentDetailId')

    def __init__(self):
        self.listSerials = []
        self.source_document_detail = None
        self.serialAdjustmentList = []

    def export_data(self):
        """
        Allow export an document header object
        :return:  Document header object in JSon format
        """
        return {
            'documentDetailId': self.documentDetailId,
            'documentHeaderId': self.documentHeaderId,
            'crossDocumentHeaderId': self.crossDocumentHeaderId,
            'assetId': self.assetId,
            'asset': None if self.asset is None else self.asset.export_simple(),
            'sourceDocumentDetailId': self.sourceDocumentDetailId,
            'sectionId': self.sectionId,
            'bankAccountId': self.bankAccountId,
            'financialEntityId': self.financialEntityId,
            'kitLaborId': self.kitLaborId,
            'importConceptId': self.importConceptId,
            'cashRegisterId': self.cashRegisterId,
            'kitItemId': self.kitItemId,
            'detailDocumentTypeId': self.detailDocumentTypeId,
            'sourceDocumentTypeId': self.sourceDocumentTypeId,
            'colorId': self.colorId,
            'itemId': self.itemId,
            'pieceId': self.pieceId,
            'employeeId': self.employeeId,
            'payrollEntityId': self.payrollEntityId,
            'divisionId': self.divisionId,
            'sizeId': self.sizeId,
            'providerId': self.providerId,
            'provider': None if self.provider is None else self.provider.export_data_simple(self.provider),
            'measurementUnitId': self.measurementUnitId,
            'kitAssetId': self.kitAssetId,
            'consumptionTaxPUCId': self.consumptionTaxPUCId,
            'pucId': self.pucId,
            'thirdId': self.thirdId,
            'third': None if self.third is None else self.third.export_simple(),
            'detailWarehouseId': self.detailWarehouseId,
            'detailWarehouse': None if self.detailWarehouse is None else Warehouse.export_data_simple(self.detailWarehouse),
            'otherThirdId': self.otherThirdId,
            'dependencyId': self.dependencyId,
            'costCenterId': self.costCenterId,
            'ivaPUCId': self.ivaPUCId,
            'ivaPUC': None if self.ivaPUC is None or self.ivaPUCId is None else {
                'pucId': self.ivaPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaPUC.pucClass,
                                                           self.ivaPUC.pucSubClass,
                                                           self.ivaPUC.account, self.ivaPUC.subAccount,
                                                           self.ivaPUC.auxiliary1, self.ivaPUC.name),
                'percentage': self.ivaPUC.percentage
            },
            'withholdingTaxPUCId': self.withholdingTaxPUCId,
            'customerId': self.customerId,
            'businessAgentId': self.businessAgentId,
            'payrollConceptId': self.payrollConceptId,
            'detailDate': self.detailDate,
            'dueDate': self.dueDate,
            'initialDate': self.initialDate,
            'finalDate': self.finalDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'selected': self.selected,
            'isDeleted': self.isDeleted,
            'ivaCustomer': self.ivaCustomer,
            'reteICA': self.reteICA,
            'quantity': self.quantity,
            'units': self.units,
            'unitValue': self.unitValue,
            'availableStock': self.availableStock,
            'amount': self.amount,
            'balance': self.balance,
            'consumptionTaxBase': self.consumptionTaxBase,
            'consumptionTaxValue': self.consumptionTaxValue,
            'quantityRefund': self.quantityRefund,
            'overCost': self.overCost,
            'percentCost': self.percentCost,
            'withholdingValue': self.withholdingValue,
            'interest': self.interest,
            'consumptionTaxPercent': self.consumptionTaxPercent,
            'globalTax': self.globalTax,
            'surcharge': self.surcharge,
            'mainUnitValue': self.mainUnitValue,
            'conversionFactor': self.conversionFactor,
            'icaPercent': self.icaPercent,
            'reteICAPercent': self.reteICAPercent,
            'cost': self.cost,
            'baseValue': self.baseValue,
            'disccount': self.disccount,
            'iva': self.iva,
            'withholdingTax': self.withholdingTax,
            'withholdingTaxPUC': None if self.withholdingTaxPUC is None or
                                         self.withholdingTaxPUCId is None else {
                'pucId': self.withholdingTaxPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxPUC.pucClass,
                                                           self.withholdingTaxPUC.pucSubClass,
                                                           self.withholdingTaxPUC.account,
                                                           self.withholdingTaxPUC.subAccount,
                                                           self.withholdingTaxPUC.auxiliary1,
                                                           self.withholdingTaxPUC.name),
                'percentage': self.withholdingTaxPUC.percentage
            },
            'value': self.value,
            'detailPrefix': self.detailPrefix,
            'detailDocument': self.detailDocument,
            'lot': self.lot,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'checkNumber': self.checkNumber,
            'physicalLocation': self.physicalLocation,
            'sourceDocumentPrefix': self.sourceDocumentPrefix,
            'sourceDocumentNumber': self.sourceDocumentNumber,
            'bankCode': self.bankCode,
            'bankName': self.bankName,
            'accountNumber': self.accountNumber,
            'authorizationNumber': self.authorizationNumber,
            'partnerId': self.partnerId,
            'quoteNumber': self.quoteNumber,
            'puc': None if self.puc is None else self.puc.export_account(),
            'item': None if self.item is None else self.item.export_data_document(),
            'search': None,
            'consumptionTaxPUC': None if self.consumptionTaxPUC is None else self.consumptionTaxPUC.export_data(),
            'sourceDocumentDetail': None if self.sourceDocumentDetail is None
                                    else self.sourceDocumentDetail.export_data(),
            'listSerials': None if self.serialDetail is None else [s.serial.export_data_simple()
                                                                   for s in self.serialDetail
                                                                   if self.documentHeaderId == s.documentHeaderId],
        }

    def export_data_concepts(self):
        """
        Allow export an document detail example: Purchase investments, etc (without items) 
        :return:  Document header object in JSon format
        """
        return {
            'documentDetailId': self.documentDetailId,
            'documentHeaderId': self.documentHeaderId,
            'crossDocumentHeaderId': self.crossDocumentHeaderId,
            'assetId': self.assetId,
            'asset': None if self.asset is None else self.asset.export_simple(),
            'sourceDocumentDetailId': self.sourceDocumentDetailId,
            'sectionId': self.sectionId,
            'bankAccountId': self.bankAccountId,
            'financialEntityId': self.financialEntityId,
            'kitLaborId': self.kitLaborId,
            'importConceptId': self.importConceptId,
            'cashRegisterId': self.cashRegisterId,
            'kitItemId': self.kitItemId,
            'detailDocumentTypeId': self.detailDocumentTypeId,
            'pieceId': self.pieceId,
            'employeeId': self.employeeId,
            'payrollEntityId': self.payrollEntityId,
            'divisionId': self.divisionId,
            'providerId': self.providerId,
            'measurementUnitId': self.measurementUnitId,
            'kitAssetId': self.kitAssetId,
            'consumptionTaxPUCId': self.consumptionTaxPUCId,
            'pucId': self.pucId,
            'thirdId': self.thirdId,
            'third': None if self.third is None else self.third.export_simple(),
            'detailWarehouseId': self.detailWarehouseId,
            'otherThirdId': self.otherThirdId,
            'dependencyId': self.dependencyId,
            'costCenterId': self.costCenterId,
            'ivaPUCId': self.ivaPUCId,
            'withholdingTaxPUCId': self.withholdingTaxPUCId,
            'customerId': self.customerId,
            'businessAgentId': self.businessAgentId,
            'payrollConceptId': self.payrollConceptId,
            'detailDate': self.detailDate,
            'dueDate': self.dueDate,
            'initialDate': self.initialDate,
            'finalDate': self.finalDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'selected': self.selected,
            'isDeleted': self.isDeleted,
            'ivaCustomer': self.ivaCustomer,
            'reteICA': self.reteICA,
            'quantity': self.quantity,
            'units': self.units,
            'unitValue': self.unitValue,
            'availableStock': self.availableStock,
            'amount': self.amount,
            'balance': self.balance,
            'consumptionTaxBase': self.consumptionTaxBase,
            'consumptionTaxValue': self.consumptionTaxValue,
            'quantityRefund': self.quantityRefund,
            'overCost': self.overCost,
            'percentCost': self.percentCost,
            'withholdingValue': self.withholdingValue,
            'interest': self.interest,
            'consumptionTaxPercent': self.consumptionTaxPercent,
            'globalTax': self.globalTax,
            'surcharge': self.surcharge,
            'mainUnitValue': self.mainUnitValue,
            'conversionFactor': self.conversionFactor,
            'icaPercent': self.icaPercent,
            'reteICAPercent': self.reteICAPercent,
            'cost': self.cost,
            'baseValue': self.baseValue,
            'disccount': self.disccount,
            'iva': self.iva,
            'withholdingTax': self.withholdingTax,
            'value': self.value,
            'detailPrefix': self.detailPrefix,
            'detailDocument': self.detailDocument,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'checkNumber': self.checkNumber,
            'physicalLocation': self.physicalLocation,
            'sourceDocumentPrefix': self.sourceDocumentPrefix,
            'sourceDocumentNumber': self.sourceDocumentNumber,
            'bankCode': self.bankCode,
            'bankName': self.bankName,
            'accountNumber': self.accountNumber,
            'authorizationNumber': self.authorizationNumber,
            'partnerId': self.partnerId,
            'quoteNumber': self.quoteNumber,
            'puc': None if self.puc is None else self.puc.export_account(),
            'search': None,
            'consumptionTaxPUC': None if self.consumptionTaxPUC is None else self.consumptionTaxPUC.export_data(),
            'withholdingTaxPUC': None if self.withholdingTaxPUC is None or
                                                 self.withholdingTaxPUCId is None else {
                'pucId': self.withholdingTaxPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.withholdingTaxPUC.pucClass,
                                                           self.withholdingTaxPUC.pucSubClass,
                                                           self.withholdingTaxPUC.account,
                                                           self.withholdingTaxPUC.subAccount,
                                                           self.withholdingTaxPUC.auxiliary1,
                                                           self.withholdingTaxPUC.name),
                'percentage': self.withholdingTaxPUC.percentage
            },
            'ivaPUC': None if self.ivaPUC is None or self.ivaPUCId is None else {
                'pucId': self.ivaPUC.pucId,
                'pucAccount': '{0}{1}{2}{3}{4} {5}'.format(self.ivaPUC.pucClass,
                                                           self.ivaPUC.pucSubClass,
                                                           self.ivaPUC.account, self.ivaPUC.subAccount,
                                                           self.ivaPUC.auxiliary1, self.ivaPUC.name),
                'percentage': self.ivaPUC.percentage
            },
            'listSerials': None if self.serialDetail is None else [s.serial.export_data_simple()
                                                                   for s in self.serialDetail
                                                                   if self.documentHeaderId == s.documentHeaderId],
        }

    def export_data_simple(self):
        """
        Allow export a simple dict of document details object (used when call document that is made based in other, e.g:
        Remission based on purchase order)
        :return: a document detail in JSON format
        """
        return {
            'documentDetailId': self.documentDetailId,
            'itemId': self.itemId,
            'quantity': self.quantity,
            'quantityRefund': self.quantityRefund,
            'units': self.units,
            'sourceDocumentDetailId': self.sourceDocumentDetailId,
            'value': self.value,
            'balance': self.balance,
            'lot': self.lot,
            'dueDate': self.dueDate,
            'sizeId': self.sizeId,
            'colorId': self.colorId
        }

    def export_data_inventory(self):
        """
        Allow export an document header object
        :return:  Document header object in JSon format
        """
        return {
            'documentDetailId': self.documentDetailId,
            'documentHeaderId': self.documentHeaderId,
            'crossDocumentHeaderId': self.crossDocumentHeaderId,
            'assetId': self.assetId,
            'asset': None if self.asset is None else self.asset.export_simple(),
            'sourceDocumentDetailId': self.sourceDocumentDetailId,
            'sectionId': self.sectionId,
            'bankAccountId': self.bankAccountId,
            'financialEntityId': self.financialEntityId,
            'kitLaborId': self.kitLaborId,
            'importConceptId': self.importConceptId,
            'cashRegisterId': self.cashRegisterId,
            'kitItemId': self.kitItemId,
            'detailDocumentTypeId': self.detailDocumentTypeId,
            'sourceDocumentTypeId': self.sourceDocumentTypeId,
            'colorId': self.colorId,
            'color': None if self.color is None else self.color.export_data(),
            'itemId': self.itemId,
            'pieceId': self.pieceId,
            'employeeId': self.employeeId,
            'payrollEntityId': self.payrollEntityId,
            'divisionId': self.divisionId,
            'sizeId': self.sizeId,
            'size': None if self.size is None else self.size.export_data(),
            'providerId': self.providerId,
            'measurementUnitId': self.measurementUnitId,
            'kitAssetId': self.kitAssetId,
            'consumptionTaxPUCId': self.consumptionTaxPUCId,
            'pucId': self.pucId,
            'thirdId': self.thirdId,
            'third': None if self.third is None else self.third.export_simple(),
            'detailWarehouseId': self.detailWarehouseId,
            'detailWarehouse': None if self.detailWarehouse is None else Warehouse.export_data_simple(self.detailWarehouse),
            'otherThirdId': self.otherThirdId,
            'dependencyId': self.dependencyId,
            'costCenterId': self.costCenterId,
            'ivaPUCId': self.ivaPUCId,
            'withholdingTaxPUCId': self.withholdingTaxPUCId,
            'customerId': self.customerId,
            'businessAgentId': self.businessAgentId,
            'payrollConceptId': self.payrollConceptId,
            'detailDate': self.detailDate,
            'dueDate': self.dueDate,
            'initialDate': self.initialDate,
            'finalDate': self.finalDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'selected': self.selected,
            'isDeleted': self.isDeleted,
            'ivaCustomer': self.ivaCustomer,
            'reteICA': self.reteICA,
            'quantity': self.quantity,
            'units': self.units,
            'unitValue': self.unitValue,
            'availableStock': self.availableStock,
            'amount': self.amount,
            'balance': self.balance,
            'consumptionTaxBase': self.consumptionTaxBase,
            'consumptionTaxValue': self.consumptionTaxValue,
            'quantityRefund': self.quantityRefund,
            'overCost': self.overCost,
            'percentCost': self.percentCost,
            'withholdingValue': self.withholdingValue,
            'interest': self.interest,
            'consumptionTaxPercent': self.consumptionTaxPercent,
            'globalTax': self.globalTax,
            'surcharge': self.surcharge,
            'mainUnitValue': self.mainUnitValue,
            'conversionFactor': self.conversionFactor,
            'icaPercent': self.icaPercent,
            'reteICAPercent': self.reteICAPercent,
            'cost': self.cost,
            'baseValue': self.baseValue,
            'disccount': self.disccount,
            'iva': self.iva,
            'withholdingTax': self.withholdingTax,
            'value': self.value,
            'detailPrefix': self.detailPrefix,
            'detailDocument': self.detailDocument,
            'lot': self.lot,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'checkNumber': self.checkNumber,
            'physicalLocation': self.physicalLocation,
            'sourceDocumentPrefix': self.sourceDocumentPrefix,
            'sourceDocumentNumber': self.sourceDocumentNumber,
            'bankCode': self.bankCode,
            'bankName': self.bankName,
            'accountNumber': self.accountNumber,
            'authorizationNumber': self.authorizationNumber,
            'partnerId': self.partnerId,
            'quoteNumber': self.quoteNumber,
            'item': None if self.item is None else self.item.export_data_document(),
            'search': None,
            'listSerials': None if self.serialDetail is None else [s.serial.export_data_simple()
                                                                   for s in self.serialDetail
                                                                   if self.documentHeaderId == s.documentHeaderId],
            'serialAdjustmentList': None if self.serialAdjustment is None else [s.export_data()
                                                                                for s in self.serialAdjustment
                                                                                if
                                                                                self.documentDetailId == s.documentDetailId],
        }

    def import_data(self, data):
        """
        Allow create a un new document detail according to data
        :param data: information by new document detail
        :exception: keyError An error occurs when a key not set in data
        :return: A document detail in JSON format
        """
        if 'documentDetailId' in data:
            self.documentDetailId = data['documentDetailId']
        if 'documentHeaderId' in data:
            self.documentHeaderId = data['documentHeaderId']
        if 'crossDocumentHeaderId' in data:
            self.crossDocumentHeaderId = data['crossDocumentHeaderId']
        if 'assetId' in data:
            self.assetId = data['assetId']
        if 'sourceDocumentDetailId' in data:
            self.sourceDocumentDetailId = data['sourceDocumentDetailId']
        if 'sectionId' in data:
            self.sectionId = data['sectionId']
        if 'bankAccountId' in data:
            self.bankAccountId = data['bankAccountId']
        if 'financialEntityId' in data:
            self.financialEntityId = data['financialEntityId']
        if 'kitLaborId' in data:
            self.kitLaborId = data['kitLaborId']
        if 'importConceptId' in data:
            self.importConceptId = data['importConceptId']
        if 'cashRegisterId' in data:
            self.cashRegisterId = data['cashRegisterId']
        if 'kitItemId' in data:
            self.kitItemId = data['kitItemId']
        if 'detailDocumentTypeId' in data:
            self.detailDocumentTypeId = data['detailDocumentTypeId']
        if 'sourceDocumentTypeId' in data:
            self.sourceDocumentTypeId = data['sourceDocumentTypeId']
        if 'colorId' in data:
            self.colorId = data['colorId']
        if 'itemId' in data:
            self.itemId = data['itemId']
        if 'pieceId' in data:
            self.pieceId = data['pieceId']
        if 'employeeId' in data:
            self.employeeId = data['employeeId']
        if 'payrollEntityId' in data:
            self.payrollEntityId = data['payrollEntityId']
        if 'divisionId' in data:
            self.divisionId = data['divisionId']
        if 'sizeId' in data:
            self.sizeId = data['sizeId']
        if 'providerId' in data:
            self.providerId = data['providerId']
        if 'measurementUnitId' in data:
            self.measurementUnitId = data['measurementUnitId']
        if 'kitAssetId' in data:
            self.kitAssetId = data['kitAssetId']
        if 'consumptionTaxPUCId' in data:
            self.consumptionTaxPUCId = data['consumptionTaxPUCId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'thirdId' in data:
            self.thirdId = data['thirdId']
        if 'detailWarehouseId' in data:
            self.detailWarehouseId = data['detailWarehouseId']
        if 'otherThirdId' in data:
            self.otherThirdId = data['otherThirdId']
        if 'dependencyId' in data:
            self.dependencyId = data['dependencyId']
        if 'costCenterId' in data:
            self.costCenterId = data['costCenterId']
        if 'ivaPUCId' in data:
            self.ivaPUCId = data['ivaPUCId']
        if 'withholdingTaxPUCId' in data:
            self.withholdingTaxPUCId = data['withholdingTaxPUCId']
        if 'customerId' in data:
            self.customerId = data['customerId']
        if 'businessAgentId' in data:
            self.businessAgentId = data['businessAgentId']
        if 'payrollConceptId' in data:
            self.payrollConceptId = data['payrollConceptId']
        if 'detailDate' in data:
            self.detailDate = converters.convert_string_to_date(data['detailDate'])
        if 'dueDate' in data:
            self.dueDate = converters.convert_string_to_date(data['dueDate'])
        if 'initialDate' in data:
            self.initialDate = converters.convert_string_to_date(data['initialDate'])
        if 'finalDate' in data:
            self.finalDate = converters.convert_string_to_date(data['finalDate'])
        if 'creationDate' in data:
            self.creationDate = converters.convert_string_to_date(data['creationDate'])
        if 'updateDate' in data:
            self.updateDate = converters.convert_string_to_date(data['updateDate'])
        if 'selected' in data:
            self.selected = data['selected']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'ivaCustomer' in data:
            self.ivaCustomer = data['ivaCustomer']
        if 'reteICA' in data:
            self.reteICA = data['reteICA']
        if 'quantity' in data:
            self.quantity = data['quantity']
        if 'units' in data:
            self.units = data['units']
        if 'unitValue' in data:
            self.unitValue = data['unitValue']
        if 'availableStock' in data:
            self.availableStock = data['availableStock']
        if 'amount' in data:
            self.amount = data['amount']
        if 'balance' in data:
            self.balance = data['balance']
        if 'consumptionTaxBase' in data:
            self.consumptionTaxBase = data['consumptionTaxBase']
        if 'consumptionTaxValue' in data:
            self.consumptionTaxValue = data['consumptionTaxValue']
        if 'quantityRefund' in data:
            self.quantityRefund = data['quantityRefund']
        if 'overCost' in data:
            self.overCost = data['overCost']
        if 'percentCost' in data:
            self.percentCost = data['percentCost']
        if 'withholdingValue' in data:
            self.withholdingValue = data['withholdingValue']
        if 'interest' in data:
            self.interest = data['interest']
        if 'consumptionTaxPercent' in data:
            self.consumptionTaxPercent = data['consumptionTaxPercent']
        if 'globalTax' in data:
            self.globalTax = data['globalTax']
        if 'surcharge' in data:
            self.surcharge = data['surcharge']
        if 'mainUnitValue' in data:
            self.mainUnitValue = data['mainUnitValue']
        if 'conversionFactor' in data:
            self.conversionFactor = data['conversionFactor']
        if 'icaPercent' in data:
            self.icaPercent = data['icaPercent']
        if 'reteICAPercent' in data:
            self.reteICAPercent = data['reteICAPercent']
        if 'cost' in data:
            self.cost = data['cost']
        if 'baseValue' in data:
            self.baseValue = data['baseValue']
        if 'baseValueIVA' in data:
            self.baseValueIVA = data['baseValueIVA']
        if 'disccount' in data:
            self.disccount = data['disccount']
        if 'iva' in data:
            self.iva = data['iva']
        if 'withholdingTax' in data:
            self.withholdingTax = data['withholdingTax']
        if 'value' in data:
            self.value = data['value']
        if 'detailPrefix' in data:
            self.detailPrefix = data['detailPrefix']
        if 'detailDocument' in data:
            self.detailDocument = data['detailDocument']
        if 'lot' in data:
            self.lot = data['lot']
        if 'comments' in data:
            self.comments = data['comments']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'checkNumber' in data:
            self.checkNumber = data['checkNumber']
        if 'physicalLocation' in data:
            self.physicalLocation = data['physicalLocation']
        if 'sourceDocumentPrefix' in data:
            self.sourceDocumentPrefix = data['sourceDocumentPrefix']
        if 'sourceDocumentNumber' in data:
            self.sourceDocumentNumber = data['sourceDocumentNumber']
        if 'bankCode' in data:
            self.bankCode = data['bankCode']
        if 'bankName' in data:
            self.bankName = data['bankName']
        if 'accountNumber' in data:
            self.accountNumber = data['accountNumber']
        if 'authorizationNumber' in data:
            self.authorizationNumber = data['authorizationNumber']
        if 'partnerId' in data:
            self.partnerId = data['partnerId']
        if 'quoteNumber' in data:
            self.quoteNumber = data['quoteNumber']

        if 'listSerials' in data:
            self.listSerials = data['listSerials']
        if 'serialAdjustmentList' in data:
            self.serialAdjustmentList = data['serialAdjustmentList']
        if 'search' in data:
            self.search = data['search']
        return self

    def save(self):
        """
        Allow save a document detail in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.createdBy = g.user['name']
            self.creationDate = datetime.now()
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def update(self):
        """
        Allow save a document detail in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_document_details_by_document_header_id(id):
        """
        Allow obtain a document details from document header identifier
        :param id: document header identifier
        :return: a document details object in JSON format
        """
        dd = session.query(DocumentDetail).filter(DocumentDetail.documentHeaderId == id).all()
        return dd
