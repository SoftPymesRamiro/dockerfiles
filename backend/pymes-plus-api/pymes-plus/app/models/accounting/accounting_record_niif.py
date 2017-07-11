# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################

__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"
__status__ = "develop"

from datetime import datetime
from ... import Base
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, load_only, aliased, Load, joinedload
from flask import jsonify
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy import or_, and_, func, not_
from .. import Branch, PUC, BankAccount, Dependency, Division, DocumentType, Provider, DefaultValue
from .. import DocumentHeader, DocumentType, DocumentDetail, ExchangeRate, Provider, Company, IVAType, Warehouse
from .. import City, Department, Country, Item, MeasurementUnit, DefaultValue, Branch, AccountingAllThirds, Image
from .. import ExchangeRate
from ...utils import converters
from ...reports import DocumentAccountingPreview


class AccountingRecordNIIF(Base):
    """AccountingRecordNIIF as a public model class.

        """
    __tablename__ = 'accountingrecordsniif'

    accountingRecordNIIFId = Column(Integer, primary_key=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    mainThirdId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    payrollEntityId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    allThirdId = Column(Integer)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    productionOrderId = Column(ForeignKey(u'productionorders.productionOrderId'), index=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    businessAgentId = Column(ForeignKey(u'businessagents.businessAgentId'), index=True)
    payrollConceptId = Column(ForeignKey(u'payrollconcepts.payrollConceptId'), index=True)
    contractId = Column(ForeignKey(u'contracts.contractId'), index=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    assetId = Column(ForeignKey(u'assets.assetId'), index=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    crossDocumentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    cashRegisterId = Column(ForeignKey(u'cashregisters.cashRegisterId'), index=True)
    sourceDocumentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    documentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    financialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    employeeId = Column(ForeignKey(u'employees.employeeId'), index=True)
    cashierId = Column(ForeignKey(u'employees.employeeId'), index=True)
    roleEmployeeId = Column(ForeignKey(u'roleemployees.roleEmployeeId'), index=True)
    importId = Column(ForeignKey(u'imports.importId'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    partnerId = Column(ForeignKey(u'partners.partnerId'), index=True)
    colorId = Column(ForeignKey(u'colors.colorId'), index=True)
    pieceId = Column(ForeignKey(u'pieces.pieceId'), index=True)
    otherThirdId = Column(ForeignKey(u'otherthirds.otherThirdId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    sizeId = Column(ForeignKey(u'sizes.sizeId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    measurementUnitId = Column(ForeignKey(u'measurementunits.measurementUnitId'), index=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    accountingDate = Column(DateTime)
    dueDate = Column(DateTime)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    transfered = Column(Integer)
    ivaToCost = Column(Integer)
    niif = Column(Integer, default=1)
    consumptionToCost = Column(Integer)
    apportionment = Column(Integer)
    foreignCurrency = Column(DECIMAL(18, 5), default=0.0)
    quantity = Column(DECIMAL(18, 5), default=0.0)
    simulatedQuantity = Column(DECIMAL(18, 5), default=0.0)
    units = Column(DECIMAL(18, 5), default=0.0)
    balance = Column(DECIMAL(18, 6), default=0.0)
    baseValue = Column(DECIMAL(18, 6), default=0.0)
    percentage = Column(DECIMAL(7, 4), default=0.0)
    debit = Column(DECIMAL(18, 6), default=0.0)
    simulatedDebit = Column(DECIMAL(18, 6), default=0.0)
    credit = Column(DECIMAL(18, 6), default=0.0)
    simulatedCredit = Column(DECIMAL(18, 6), default=0.0)
    documentPrefix = Column(String(5))
    documentNumber = Column(String(10))
    crossPrefix = Column(String(5))
    crossDocument = Column(String(10))
    lot = Column(String(50))
    sourcePrefix = Column(String(5))
    bankName = Column(String(50))
    cardNumber = Column(String(50))
    sign = Column(String(1))
    sourceDocument = Column(String(10))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    accountNumber = Column(String(50))
    bankCode = Column(String(3))
    quoteNumber = Column(TINYINT)
    allThirdType = Column(String(2))
    asset = relationship(u'Asset')
    bankAccount = relationship(u'BankAccount')
    branch = relationship(u'Branch')
    businessAgent = relationship(u'BusinessAgent')
    cashRegister = relationship(u'CashRegister')
    cashier = relationship(u'Employee', primaryjoin='AccountingRecordNIIF.cashierId == Employee.employeeId')
    color = relationship(u'Color')
    contract = relationship(u'Contract')
    costCenter = relationship(u'CostCenter')
    crossDocumentHeader = relationship(u'DocumentHeader', primaryjoin='AccountingRecordNIIF.crossDocumentHeaderId == DocumentHeader.documentHeaderId')
    customer = relationship(u'Customer')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    documentHeader = relationship(u'DocumentHeader', primaryjoin='AccountingRecordNIIF.documentHeaderId == DocumentHeader.documentHeaderId')
    documentType = relationship(u'DocumentType', primaryjoin='AccountingRecordNIIF.documentTypeId == DocumentType.documentTypeId')
    employee = relationship(u'Employee', primaryjoin='AccountingRecordNIIF.employeeId == Employee.employeeId')
    financialEntity = relationship(u'FinancialEntity')
    _import = relationship(u'Import')
    item = relationship(u'Item')
    thirdParty = relationship(u'ThirdParty')
    measurementUnit = relationship(u'MeasurementUnit')
    otherThird = relationship(u'OtherThird')
    puc = relationship(u'PUC')
    partner = relationship(u'Partner')
    payrollConcept = relationship(u'PayrollConcept')
    payrollEntity = relationship(u'PayrollEntity')
    piece = relationship(u'Piece')
    productionOrder = relationship(u'ProductionOrder')
    provider = relationship(u'Provider')
    roleEmployee = relationship(u'RoleEmployee')
    section = relationship(u'Section')
    size = relationship(u'Size')
    sourceDocumentType = relationship(u'DocumentType', primaryjoin='AccountingRecordNIIF.sourceDocumentTypeId == DocumentType.documentTypeId')
    stage = relationship(u'Stage')
    warehouse = relationship(u'Warehouse')

    def export_data(self):
        """
            Allow export an accounting record niif object
            :return:  Document header object in JSon format
        """
        return {
            'accountingRecordNIIFId': self.accountingRecordNIIFId,
            'customerId': self.customerId,
            'contractId': self.contractId,
            'payrollConceptId': self.payrollConceptId,
            'businessAgentId': self.businessAgentId,
            'productionOrderId': self.productionOrderId,
            'allThirdId': self.allThirdId,
            'otherThirdId': self.otherThirdId,
            'payrollEntityId': self.payrollEntityId,
            'dependencyId': self.dependencyId,
            'warehouseId': self.warehouseId,
            'mainThirdId': self.mainThirdId,
            'pucId': self.pucId,
            'importId': self.importId,
            'providerId': self.providerId,
            'measurementUnitId': self.measurementUnitId,
            'stageId': self.stageId,
            'sizeId': self.sizeId,
            'divisionId': self.divisionId,
            'cashRegisterId': self.cashRegisterId,
            'colorId': self.colorId,
            'partnerId': self.partnerId,
            'pieceId': self.pieceId,
            'itemId': self.itemId,
            'roleEmployeeId': self.roleEmployeeId,
            'bankAccountId': self.bankAccountId,
            'cashierId': self.cashierId,
            'employeeId': self.employeeId,
            'financialEntityId': self.financialEntityId,
            'documentTypeId': self.documentTypeId,
            'sourceDocumentTypeId': self.sourceDocumentTypeId,
            'branchId': self.branchId,
            'sectionId': self.sectionId,
            'costCenterId': self.costCenterId,
            'documentHeaderId': self.documentHeaderId,
            'crossDocumentHeaderId': self.crossDocumentHeaderId,
            'assetId': self.assetId,
            'accountingDate': self.accountingDate,
            'dueDate': self.dueDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'transfered': self.transfered,
            'ivaToCost': self.ivaToCost,
            'niif': self.niif,
            'consumptionToCost': self.consumptionToCost,
            'apportionment': self.apportionment,
            'foreignCurrency': self.foreignCurrency,
            'quantity': self.quantity,
            'simulatedQuantity': self.simulatedQuantity,
            'units': self.units,
            'balance': self.balance,
            'baseValue': self.baseValue,
            'percentage': self.percentage,
            'debit': self.debit,
            'simulatedDebit': self.simulatedDebit,
            'credit': self.credit,
            'simulatedCredit': self.simulatedCredit,
            'documentPrefix': self.documentPrefix,
            'documentNumber': self.documentNumber,
            'crossPrefix': self.crossPrefix,
            'crossDocument': self.crossDocument,
            'lot': self.lot,
            'sourcePrefix': self.sourcePrefix,
            'bankName': self.bankName,
            'cardNumber': self.cardNumber,
            'sign': self.sign,
            'sourceDocument': self.sourceDocument,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'accountNumber': self.accountNumber,
            'bankCode': self.bankCode,
            'quoteNumber': self.quoteNumber,
        }

    def save(self):
        """
            Allow save an accounting record object
        """
        try:
            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    def delete(self):
        """
            Allow delete an accounting record object
        """
        try:
            session.delete(self)
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_accounting_record_by_document_header_id(document_header_id):
        """
        Allow get accounting records by document header id
        :param document_header_id: document header id
        :return: accounting records object
        """
        try:
            accounting_records = session.query(AccountingRecordNIIF) \
                .filter(AccountingRecordNIIF.documentHeaderId == document_header_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)