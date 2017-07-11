# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from ... import Base
from flask import g
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, DECIMAL
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, load_only
from .. import PaymentReceipt, DocumentDetail, CostCenter, Section, Dependency, Division, DocumentType, \
    Provider, DefaultValue, Customer, OtherThird, Partner, ThirdParty, Employee, FinancialEntity, BusinessAgent,\
    PayrollEntity
from .. import ExchangeRate
from ...utils import converters
from ...exceptions import InternalServerError
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import relationship, load_only, aliased, Load, joinedload


class DocumentHeader(Base):
    """DocumentHeader as a public model class.

    """
    __tablename__ = 'documentheaders'

    documentHeaderId = Column(Integer, primary_key=True)
    financialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    cashRegisterId = Column(ForeignKey(u'cashregisters.cashRegisterId'), index=True)
    sourceDocumentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    documentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    sourceId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    destinyBranchId = Column(ForeignKey(u'branches.branchId'), index=True)
    assetId = Column(ForeignKey(u'assets.assetId'), index=True)
    sourceDocumentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    interestPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    reteICAPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    reteIVAPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    insurancePUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    payrollBasicId = Column(ForeignKey(u'payrollbasics.payrollBasicId'), index=True)
    businessAgentId = Column(ForeignKey(u'businessagents.businessAgentId'), index=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    productionOrderId = Column(ForeignKey(u'productionorders.productionOrderId'), index=True)
    withholdingTaxPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    ivaPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    consumptionTaxPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    freightPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    withholdingCREEPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    retentionPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    contractId = Column(ForeignKey(u'contracts.contractId'), index=True)
    payrollEntityId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    otherThirdId = Column(ForeignKey(u'otherthirds.otherThirdId'), index=True)
    billingResolutionId = Column(ForeignKey(u'billingresolutions.billingResolutionId'), index=True)
    sourceWarehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    destinyWarehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    thirdId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    importId = Column(ForeignKey(u'imports.importId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    currencyId = Column(ForeignKey(u'currencies.currencyId'), index=True)
    paymentTermId = Column(ForeignKey(u'paymentterms.paymentTermId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    employeeId = Column(ForeignKey(u'employees.employeeId'), index=True)
    cashierId = Column(ForeignKey(u'employees.employeeId'), index=True)
    partnerId = Column(ForeignKey(u'partners.partnerId'), index=True)
    kitId = Column(ForeignKey(u'kits.kitId'), index=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    documentDate = Column(DateTime)
    dateFrom = Column(DateTime)
    dateTo = Column(DateTime)
    initialDate = Column(DateTime)
    finalDate = Column(DateTime)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    bonusDateFrom = Column(DateTime)
    vacationDateFrom = Column(DateTime)
    auxTimeOne = Column(DateTime)
    auxTimeTwo = Column(DateTime)
    firtsContractDate = Column(DateTime)
    overCostTaxBase = Column(Integer, default=0)
    disccount2Mode = Column(Integer, default=0)
    disccount2TaxBase = Column(Integer, default=0)
    addToPayroll = Column(Integer)
    accounted = Column(Integer, default=0)
    annuled = Column(Integer, default=0)
    freezeBill = Column(Integer, default=0)
    pettyCash = Column(Integer, default=0)
    revolvingFund = Column(Integer, default=0)
    importReplaced = Column(Integer, default=0)
    isConsignment = Column(Integer, default=0)
    state = Column(Integer, default=0)
    retentionMode = Column(Integer, default=0)
    isDeleted = Column(Integer, default=0)
    closingType = Column(Integer, default=0)
    assumedIVA = Column(Integer, default=0)
    isChangeNoted = Column(Integer, default=0)
    exchangeRate = Column(DECIMAL(16, 4), default=0.0)
    subtotal = Column(DECIMAL(18, 4), default=0.0)
    balance = Column(DECIMAL(18, 4), default=0)
    disccountPercent = Column(DECIMAL(6, 2), default=0)
    disccount = Column(DECIMAL(18, 4), default=0)
    insurance = Column(DECIMAL(18, 4), default=0)
    bonus = Column(DECIMAL(18, 4), default=0)
    vacation = Column(DECIMAL(18, 4), default=0)
    percentageCREE = Column(DECIMAL(4, 2), default=0)
    baseCREE = Column(DECIMAL(18, 4), default=0)
    valueCREE = Column(DECIMAL(18, 4), default=0)
    inability = Column(DECIMAL(18, 4), default=0.0)
    layoffValue = Column(DECIMAL(18, 4), default=0.0)
    advanceLayoff = Column(DECIMAL(18, 4), default=0.0)
    sanction = Column(DECIMAL(18, 4), default=0.0)
    importationValue = Column(DECIMAL(18, 4), default=0.0)
    directIVAPercent = Column(DECIMAL(6, 2), default=0.0)
    productionUnits = Column(DECIMAL(16, 4), default=0.0)
    stageCostTotal = Column(DECIMAL(18, 4), default=0.0)
    deductibleRF = Column(DECIMAL(18, 4), default=0.0)
    fspValue = Column(DECIMAL(18, 2), default=0.0)
    directIVA = Column(DECIMAL(18, 4), default=0.0)
    comissionPercent = Column(DECIMAL(6, 2), default=0.0)
    comission = Column(DECIMAL(18, 4), default=0.0)
    expenses = Column(DECIMAL(18, 4), default=0.0)
    adjustment = Column(DECIMAL(18, 4), default=0.0)
    overTax = Column(DECIMAL(18, 2), default=0.0)
    sodicon = Column(DECIMAL(18, 2), default=0.0)
    daysVacation = Column(DECIMAL(6, 2), default=0.0)
    baseSalary = Column(DECIMAL(18, 4), default=0.0)
    epsValue = Column(DECIMAL(18, 2), default=0.0)
    afpValue = Column(DECIMAL(18, 2), default=0.0)
    cash = Column(DECIMAL(18, 4), default=0.0)
    checks = Column(DECIMAL(18, 4), default=0.0)
    total = Column(DECIMAL(18, 4), default=0.0)
    payment = Column(DECIMAL(18, 4), default=0)
    initialQuota = Column(DECIMAL(18, 4), default=0)
    globalTax = Column(DECIMAL(18, 2), default=0.0)
    retentionBase = Column(DECIMAL(18, 4), default=0.0)
    retentionValue = Column(DECIMAL(18, 4), default=0.0)
    overCost = Column(DECIMAL(18, 4), default=0)
    disccount2 = Column(DECIMAL(5, 2), default=0)
    disccount2Value = Column(DECIMAL(18, 4), default=0)
    tipValue = Column(DECIMAL(18, 4), default=0)
    reteICABase = Column(DECIMAL(18, 4), default=0.0)
    reteICAValue = Column(DECIMAL(18, 4), default=0.0)
    consumptionTaxPercent = Column(DECIMAL(6, 2), default=0.0)
    consumptionTaxBase = Column(DECIMAL(18, 4), default=0.0)
    consumptionTaxValue = Column(DECIMAL(18, 4), default=0.0)
    retentionPercent = Column(DECIMAL(6, 2), default=0.0)
    withholdingTaxBase = Column(DECIMAL(18, 4), default=0.0)
    withholdingTaxValue = Column(DECIMAL(18, 4), default=0.0)
    reteIVAPercent = Column(DECIMAL(6, 2), default=0.0)
    reteIVABase = Column(DECIMAL(18, 4), default=0.0)
    reteIVAValue = Column(DECIMAL(18, 4), default=0.0)
    reteICAPercent = Column(DECIMAL(6, 3), default=0.0)
    freight = Column(DECIMAL(18, 4), default=0.0)
    interest = Column(DECIMAL(18, 4), default=0.0)
    ivaPercent = Column(DECIMAL(6, 2), default=0.0)
    ivaBase = Column(DECIMAL(18, 4), default=0.0)
    ivaValue = Column(DECIMAL(18, 4), default=0.0)
    withholdingTaxPercent = Column(DECIMAL(6, 2), default=0.0)
    prefix = Column(String(5))
    documentNumber = Column(String(10))
    controlPrefix = Column(String(5))
    controlNumber = Column(String(10))
    orderNumber = Column(String(20))
    prefixRequisitionNumber = Column(String(5))
    retirement = Column(String(1))
    auxCharacterOne = Column(String(2000))
    auxCharacterTwo = Column(String(2000))
    depositNumber = Column(String(15))
    leadDocumentTo = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    typeThirdParty = Column(String(2))
    payrollPaymentType = Column(String(1))
    shipCity = Column(String(50))
    shipDepartment = Column(String(50))
    shipCountry = Column(String(50))
    shipZipCode = Column(String(10))
    shipPhone = Column(String(30))
    documentTypeConsign = Column(String(1))
    semester = Column(String(1))
    month = Column(String(2))
    realSimulated = Column(String(1))
    comments = Column(String(2000))
    shipTo = Column(String(100))
    shipAddress = Column(String(100))
    requisitionNumber = Column(String(20))
    workNumber = Column(String(20))
    sourcePrefix = Column(String(5))
    sourceDocument = Column(String(10))
    periodicityQuota = Column(String(1))
    year = Column(String(4))
    paymentBy = Column(TINYINT(4), default=0)
    printed = Column(TINYINT(4), default=0)
    quotaNumbers = Column(TINYINT(4), default=0)
    cutNumber = Column(TINYINT(4))
    payrollType = Column(TINYINT(4))
    baseType = Column(TINYINT(4))
    accountsBackward = Column(TINYINT(4), default=0)
    typeAccount = Column(TINYINT(4), default=1)
    auxNumberOne = Column(TINYINT(4))
    auxNumberTwo = Column(TINYINT(4))
    termDays = Column(SMALLINT(6))
    daysWorked = Column(SMALLINT(6))
    daysLicensed = Column(SMALLINT(6))
    daysNetMoney = Column(SMALLINT(6))
    daysEnjoy = Column(SMALLINT(6))
    daysPILA = Column(SMALLINT(6))
    dateComeBack = Column(DateTime)
    vacationMoney = Column(DECIMAL(18, 2), default=0.0)
    daysMoney = Column(SMALLINT(6), nullable=True)

    financialEntity = relationship("FinancialEntity")
    cashRegister = relationship("CashRegister")
    sourceDocumentType = relationship("DocumentType", foreign_keys=[sourceDocumentTypeId])
    documentType = relationship("DocumentType", foreign_keys=[documentTypeId])
    source = relationship("DocumentType", foreign_keys=[sourceId])
    branch = relationship("Branch", foreign_keys=[branchId])
    destinyBranch = relationship("Branch", foreign_keys=[destinyBranchId])
    asset = relationship("Asset")
    sourceDocumentHeader = relationship('DocumentHeader', remote_side=[documentHeaderId])
    interestPUC = relationship("PUC", foreign_keys=[interestPUCId])
    reteICAPUC = relationship("PUC", foreign_keys=[reteICAPUCId])
    reteIVAPUC = relationship("PUC", foreign_keys=[reteIVAPUCId])
    insurancePUC = relationship("PUC", foreign_keys=[insurancePUCId])
    costCenter = relationship("CostCenter")
    section = relationship("Section")
    payrollBasic = relationship("PayrollBasic")
    businessAgent = relationship("BusinessAgent")
    customer = relationship("Customer")
    productionOrder = relationship("ProductionOrder")
    withholdingTaxPUC = relationship("PUC", foreign_keys=[withholdingTaxPUCId])
    puc = relationship("PUC", foreign_keys=[pucId])
    ivaPUC = relationship("PUC", foreign_keys=[ivaPUCId])
    consumptionTaxPUC = relationship("PUC", foreign_keys=[consumptionTaxPUCId])
    freightPUC = relationship("PUC", foreign_keys=[freightPUCId])
    withholdingCREEPUC = relationship("PUC", foreign_keys=[withholdingCREEPUCId])
    retentionPUC = relationship("PUC", foreign_keys=[retentionPUCId])
    contract = relationship("Contract", foreign_keys=[contractId])
    payrollEntity = relationship("PayrollEntity", foreign_keys=[payrollEntityId])
    otherThird = relationship("OtherThird", foreign_keys=[otherThirdId])
    billingResolution = relationship("BillingResolution", foreign_keys=[billingResolutionId])
    sourceWarehouse = relationship("Warehouse", foreign_keys=[sourceWarehouseId])
    destinyWarehouse = relationship("Warehouse", foreign_keys=[destinyWarehouseId])
    third = relationship("ThirdParty", foreign_keys=[thirdId])
    _import = relationship("Import", foreign_keys=[importId])
    division = relationship("Division", foreign_keys=[divisionId])
    stage = relationship("Stage", foreign_keys=[stageId])
    currency = relationship("Currency", foreign_keys=[currencyId])
    paymentTerm = relationship("PaymentTerm", foreign_keys=[paymentTermId])
    dependency = relationship("Dependency", foreign_keys=[dependencyId])
    bankAccount = relationship("BankAccount", foreign_keys=[bankAccountId])
    employee = relationship("Employee", foreign_keys=[employeeId])
    cashier = relationship("Employee", foreign_keys=[cashierId])
    partner = relationship("Partner", foreign_keys=[partnerId])
    kit = relationship("Kit", foreign_keys=[kitId])
    provider = relationship("Provider", foreign_keys=[providerId])
    documentDetails = relationship('DocumentDetail', lazy='dynamic',
                                   primaryjoin=documentHeaderId == DocumentDetail.documentHeaderId,
                                   order_by='DocumentDetail.documentDetailId')

    paymentReceipt = relationship('PaymentReceipt', lazy='dynamic',
                                  primaryjoin=documentHeaderId == PaymentReceipt.documentHeaderId)

    def __repr__(self):
        return "{0} {1}".format(self.documentNumber, self.documentType.shortWord)

    def export_search(self):
        """
         Allow export a document header object
         :return:  Document header object in JSon format
         """
        def tostr(data):
            """
            Allow convert to json object
            :param data: object
            :return: json string
            """
            return "{0} {1} {2} {3} {4} - {5}".format(
                "" if data.thirdParty.tradeName is None
                else data.thirdParty.tradeName.strip(),
                "" if data.thirdParty.lastName is None
                else data.thirdParty.lastName.strip(),
                "" if data.thirdParty.maidenName is None
                else data.thirdParty.maidenName.strip(),
                "" if data.thirdParty.firstName is None
                else data.thirdParty.firstName.strip(),
                "" if data.thirdParty.identificationNumber is None
                else "({0})".format(data.thirdParty.identificationNumber.strip()),
                " - " if type(data) == type(Partner()) or data.name is None else " - "+data.name,
                "" if type(data) != type(Partner()) and not data.isMain else "(P)") if data and data.thirdParty else ""

        return {
            'annuled': self.annuled,
            'documentHeaderId': self.documentHeaderId,
            'prefix': self.prefix,
            'documentNumber': self.documentNumber,
            'documentDate': self.documentDate,
            'controlPrefix': self.controlPrefix,
            'controlNumber': self.controlNumber,
            'orderNumber': self.orderNumber,
            'dateComeBack': self.dateComeBack,
            'vacationMoney': self.vacationMoney,
            'billingResolutionId': self.billingResolutionId,
            'daysMoney': self.daysMoney,
            'documentTypeId': self.documentTypeId,
            'documentType': None if self.documentType is None else self.documentType.export_data(),
            'dateFrom': self.dateFrom,
            'dateTo': self.dateTo,
            'customerId': self.customerId,
            'customer': None if self.customer is None else tostr(self.customer),
            'providerId': self.providerId,
            'provider': None if self.provider is None else tostr(self.provider),
            'thirdId': self.thirdId,
            'third': None if self.third is None else self.third.export_data(),
            'employeeId': self.employeeId,
            'employee': None if self.employee is None else str(self.employee),
            'businessAgentId': self.businessAgentId,
            'businessAgent': None if self.businessAgent is None else tostr(self.businessAgent),
            'financialEntityId': self.financialEntityId,
            'financialEntity': None if self.financialEntity is None else str(self.financialEntity),
            'partnerId': self.partnerId,
            'partner': None if self.partner is None else tostr(self.partner),
            'payrollEntityId': self.payrollEntityId,
            'payrollEntity': None if self.payrollEntity is None else str(self.payrollEntity),
            'total': self.total
        }

    def export_data(self):
        """
        Allow export a document header object
        :return:  Document header object in JSon format
        """
        return {
            'documentHeaderId': self.documentHeaderId,
            'financialEntityId': self.financialEntityId,
            'cashRegisterId': self.cashRegisterId,
            'sourceDocumentTypeId': self.sourceDocumentTypeId,
            'documentTypeId': self.documentTypeId,
            'sourceId': self.sourceId,
            'branchId': self.branchId,
            'destinyBranchId': self.destinyBranchId,
            'assetId': self.assetId,
            'sourceDocumentHeaderId': self.sourceDocumentHeaderId,
            'interestPUCId': self.interestPUCId,
            'reteICAPUCId': self.reteICAPUCId,
            'reteIVAPUCId': self.reteIVAPUCId,
            'insurancePUCId': self.insurancePUCId,
            'costCenterId': self.costCenterId,
            'sectionId': self.sectionId,
            'payrollBasicId': self.payrollBasicId,
            'businessAgentId': self.businessAgentId,
            'customerId': self.customerId,
            'productionOrderId': self.productionOrderId,
            'withholdingTaxPUCId': self.withholdingTaxPUCId,
            'pucId': self.pucId,
            'ivaPUCId': self.ivaPUCId,
            'consumptionTaxPUCId': self.consumptionTaxPUCId,
            'freightPUCId': self.freightPUCId,
            'withholdingCREEPUCId': self.withholdingCREEPUCId,
            'retentionPUCId': self.retentionPUCId,
            'contractId': self.contractId,
            'payrollEntityId': self.payrollEntityId,
            'otherThirdId': self.otherThirdId,
            'billingResolutionId': self.billingResolutionId,
            'sourceWarehouseId': self.sourceWarehouseId,
            'destinyWarehouseId': self.destinyWarehouseId,
            'thirdId': self.thirdId,
            'importId': self.importId,
            'divisionId': self.divisionId,
            'stageId': self.stageId,
            'currencyId': self.currencyId,
            'paymentTermId': self.paymentTermId,
            'dependencyId': self.dependencyId,
            'bankAccountId': self.bankAccountId,
            'employeeId': self.employeeId,
            'cashierId': self.cashierId,
            'partnerId': self.partnerId,
            'kitId': self.kitId,
            'providerId': self.providerId,
            'documentDate': self.documentDate,
            'dateFrom': self.dateFrom,
            'dateTo': self.dateTo,
            'initialDate': self.initialDate,
            'finalDate': self.finalDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'bonusDateFrom': self.bonusDateFrom,
            'vacationDateFrom': self.vacationDateFrom,
            'auxTimeOne': self.auxTimeOne,
            'auxTimeTwo': self.auxTimeTwo,
            'firtsContractDate': self.firtsContractDate,
            'overCostTaxBase': self.overCostTaxBase,
            'disccount2Mode': self.disccount2Mode,
            'disccount2TaxBase': self.disccount2TaxBase,
            'addToPayroll': self.addToPayroll,
            'accounted': self.accounted,
            'annuled': self.annuled,
            'freezeBill': self.freezeBill,
            'pettyCash': self.pettyCash,
            'revolvingFund': self.revolvingFund,
            'importReplaced': self.importReplaced,
            'isConsignment': self.isConsignment,
            'state': self.state,
            'retentionMode': self.retentionMode,
            'isDeleted': self.isDeleted,
            'closingType': self.closingType,
            'assumedIVA': self.assumedIVA,
            'isChangeNoted': self.isChangeNoted,
            'exchangeRate': self.exchangeRate,
            'subtotal': self.subtotal,
            'balance': self.balance,
            'disccountPercent': self.disccountPercent,
            'disccount': self.disccount,
            'insurance': self.insurance,
            'bonus': self.bonus,
            'vacation': self.vacation,
            'percentageCREE': self.percentageCREE,
            'baseCREE': self.baseCREE,
            'valueCREE': self.valueCREE,
            'inability': self.inability,
            'layoffValue': self.layoffValue,
            'advanceLayoff': self.advanceLayoff,
            'sanction': self.sanction,
            'importationValue': self.importationValue,
            'directIVAPercent': self.directIVAPercent,
            'productionUnits': self.productionUnits,
            'stageCostTotal': self.stageCostTotal,
            'deductibleRF': self.deductibleRF,
            'fspValue': self.fspValue,
            'directIVA': self.directIVA,
            'comissionPercent': self.comissionPercent,
            'comission': self.comission,
            'expenses': self.expenses,
            'adjustment': self.adjustment,
            'overTax': self.overTax,
            'sodicon': self.sodicon,
            'daysVacation': self.daysVacation,
            'baseSalary': self.baseSalary,
            'epsValue': self.epsValue,
            'afpValue': self.afpValue,
            'cash': self.cash,
            'checks': self.checks,
            'total': self.total,
            'payment': self.payment,
            'initialQuota': self.initialQuota,
            'globalTax': self.globalTax,
            'retentionBase': self.retentionBase,
            'retentionValue': self.retentionValue,
            'overCost': self.overCost,
            'disccount2': self.disccount2,
            'disccount2Value': self.disccount2Value,
            'tipValue': self.tipValue,
            'reteICABase': self.reteICABase,
            'reteICAValue': self.reteICAValue,
            'consumptionTaxPercent': self.consumptionTaxPercent,
            'consumptionTaxBase': self.consumptionTaxBase,
            'consumptionTaxValue': self.consumptionTaxValue,
            'retentionPercent': self.retentionPercent,
            'withholdingTaxBase': self.withholdingTaxBase,
            'withholdingTaxValue': self.withholdingTaxValue,
            'reteIVAPercent': self.reteIVAPercent,
            'reteIVABase': self.reteIVABase,
            'reteIVAValue': self.reteIVAValue,
            'reteICAPercent': self.reteICAPercent,
            'freight': self.freight,
            'interest': self.interest,
            'ivaPercent': self.ivaPercent,
            'ivaBase': self.ivaBase,
            'ivaValue': self.ivaValue,
            'withholdingTaxPercent': self.withholdingTaxPercent,
            'prefix': self.prefix,
            'documentNumber': self.documentNumber,
            'controlPrefix': self.controlPrefix,
            'controlNumber': self.controlNumber,
            'orderNumber': self.orderNumber,
            'prefixRequisitionNumber': self.prefixRequisitionNumber,
            'retirement': self.retirement,
            'auxCharacterOne': self.auxCharacterOne,
            'auxCharacterTwo': self.auxCharacterTwo,
            'depositNumber': self.depositNumber,
            'leadDocumentTo': self.leadDocumentTo,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'typeThirdParty': self.typeThirdParty,
            'payrollPaymentType': self.payrollPaymentType,
            'shipCity': self.shipCity,
            'shipDepartment': self.shipDepartment,
            'shipCountry': self.shipCountry,
            'shipZipCode': self.shipZipCode,
            'shipPhone': self.shipPhone,
            'documentTypeConsign': self.documentTypeConsign,
            'semester': self.semester,
            'month': self.month,
            'realSimulated': self.realSimulated,
            'comments': self.comments,
            'shipTo': self.shipTo,
            'shipAddress': self.shipAddress,
            'requisitionNumber': self.requisitionNumber,
            'workNumber': self.workNumber,
            'sourcePrefix': self.sourcePrefix,
            'sourceDocument': self.sourceDocument,
            'periodicityQuota': self.periodicityQuota,
            'year': self.year,
            'paymentBy': self.paymentBy,
            'printed': self.printed,
            'quotaNumbers': self.quotaNumbers,
            'cutNumber': self.cutNumber,
            'payrollType': self.payrollType,
            'baseType': self.baseType,
            'accountsBackward': self.accountsBackward,
            'typeAccount': self.typeAccount,
            'auxNumberOne': self.auxNumberOne,
            'auxNumberTwo': self.auxNumberTwo,
            'termDays': self.termDays,
            'daysWorked': self.daysWorked,
            'daysLicensed': self.daysLicensed,
            'daysNetMoney': self.daysNetMoney,
            'daysEnjoy': self.daysEnjoy,
            'daysPILA': self.daysPILA,
            'dateComeBack': self.dateComeBack,
            'vacationMoney': self.vacationMoney,
            'daysMoney': self.daysMoney,

            'financialEntity': None if self.financialEntity is None else self.financialEntity.export_data(),
            'cashRegister': None if self.cashRegister is None else self.cashRegister.export_data(),
            'sourceDocumentType': None if self.sourceDocumentType is None else self.sourceDocumentType.export_data(),
            'documentType': None if self.documentType is None else self.documentType.export_data(),
            'source': None if self.source is None else self.source.export_data(),
            'branch': None if self.branch is None else self.branch.export_data(),
            'destinyBranch': None if self.destinyBranch is None else self.destinyBranch.export_data(),
            'asset': None if self.asset is None else self.asset.export_data(),
            'sourceDocumentHeader': None if self.sourceDocumentHeader is None else self.sourceDocumentHeader.export_data(),
            'interestPUC': None if self.interestPUC is None else self.interestPUC.export_data(),
            'reteICAPUC': None if self.reteICAPUC is None else self.reteICAPUC.export_data(),
            'reteIVAPUC': None if self.reteIVAPUC is None else self.reteIVAPUC.export_data(),
            'insurancePUC': None if self.insurancePUC is None else self.insurancePUC.export_data(),
            'costCenter': None if self.costCenter is None else CostCenter.export_data(self.costCenter),
            'section': None if self.section is None else Section.export_data(self.section),
            'payrollBasic': None if self.payrollBasic is None else self.payrollBasic.export_data(),
            'businessAgent': None if self.businessAgent is None else self.businessAgent.export_data(),
            'customer': None if self.customer is None else self.customer.export_data(),
            'productionOrder': None if self.productionOrder is None else self.productionOrder.export_data(),
            'withholdingTaxPUC': None if self.withholdingTaxPUC is None else self.withholdingTaxPUC.export_data(),
            'puc': None if self.puc is None else self.puc.export_data(),
            'ivaPUC': None if self.ivaPUC is None else self.ivaPUC.export_data(),
            'consumptionTaxPUC': None if self.consumptionTaxPUC is None else self.consumptionTaxPUC.export_data(),
            'freightPUC': None if self.freightPUC is None else self.freightPUC.export_data(),
            'withholdingCREEPUC': None if self.withholdingCREEPUC is None else self.withholdingCREEPUC.export_data(),
            'retentionPUC': None if self.retentionPUC is None else self.retentionPUC.export_data(),
            'contract': None if self.contract is None else self.contract.export_data(),
            'payrollEntity': None if self.payrollEntity is None else self.payrollEntity.export_data(),
            'otherThird': None if self.otherThird is None else self.otherThird.export_data(),
            'billingResolution': None if self.billingResolution is None else self.billingResolution.export_data(),
            'sourceWarehouse': None if self.sourceWarehouse is None else self.sourceWarehouse.export_data(),
            'destinyWarehouse': None if self.destinyWarehouse is None else self.destinyWarehouse.export_data(),
            'third': None if self.third is None else self.third.export_data(),
            'import': None if self._import is None else self._import.export_data(),
            'division': None if self.division is None else Division.export_data(self.division),
            'stage': None if self.stage is None else self.stage.export_data(),
            'currency': None if self.currency is None else self.currency.export_data(),
            'paymentTerm': None if self.paymentTerm is None else self.paymentTerm.export_data(),
            'dependency': None if self.dependency is None else Dependency.export_data(self.dependency),
            'bankAccount': None if self.bankAccount is None else self.bankAccount.export_data(),
            'employee': None if self.employee is None else self.employee.export_data(),
            'cashier': None if self.cashier is None else self.cashier.export_data(),
            'partner': None if self.partner is None else self.partner.export_data(),
            'kit': None if self.kit is None else self.kit.export_data(),
            'provider': None if self.provider is None else self.provider.export_data(),
            'documentDetails': None if self.documentDetails is None
            else [dd.export_data() for dd in self.documentDetails]
        }

    def export_data_source(self):
        """
            Allow export an document header object
            :return:  Document header object in JSon format
            """
        return {
            'documentHeaderId': self.documentHeaderId,
            'providerId': self.providerId,
            'customerId': self.customerId,
            'employeeId': self.employeeId,
            'businessAgentId': self.businessAgentId,
            'documentDate': self.documentDate,
            'documentNumber': self.documentNumber,
            'total': self.total,
            'provider': None if self.provider is None else Provider.export_light(self.provider),
            'customer': None if self.customer is None else Customer.export_light(self.customer),
            'employee': None if self.employee is None else Employee.export_data_light(self.employee),
            'businessAgent': None if self.businessAgent is None else BusinessAgent.export_data_light(self.businessAgent),
            'paymentTerm': None if self.paymentTerm is None else self.paymentTerm.export_data(),
            'source': None if self.source is None else self.source.export_data(),
            'documentDetails': None if self.documentDetails is None
            else [dd.export_data_simple() for dd in self.documentDetails]
        }

    def export_data_documents_affecting(self):
        return {
            'documentHeaderId': self.documentHeaderId,
            'documentNumber': self.documentNumber,
            'creationDate': self.creationDate,
            'documentType': self.documentType.export_data()
        }

    def import_data(self, data):
        """
        Allow create a new document header object from data
        :param data: information by new document header
        :exception: KeyError an error occurs when a key in data not is set
        :return: document header object in JSON format
        """
        try:
            if 'documentHeaderId' in data:
                self.documentHeaderId = data['documentHeaderId']
            if 'financialEntityId' in data:
                self.financialEntityId = data['financialEntityId']
            if 'cashRegisterId' in data:
                self.cashRegisterId = data['cashRegisterId']
            if 'sourceDocumentTypeId' in data:
                self.sourceDocumentTypeId = data['sourceDocumentTypeId']
            if 'documentTypeId' in data:
                self.documentTypeId = data['documentTypeId']
            if 'sourceId' in data:
                self.sourceId = data['sourceId']
            if 'branchId' in data:
                self.branchId = data['branchId']
            if 'destinyBranchId' in data:
                self.destinyBranchId = data['destinyBranchId']
            if 'assetId' in data:
                self.assetId = data['assetId']
            if 'sourceDocumentHeaderId' in data:
                self.sourceDocumentHeaderId = data['sourceDocumentHeaderId']
            if 'interestPUCId' in data:
                self.interestPUCId = data['interestPUCId']
            if 'reteICAPUCId' in data:
                self.reteICAPUCId = data['reteICAPUCId']
            if 'reteIVAPUCId' in data:
                self.reteIVAPUCId = data['reteIVAPUCId']
            if 'insurancePUCId' in data:
                self.insurancePUCId = data['insurancePUCId']
            if 'costCenterId' in data:
                self.costCenterId = data['costCenterId']
            if 'sectionId' in data:
                self.sectionId = data['sectionId']
            if 'payrollBasicId' in data:
                self.payrollBasicId = data['payrollBasicId']
            if 'businessAgentId' in data:
                self.businessAgentId = data['businessAgentId']
            if 'customerId' in data:
                self.customerId = data['customerId']
            if 'productionOrderId' in data:
                self.productionOrderId = data['productionOrderId']
            if 'withholdingTaxPUCId' in data:
                self.withholdingTaxPUCId = data['withholdingTaxPUCId']
            if 'pucId' in data:
                self.pucId = data['pucId']
            if 'ivaPUCId' in data:
                self.ivaPUCId = data['ivaPUCId']
            if 'consumptionTaxPUCId' in data:
                self.consumptionTaxPUCId = data['consumptionTaxPUCId']
            if 'freightPUCId' in data:
                self.freightPUCId = data['freightPUCId']
            if 'withholdingCREEPUCId' in data:
                self.withholdingCREEPUCId = data['withholdingCREEPUCId']
            if 'retentionPUCId' in data:
                self.retentionPUCId = data['retentionPUCId']
            if 'contractId' in data:
                self.contractId = data['contractId']
            if 'payrollEntityId' in data:
                self.payrollEntityId = data['payrollEntityId']
            if 'otherThirdId' in data:
                self.otherThirdId = data['otherThirdId']
            if 'billingResolutionId' in data:
                self.billingResolutionId = data['billingResolutionId']
            if 'sourceWarehouseId' in data:
                self.sourceWarehouseId = data['sourceWarehouseId']
            if 'destinyWarehouseId' in data:
                self.destinyWarehouseId = data['destinyWarehouseId']
            if 'thirdId' in data:
                self.thirdId = data['thirdId']
            if 'importId' in data:
                self.importId = data['importId']
            if 'divisionId' in data:
                self.divisionId = data['divisionId']
            if 'stageId' in data:
                self.stageId = data['stageId']
            if 'currencyId' in data:
                self.currencyId = data['currencyId']
            if 'paymentTermId' in data:
                self.paymentTermId = data['paymentTermId']
            if 'dependencyId' in data:
                self.dependencyId = data['dependencyId']
            if 'bankAccountId' in data:
                self.bankAccountId = data['bankAccountId']
            if 'employeeId' in data:
                self.employeeId = data['employeeId']
            if 'cashierId' in data:
                self.cashierId = data['cashierId']
            if 'partnerId' in data:
                self.partnerId = data['partnerId']
            if 'kitId' in data:
                self.kitId = data['kitId']
            if 'providerId' in data:
                self.providerId = data['providerId']
            if 'documentDate' in data:
                self.documentDate = converters.convert_string_to_date(data['documentDate'])
            if 'dateFrom' in data:
                self.dateFrom = converters.convert_string_to_date(data['dateFrom'])
            if 'dateTo' in data:
                self.dateTo = converters.convert_string_to_date(data['dateTo'])
            if 'initialDate' in data:
                self.initialDate = converters.convert_string_to_date(data['initialDate'])
            if 'finalDate' in data:
                self.finalDate = converters.convert_string_to_date(data['finalDate'])
            if 'creationDate' in data:
                self.creationDate = converters.convert_string_to_date(data['creationDate'])
            if 'updateDate' in data:
                self.updateDate = converters.convert_string_to_date(data['updateDate'])
            if 'bonusDateFrom' in data:
                self.bonusDateFrom = converters.convert_string_to_date(data['bonusDateFrom'])
            if 'vacationDateFrom' in data:
                self.vacationDateFrom = converters.convert_string_to_date(data['vacationDateFrom'])
            if 'auxTimeOne' in data:
                self.auxTimeOne = converters.convert_string_to_date(data['auxTimeOne'])
            if 'auxTimeTwo' in data:
                self.auxTimeTwo = converters.convert_string_to_date(data['auxTimeTwo'])
            if 'firtsContractDate' in data:
                self.firtsContractDate = converters.convert_string_to_date(data['firtsContractDate'])
            if 'overCostTaxBase' in data:
                self.overCostTaxBase = data['overCostTaxBase']
            if 'disccount2Mode' in data:
                self.disccount2Mode = data['disccount2Mode']
            if 'disccount2TaxBase' in data:
                self.disccount2TaxBase = data['disccount2TaxBase']
            if 'addToPayroll' in data:
                self.addToPayroll = data['addToPayroll']
            if 'accounted' in data:
                self.accounted = data['accounted']
            if 'annuled' in data:
                self.annuled = data['annuled']
            if 'freezeBill' in data:
                self.freezeBill = data['freezeBill']
            if 'pettyCash' in data:
                self.pettyCash = data['pettyCash']
            if 'revolvingFund' in data:
                self.revolvingFund = data['revolvingFund']
            if 'importReplaced' in data:
                self.importReplaced = data['importReplaced']
            if 'isConsignment' in data:
                self.isConsignment = data['isConsignment']
            if 'state' in data:
                self.state = data['state']
            if 'retentionMode' in data:
                self.retentionMode = data['retentionMode']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'closingType' in data:
                self.closingType = data['closingType']
            if 'assumedIVA' in data:
                self.assumedIVA = data['assumedIVA']
            if 'isChangeNoted' in data:
                self.isChangeNoted = data['isChangeNoted']
            if 'exchangeRate' in data:
                self.exchangeRate = data['exchangeRate']
            if 'subtotal' in data:
                self.subtotal = data['subtotal']
            if 'balance' in data:
                self.balance = data['balance']
            if 'disccountPercent' in data:
                self.disccountPercent = data['disccountPercent']
            if 'disccount' in data:
                self.disccount = data['disccount']
            if 'insurance' in data:
                self.insurance = data['insurance']
            if 'bonus' in data:
                self.bonus = data['bonus']
            if 'vacation' in data:
                self.vacation = data['vacation']
            if 'percentageCREE' in data:
                self.percentageCREE = data['percentageCREE']
            if 'baseCREE' in data:
                self.baseCREE = data['baseCREE']
            if 'valueCREE' in data:
                self.valueCREE = data['valueCREE']
            if 'inability' in data:
                self.inability = data['inability']
            if 'layoffValue' in data:
                self.layoffValue = data['layoffValue']
            if 'advanceLayoff' in data:
                self.advanceLayoff = data['advanceLayoff']
            if 'sanction' in data:
                self.sanction = data['sanction']
            if 'importationValue' in data:
                self.importationValue = data['importationValue']
            if 'directIVAPercent' in data:
                self.directIVAPercent = data['directIVAPercent']
            if 'productionUnits' in data:
                self.productionUnits = data['productionUnits']
            if 'stageCostTotal' in data:
                self.stageCostTotal = data['stageCostTotal']
            if 'deductibleRF' in data:
                self.deductibleRF = data['deductibleRF']
            if 'fspValue' in data:
                self.fspValue = data['fspValue']
            if 'directIVA' in data:
                self.directIVA = data['directIVA']
            if 'comissionPercent' in data:
                self.comissionPercent = data['comissionPercent']
            if 'comission' in data:
                self.comission = data['comission']
            if 'expenses' in data:
                self.expenses = data['expenses']
            if 'adjustment' in data:
                self.adjustment = data['adjustment']
            if 'overTax' in data:
                self.overTax = data['overTax']
            if 'sodicon' in data:
                self.sodicon = data['sodicon']
            if 'daysVacation' in data:
                self.daysVacation = data['daysVacation']
            if 'baseSalary' in data:
                self.baseSalary = data['baseSalary']
            if 'epsValue' in data:
                self.epsValue = data['epsValue']
            if 'afpValue' in data:
                self.afpValue = data['afpValue']
            if 'cash' in data:
                self.cash = data['cash']
            if 'checks' in data:
                self.checks = data['checks']
            if 'total' in data:
                self.total = data['total']
            if 'payment' in data:
                self.payment = data['payment']
            if 'initialQuota' in data:
                self.initialQuota = data['initialQuota']
            if 'globalTax' in data:
                self.globalTax = data['globalTax']
            if 'retentionBase' in data:
                self.retentionBase = data['retentionBase']
            if 'retentionValue' in data:
                self.retentionValue = data['retentionValue']
            if 'overCost' in data:
                self.overCost = data['overCost']
            if 'disccount2' in data:
                self.disccount2 = data['disccount2']
            if 'disccount2Value' in data:
                self.disccount2Value = data['disccount2Value']
            if 'tipValue' in data:
                self.tipValue = data['tipValue']
            if 'reteICABase' in data:
                self.reteICABase = data['reteICABase']
            if 'reteICAValue' in data:
                self.reteICAValue = data['reteICAValue']
            if 'consumptionTaxPercent' in data:
                self.consumptionTaxPercent = data['consumptionTaxPercent']
            if 'consumptionTaxBase' in data:
                self.consumptionTaxBase = data['consumptionTaxBase']
            if 'consumptionTaxValue' in data:
                self.consumptionTaxValue = data['consumptionTaxValue']
            if 'retentionPercent' in data:
                self.retentionPercent = data['retentionPercent']
            if 'withholdingTaxBase' in data:
                self.withholdingTaxBase = data['withholdingTaxBase']
            if 'withholdingTaxValue' in data:
                self.withholdingTaxValue = data['withholdingTaxValue']
            if 'reteIVAPercent' in data:
                self.reteIVAPercent = data['reteIVAPercent']
            if 'reteIVABase' in data:
                self.reteIVABase = data['reteIVABase']
            if 'reteIVAValue' in data:
                self.reteIVAValue = data['reteIVAValue']
            if 'reteICAPercent' in data:
                self.reteICAPercent = data['reteICAPercent']
            if 'freight' in data:
                self.freight = data['freight']
            if 'interest' in data:
                self.interest = data['interest']
            if 'ivaPercent' in data:
                self.ivaPercent = data['ivaPercent']
            if 'ivaBase' in data:
                self.ivaBase = data['ivaBase']
            if 'ivaValue' in data:
                self.ivaValue = data['ivaValue']
            if 'withholdingTaxPercent' in data:
                self.withholdingTaxPercent = data['withholdingTaxPercent']
            if 'prefix' in data:
                self.prefix = data['prefix']
            if 'documentNumber' in data:
                self.documentNumber = data['documentNumber']
            if 'controlPrefix' in data:
                self.controlPrefix = data['controlPrefix']
            if 'controlNumber' in data:
                self.controlNumber = data['controlNumber']
            if 'orderNumber' in data:
                self.orderNumber = data['orderNumber']
            if 'prefixRequisitionNumber' in data:
                self.prefixRequisitionNumber = data['prefixRequisitionNumber']
            if 'retirement' in data:
                self.retirement = data['retirement']
            if 'auxCharacterOne' in data:
                self.auxCharacterOne = data['auxCharacterOne']
            if 'auxCharacterTwo' in data:
                self.auxCharacterTwo = data['auxCharacterTwo']
            if 'depositNumber' in data:
                self.depositNumber = data['depositNumber']
            if 'dateComeBack' in data:
                self.dateComeBack = data['dateComeBack']
            if 'vacationMoney' in data:
                self.vacationMoney = data['vacationMoney']
            if 'daysMoney' in data:
                self.daysMoney = data['daysMoney']
            if 'leadDocumentTo' in data:
                self.leadDocumentTo = data['leadDocumentTo']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
            if 'typeThirdParty' in data:
                self.typeThirdParty = data['typeThirdParty']
            if 'payrollPaymentType' in data:
                self.payrollPaymentType = data['payrollPaymentType']
            if 'shipCity' in data:
                self.shipCity = data['shipCity']
            if 'shipDepartment' in data:
                self.shipDepartment = data['shipDepartment']
            if 'shipCountry' in data:
                self.shipCountry = data['shipCountry']
            if 'shipZipCode' in data:
                self.shipZipCode = data['shipZipCode']
            if 'shipPhone' in data:
                self.shipPhone = data['shipPhone']
            if 'documentTypeConsign' in data:
                self.documentTypeConsign = data['documentTypeConsign']
            if 'semester' in data:
                self.semester = data['semester']
            if 'month' in data:
                self.month = data['month']
            if 'realSimulated' in data:
                self.realSimulated = data['realSimulated']
            if 'comments' in data:
                self.comments = data['comments']
            if 'shipTo' in data:
                self.shipTo = data['shipTo']
            if 'shipAddress' in data:
                self.shipAddress = data['shipAddress']
            if 'requisitionNumber' in data:
                self.requisitionNumber = data['requisitionNumber']
            if 'workNumber' in data:
                self.workNumber = data['workNumber']
            if 'sourcePrefix' in data:
                self.sourcePrefix = data['sourcePrefix']
            if 'sourceDocument' in data:
                self.sourceDocument = data['sourceDocument']
            if 'periodicityQuota' in data:
                self.periodicityQuota = data['periodicityQuota']
            if 'year' in data:
                self.year = data['year']
            if 'paymentBy' in data:
                self.paymentBy = data['paymentBy']
            if 'printed' in data:
                self.printed = data['printed']
            if 'quotaNumbers' in data:
                self.quotaNumbers = data['quotaNumbers']
            if 'cutNumber' in data:
                self.cutNumber = data['cutNumber']
            if 'payrollType' in data:
                self.payrollType = data['payrollType']
            if 'baseType' in data:
                self.baseType = data['baseType']
            if 'accountsBackward' in data:
                self.accountsBackward = data['accountsBackward']
            if 'typeAccount' in data:
                self.typeAccount = data['typeAccount']
            if 'auxNumberOne' in data:
                self.auxNumberOne = data['auxNumberOne']
            if 'auxNumberTwo' in data:
                self.auxNumberTwo = data['auxNumberTwo']
            if 'termDays' in data:
                self.termDays = data['termDays']
            if 'daysWorked' in data:
                self.daysWorked = data['daysWorked']
            if 'daysLicensed' in data:
                self.daysLicensed = data['daysLicensed']
            if 'daysNetMoney' in data:
                self.daysNetMoney = data['daysNetMoney']
            if 'daysEnjoy' in data:
                self.daysEnjoy = data['daysEnjoy']
            if 'daysPILA' in data:
                self.daysPILA = data['daysPILA']
        except KeyError as e:
            print(e)
        return self

    @staticmethod
    def get_by_seach(**kwargs):
        """
        Allow search a document header object according to features in request params
        :param kwargs: request params to search
        :return: A document header object in JSON format
        """
        short_word = kwargs.get("short_word")
        document_number = kwargs.get("document_number")
        branch_id = kwargs.get("branch_id")
        control_number = kwargs.get("control_number")
        control_prefix = kwargs.get("control_prefix")
        provider_id = kwargs.get("provider_id")
        billing_resolution_id = kwargs.get("billing_resolution_id")
        if short_word and document_number and branch_id:
            document_header = session.query(DocumentHeader).join(DocumentType, DocumentHeader.documentTypeId ==
                                                                 DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word,
                DocumentHeader.documentNumber == document_number,
                DocumentHeader.branchId == branch_id
            )
            # Para ventas
            if billing_resolution_id:
                document_header = document_header.filter(DocumentHeader.billingResolutionId == billing_resolution_id)
            return document_header.first()
        else:
            document_header = session.query(DocumentHeader).filter(
                DocumentHeader.controlPrefix == control_prefix,
                DocumentHeader.controlNumber == control_number,
                DocumentHeader.documentNumber != document_number,
                DocumentHeader.providerId == provider_id if provider_id else False
            ).first()
            return document_header

    @staticmethod
    def get_source_document(**kwargs):
        """
        Allow search a document header object according to features in request params
        :param kwargs: request params to search
        :return: A document header object in JSON format
        """
        try:
            branch_id = kwargs.get('branch_id')
            provider_id = kwargs.get('provider_id')
            source_short_word = kwargs.get('source_short_word')

            query = session.query(DocumentHeader)\
                .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.documentTypeId)
            # .options(load_only('documentHeaderId', 'documentNumber',
            #                                                     'isConsignment', 'documentDate', 'termDays',
            #                                                     'controlPrefix', 'controlNumber', 'total'))

            if provider_id is not None:
                query = query.join(Provider, Provider.providerId == DocumentHeader.providerId)
                query = query.filter(Provider.providerId == provider_id)

            document_headers = query.filter(
                DocumentType.shortWord == source_short_word,
                DocumentHeader.state == 1,
                DocumentHeader.annuled == 0,
                DocumentHeader.branchId == branch_id).all()

            return document_headers

        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_by_customer_document(**kwargs):
        """
        Allow search a document header object according to features in request params
        :param kwargs: request params to search
        :return: A document header object in JSON format
        """
        branch_id = kwargs.get('branch_id')
        customer_id = kwargs.get('customer_id')
        source_short_word = kwargs.get('source_short_word')

        document_headers= session.query(DocumentHeader) \
            .join(Customer, Customer.customerId == DocumentHeader.customerId) \
            .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.sourceId)\
            .filter(Customer.customerId == customer_id)\
            .filter(
                DocumentType.shortWord == source_short_word,
                DocumentHeader.state == 1,
                DocumentHeader.annuled == 0,
                DocumentHeader.branchId == branch_id).all()

        return  document_headers

    @staticmethod
    def get_by_document_number(**kwargs):
        """
        Allow search a document header object according to features in request params
        :param kwargs: request params to search
        :return: A document header object in JSON format
        """
        branch_id = kwargs.get('branch_id')
        customer_id = kwargs.get('customer_id')
        source_short_word = kwargs.get('source_short_word')
        document_number = kwargs.get('document_number')

        document_headers = session.query(DocumentHeader) \
            .join(Customer, Customer.customerId == DocumentHeader.customerId) \
            .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.documentTypeId) \
            .filter(
            DocumentType.shortWord == source_short_word,
            DocumentHeader.annuled == 0,
            DocumentHeader.branchId == branch_id)
        if customer_id:
            document_headers = document_headers.filter(Customer.customerId == customer_id)
        if document_number:
            document_headers = document_headers.filter(DocumentHeader.documentNumber == document_number)

        return document_headers.all()

    @staticmethod
    def get_sourceid_document(**kwargs):
        """
        Allow search a document header object according to features in request params
        :param kwargs: request params to search
        :return: A document header object in JSON format
        """
        branch_id = kwargs.get('branch_id')
        provider_id = kwargs.get('provider_id')
        source_short_word = kwargs.get('source_short_word')

        document_headers= session.query(DocumentHeader) \
            .join(Provider, Provider.providerId == DocumentHeader.providerId) \
            .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.sourceId)\
            .filter(Provider.providerId == provider_id)\
            .filter(
                DocumentType.shortWord == source_short_word,
                DocumentHeader.state == 1,
                DocumentHeader.annuled == 0,
                DocumentHeader.branchId == branch_id).all()

        return  document_headers

    def save(self):
        """
        Allow save a document header object in database
        :exceptions: An error occurs when data or server no is alive
        :return: int -- document header identifier
        """
        try:

            session.add(self)
            session.flush()

            return self.documentHeaderId
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def update(self):
        """
        Allow update a document header object in database
        :exceptions: An error occurs when data or server no is alive
        :return: void
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
    def delete(id):
        """
        Allow delete a document header object in database

        :exceptions: An error occurs when data or server no is alive
        :return: void
        """
        pass

    def cancel(self):
        from .. import AccountingRecord, AccountingRecordNIIF, Serial, SerialDetail
        try:
            self.annuled = True
            self.updateDate = datetime.now()
            accounting_records = AccountingRecord.get_accounting_record_by_document_header_id(self.documentHeaderId)
            if accounting_records:
                [ar.delete() for ar in accounting_records]

            accounting_records_niif = AccountingRecordNIIF.get_accounting_record_by_document_header_id(self.documentHeaderId)
            if accounting_records_niif:
                [ar.delete() for ar in accounting_records_niif]

            if self.documentDetails:
                # Elimina serial details
                for d in self.documentDetails:
                    if d.itemId and d.item.serial:
                        sdetails_delete = session.query(SerialDetail)\
                            .join(Serial, Serial.serialId == SerialDetail.serialId)\
                            .filter(SerialDetail.documentDetailId == d.documentDetailId,
                                    SerialDetail.documentHeaderId == self.documentHeaderId) \
                            .delete(synchronize_session='fetch')

            if self.documentType.shortWord != 'TB' and self.documentType.shortWord != 'TS':
                # Elimina seriales
                serials_delete = session.query(Serial).filter(Serial.documentHeaderId == self.documentHeaderId) \
                    .delete(synchronize_session='fetch')
            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_document_detail(document_detail):

        document_detail.detailPrefix = document_detail.detailPrefix \
            if document_detail.detailPrefix is not None and document_detail.detailPrefix.strip() != '' else None
        document_detail.updateDate = datetime.now()
        # Actualiza los seriales
        if document_detail.item is not None and document_detail.item.serial \
                and document_detail.documentHeader is not None \
                and document_detail.documentHeader.documentType is not None \
                and ('RP~FP~LT~CM~TEP~TP'.split('~') not in document_detail.documentHeader.documentType.shortWord) \
                and not document_detail.documentHeader.annuled:
            for s in document_detail.serials:
                if s.serialId is not None:
                    s.warehouseId = document_detail.detailWarehouseId
                    if document_detail.documentHeader.documentType.shortWord == 'TB' and document_detail.isDeleted:
                        s.warehouseId = document_detail.documentHeader.sourceWarehouseId \
                            if document_detail.documentHeader.sourceWarehouseId is not None \
                            else document_detail.detailWarehouseId
                    s.updateBy = document_detail.updateBy
                    s.updateDate = datetime.now()
                    DocumentHeader.update_serial(s, document_detail.documentHeaderId, document_detail.documentDetailId)

    @staticmethod
    def update_serial(serial, document_header_id, document_detail_id):
        from .. import Serial, SerialDetail
        sd = session.query(SerialDetail)\
            .filter(SerialDetail.serialId == serial.serialId,
                    SerialDetail.documentHeaderId == document_header_id)
        if serial.documentHeaderId is not None and serial.documentheader.documentType is not None and serial.documentheader.documentType.shortWord in 'TS~TB'.split('~'):
            sd = sd.filter(SerialDetail.type == 'E').first()
        else:
            sd = sd.first()
        #if sd is not None:

    @staticmethod
    def get_by_id(id):
        """
        Allow obtain a document header according to identifier

        :param id: identifier by document header to seek
        :exception: An error occurs when server or database is no alive
        :return: a document header objet in JSON format
        """
        try:
            dh = session.query(DocumentHeader).get(id)
            return dh
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def validate_document_header(**kwargs):
        """
        Allow validate a document header according to request params
        :param kwargs: url or uri params
        :exception: An error occurs when server or database is no alive
        :return: identifier of document header found, 1 not fond
        """
        branch_id = kwargs.get('branch_id')
        document_number = kwargs.get('document_number')
        document_number_before = kwargs.get('last_consecutive')
        short_word = kwargs.get('short_word')

        if document_number == '0000000000' or int(document_number_before) < int(document_number):
            return None
        try:
            document_header = session.query(DocumentHeader).join(DocumentType, DocumentHeader.documentTypeId ==
                                                                 DocumentType.documentTypeId).filter(
                DocumentHeader.documentNumber == document_number,
                DocumentHeader.branchId == branch_id,
                DocumentType.shortWord == short_word).first()

            if document_header is not None:
                return document_header
            else:
                return 1
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def search_document(**kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            source_short_word = kwargs.get('source_short_word')
            startDate = kwargs.get('startDate')
            limitDate = kwargs.get('limitDate')
            branch_id = kwargs.get('branch_id')
            document_number = kwargs.get('document_number')
            control_number = kwargs.get('control_number')
            search = kwargs.get('search')
            words = kwargs.get('words')
            filter_by = kwargs.get('filter_by')
            init_total = kwargs.get('init_total')
            end_total = kwargs.get('end_total')
            if filter_by is None:
                init_total = None
                end_total = None

            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == source_short_word).scalar() if source_short_word else None

            third_provider = aliased(ThirdParty)
            third_customer = aliased(ThirdParty)
            third_employee = aliased(ThirdParty)
            third_partner = aliased(ThirdParty)
            third_otherThird = aliased(ThirdParty)
            third_business = aliased(ThirdParty)
            third_financial = aliased(ThirdParty)
            third_payroll = aliased(ThirdParty)

            document_headers = session.query(DocumentHeader) \
                .distinct() \
                .join(Customer, Customer.customerId == DocumentHeader.customerId, isouter=True) \
                .join(Employee, Employee.employeeId == DocumentHeader.employeeId, isouter=True) \
                .join(Provider, Provider.providerId == DocumentHeader.providerId, isouter=True) \
                .join(Partner, Partner.partnerId == DocumentHeader.partnerId, isouter=True) \
                .join(OtherThird, OtherThird.otherThirdId == DocumentHeader.otherThirdId, isouter=True) \
                .join(BusinessAgent, BusinessAgent.businessAgentId == DocumentHeader.businessAgentId, isouter=True) \
                .join(FinancialEntity, FinancialEntity.financialEntityId == DocumentHeader.financialEntityId, isouter=True) \
                .join(PayrollEntity, PayrollEntity.payrollEntityId == DocumentHeader.payrollEntityId, isouter=True) \
                .join(third_provider, Provider.thirdPartyId == third_provider.thirdPartyId, isouter=True) \
                .join(third_customer, Customer.thirdPartyId == third_customer.thirdPartyId, isouter=True) \
                .join(third_employee, Employee.thirdPartyId == third_employee.thirdPartyId, isouter=True) \
                .join(third_partner, Partner.thirdPartyId == third_partner.thirdPartyId, isouter=True) \
                .join(third_otherThird, OtherThird.thirdPartyId == third_otherThird.thirdPartyId, isouter=True) \
                .join(third_business, BusinessAgent.thirdPartyId == third_business.thirdPartyId, isouter=True) \
                .join(third_financial, FinancialEntity.thirdPartyId == third_financial.thirdPartyId, isouter=True) \
                .join(third_payroll, PayrollEntity.thirdPartyId == third_payroll.thirdPartyId, isouter=True) \
                .join(ThirdParty, ThirdParty.thirdPartyId == DocumentHeader.thirdId, isouter=True) \
                .filter(
                    DocumentHeader.sourceId == document_type_id if document_type_id and source_short_word else True,
                    DocumentHeader.branchId == branch_id if branch_id else False,
                    DocumentHeader.documentDate.between(startDate, limitDate) if startDate and limitDate else False,
                    DocumentHeader.documentNumber == document_number if document_number else True,
                    DocumentHeader.controlNumber == control_number if control_number else True,
                    DocumentHeader.total == init_total if filter_by == "Eq"\
                        else DocumentHeader.total >= init_total if filter_by == "Ma"\
                        else DocumentHeader.total < init_total if filter_by == "Me"\
                        else DocumentHeader.total.between(init_total, end_total) if init_total and end_total else False\
                        if filter_by == "Be" else True,
                    or_(*[Provider.name.like('%{0}%'.format(s)) for s in words],
                        *[third_provider.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_provider.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_provider.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_provider.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_provider.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_customer.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_customer.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_customer.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_customer.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_customer.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_employee.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_employee.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_employee.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_employee.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_employee.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_partner.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_partner.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_partner.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_partner.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_partner.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_otherThird.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_otherThird.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_otherThird.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_otherThird.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_otherThird.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_business.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_business.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_business.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_business.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_business.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_financial.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_financial.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_financial.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_financial.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_financial.secondName.like('%{0}%'.format(s)) for s in words],

                        *[third_payroll.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[third_payroll.lastName.like('%{0}%'.format(s)) for s in words],
                        *[third_payroll.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[third_payroll.firstName.like('%{0}%'.format(s)) for s in words],
                        *[third_payroll.secondName.like('%{0}%'.format(s)) for s in words],

                        *[ThirdParty.tradeName.like('%{0}%'.format(s)) for s in words],
                        *[ThirdParty.lastName.like('%{0}%'.format(s)) for s in words],
                        *[ThirdParty.maidenName.like('%{0}%'.format(s)) for s in words],
                        *[ThirdParty.secondName.like('%{0}%'.format(s)) for s in words],
                        *[ThirdParty.firstName.like('%{0}%'.format(s)) for s in words]) if search else True,)\
                .order_by(DocumentHeader.documentNumber.asc())
            return document_headers

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    # TODO: Metodo en construcción
    @staticmethod
    def build_document_save(document_header, document_details, short_word):
        """
        Allow build a document according to params
        :param document_header: DocumentHeader object
        :param document_details: DocumentDetail object
        :param short_word: short word
        :return: document_header_id saved
        """
        try:
            # Obtiene el documenttypeid ya que solo esta recibiendo el shortword
            document_type_id = session.query(DocumentType.documentTypeId).filter(
                DocumentType.shortWord == short_word).first()[0]

            document_header.documentNumber = '000000000'
            document_header.documentTypeId = document_type_id
            document_header.sourceId = document_type_id
            document_header.createdBy = g.user['name']
            document_header.creationDate = datetime.now()
            document_header.updateBy = g.user['name']
            document_header.updateDate = datetime.now()

            # Hace flush al documentheader para obtener el id y utilizarlo al guardar los detalles
            document_header_id = document_header.save()

            # Guarda los detalles del documento
            for dd in document_details:
                dd.documentHeaderId = document_header_id
                dd.detailDocumentTypeId = document_header.documentTypeId
                dd.createdBy = document_header.createdBy
                dd.creationDate = document_header.creationDate
                dd.updateBy = document_header.updateBy
                dd.updateDate = document_header.updateDate

                dd.save()

            # Consulta la tasa de cambio y la guarda si ya hay una en esa fecha
            flag_exchange_rate = session.query(DefaultValue.currencyId).filter(DefaultValue.branchId ==
                                                                               document_header.branchId).first()
            if flag_exchange_rate is not None and flag_exchange_rate[0] != document_header.currencyId:
                exchange_rate = session.query(ExchangeRate.rate).filter(ExchangeRate.currencyId ==
                                                                        document_header.currencyId,
                                                                        ExchangeRate.date ==
                                                                        document_header.documentDate).first()
                if exchange_rate is None:
                    exchange_rate_to_save = ExchangeRate()
                    exchange_rate_to_save.date = document_header.documentDate
                    exchange_rate_to_save.currencyId = document_header.currencyId
                    exchange_rate_to_save.rate = document_header.exchangeRate
                    exchange_rate_to_save.createdBy = g.user['name']
                    exchange_rate_to_save.creationDate = datetime.now()
                    exchange_rate_to_save.updateBy = g.user['name']
                    exchange_rate_to_save.updateDate = datetime.now()

                    session.add(exchange_rate_to_save)
                    session.flush()

            return document_header_id

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    # TODO: Metodo en construcción
    @staticmethod
    def bulid_document_update(id_document_header, document_header, document_details, data):
        """
        Allow build document before to be updated
        :param id_document_header: document_header_id of document
        :param document_header: DocumentHeader object
        :param document_details: DocumentDetail object
        :param data: data JSON
        """
        # Actualiza el documentHeader
        document_header.update()

        # Consulta los detalles del documentheader
        dds = DocumentDetail.get_document_details_by_document_header_id(id_document_header)

        document_detail_list = data['documentDetails']

        # Elimina los detalles que no estan en la nueva lista
        detalles_a_eliminar = [docd for docd in document_header.documentDetails if
                               docd.documentDetailId not in [
                                   du['documentDetailId'] if 'documentDetailId' in du else 0 for du in
                                   data['documentDetails']]]

        [session.delete(de) for de in detalles_a_eliminar]

        # Importacion de los detalles a modificar
        for d in dds:
            detail = [dl for dl in document_detail_list if
                      (dl['documentDetailId'] if 'documentDetailId' in dl else 0) == d.documentDetailId]
            if len(detail) == 1:
                d.import_data(detail[0])
                d.update()

        # Guarda los detalles nuevos
        for d in document_detail_list:
            if 'documentDetailId' not in d:
                new_detail = DocumentDetail()
                new_detail.import_data(d)
                new_detail.documentHeaderId = id_document_header
                new_detail.detailDocumentTypeId = document_header.documentTypeId
                new_detail.save()

    @staticmethod
    def contracts_affecting(contract_found):
        """
        Allow search document affecting
        :param contract_found: document header object
        :return: list of document headers
        """
        try:
            from .. import AccountingRecord
            documents = session.query(DocumentHeader) \
                .filter(DocumentHeader.branchId == contract_found.branchId,
                    DocumentHeader.contractId == contract_found.contractId).all()
                    # TODO preguntar si la legalizacion lleva el mismo puc u otro
                    # DocumentHeader.pucId == contract_found.pucId).all()

            if documents is None:
                return []
            return documents
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def imports_affecting(_import):
        """
        Allow search documents that affect an import
        :param _import: import object
        :return: list of documents
        """
        try:
            documents = session.query(DocumentHeader) \
                .join(DocumentType, DocumentHeader.documentTypeId == DocumentType.documentTypeId) \
                .filter(DocumentHeader.branchId == _import.branchId,
                        DocumentHeader.annuled == 0,
                        DocumentHeader.importId == _import.importId)\
                .order_by(DocumentHeader.creationDate, DocumentHeader.documentNumber).all()
            if documents is None:
                return []
            return documents
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def documents_affecting(document_header, short_word= None):
        """
        Allow search document affecting
        :param document_header: document header object
        :return: list of document headers
        """
        try:
            documents = None
            if not short_word:
                from .. import AccountingRecord
                documents = session.query(DocumentHeader) \
                    .join(AccountingRecord, AccountingRecord.documentHeaderId == DocumentHeader.documentHeaderId,
                          isouter=True) \
                    .distinct() \
                    .filter(AccountingRecord.crossDocumentHeaderId == document_header['documentHeaderId'],
                            AccountingRecord.documentHeaderId != document_header['documentHeaderId']) \
                    .order_by(DocumentHeader.creationDate, DocumentHeader.documentNumber).all()

            elif short_word and (short_word == 'OP' or short_word == 'CZ' or short_word == 'PE'):
                documents = session.query(DocumentHeader) \
                    .filter(DocumentHeader.branchId == document_header['branchId'],
                            DocumentHeader.annuled == 0,
                            DocumentHeader.sourceDocumentHeaderId == document_header['documentHeaderId']) \
                    .order_by(DocumentHeader.creationDate, DocumentHeader.documentNumber).all()
            # Trae los cierres que estan afectando a una factura de importacion
            elif short_word and short_word == 'FM':
                documents = session.query(DocumentHeader) \
                    .join(DocumentType, DocumentHeader.documentTypeId == DocumentType.documentTypeId) \
                    .filter(DocumentHeader.branchId == document_header['branchId'],
                            DocumentHeader.annuled == 0,
                            DocumentType.shortWord == 'CM',
                            DocumentHeader.importId == document_header['importId'],
                            DocumentHeader.documentHeaderId != document_header['documentHeaderId']) \
                    .order_by(DocumentHeader.creationDate, DocumentHeader.documentNumber).all()

            if documents is None:
                return []
            return documents

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def restore_state_of_document(document_header_id):
        """
        Allow update document's state 
        :param document_header_id: document header id
        :return: None
        """
        try:
            sp_quantity = 0
            sp_sum_quantity = 0
            sp_quantity = session.query(func.sum(DocumentDetail.quantity))\
                .filter(DocumentDetail.documentHeaderId == document_header_id)\
                .first()
            sub_query = session.query(DocumentDetail.documentDetailId)\
                .join(DocumentHeader, DocumentDetail.documentHeaderId == DocumentHeader.documentHeaderId)\
                .filter(DocumentDetail.documentHeaderId == document_header_id,
                        DocumentHeader.annuled == 0).subquery()
            sp_sum_quantity = session.query(func.sum(DocumentDetail.quantity))\
                .filter(DocumentDetail.sourceDocumentDetailId.in_(sub_query)).first()

            sp_sum_quantity = sp_sum_quantity or 0
            sp_quantity = sp_quantity or 0

            if sp_sum_quantity >= sp_quantity:
                document = session.query(DocumentHeader).get(document_header_id)
                document.state = 0
                session.commit()
            else:
                document = session.query(DocumentHeader).get(document_header_id)
                document.state = 1
                session.commit()

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)



