# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
import locale

__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"
__status__ = "develop"


from datetime import datetime
from ... import Base, engine
from flask import g
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, DECIMAL, case
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, load_only, aliased, Load, joinedload
from flask import jsonify
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy import or_, and_, func, not_
from .. import PUC, BankAccount, DocumentHeader, DocumentType, Warehouse, Customer, Branch, AccountingAllThirds, Image, \
    ThirdParty
from ...utils import converters
from ...reports import DocumentAccountingPreview
from sqlalchemy.sql import text


class AccountingRecord(Base):
    """AccountingRecord as a public model class.

    """
    __tablename__ = 'accountingrecords'

    accountingRecordId = Column(Integer, primary_key=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    contractId = Column(ForeignKey(u'contracts.contractId'), index=True)
    payrollConceptId = Column(ForeignKey(u'payrollconcepts.payrollConceptId'), index=True)
    businessAgentId = Column(ForeignKey(u'businessagents.businessAgentId'), index=True)
    productionOrderId = Column(ForeignKey(u'productionorders.productionOrderId'), index=True)
    allThirdId = Column(Integer)
    otherThirdId = Column(ForeignKey(u'otherthirds.otherThirdId'), index=True)
    payrollEntityId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    mainThirdId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    importId = Column(ForeignKey(u'imports.importId'), index=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    measurementUnitId = Column(ForeignKey(u'measurementunits.measurementUnitId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    sizeId = Column(ForeignKey(u'sizes.sizeId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    cashRegisterId = Column(ForeignKey(u'cashregisters.cashRegisterId'), index=True)
    colorId = Column(ForeignKey(u'colors.colorId'), index=True)
    partnerId = Column(ForeignKey(u'partners.partnerId'), index=True)
    pieceId = Column(ForeignKey(u'pieces.pieceId'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    roleEmployeeId = Column(ForeignKey(u'roleemployees.roleEmployeeId'), index=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    cashierId = Column(ForeignKey(u'employees.employeeId'), index=True)
    employeeId = Column(ForeignKey(u'employees.employeeId'), index=True)
    financialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    documentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    sourceDocumentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    crossDocumentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    assetId = Column(ForeignKey(u'assets.assetId'), index=True)
    accountingDate = Column(DateTime)
    dueDate = Column(DateTime)
    # creationDate = Column(DateTime, default=datetime.now())
    # updateDate = Column(DateTime, default=datetime.now())
    # isDeleted = Column(Integer, default=0)
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
    # createdBy = Column(String(50))
    # updateBy = Column(String(50))
    accountNumber = Column(String(50))
    bankCode = Column(String(3))
    quoteNumber = Column(TINYINT)
    allThirdType = Column(String(2))
    asset = relationship(u'Asset')
    bankAccount = relationship(u'BankAccount')
    branch = relationship(u'Branch')
    businessAgent = relationship(u'BusinessAgent')
    cashRegister = relationship(u'CashRegister')
    cashier = relationship(u'Employee', primaryjoin='AccountingRecord.cashierId == Employee.employeeId')
    color = relationship(u'Color')
    contract = relationship(u'Contract')
    costCenter = relationship(u'CostCenter')
    crossDocumentHeader = relationship(u'DocumentHeader', primaryjoin='AccountingRecord.crossDocumentHeaderId == DocumentHeader.documentHeaderId')
    customer = relationship(u'Customer')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    documentHeader = relationship(u'DocumentHeader', primaryjoin='AccountingRecord.documentHeaderId == DocumentHeader.documentHeaderId')
    documentType = relationship(u'DocumentType', primaryjoin='AccountingRecord.documentTypeId == DocumentType.documentTypeId')
    employee = relationship(u'Employee', primaryjoin='AccountingRecord.employeeId == Employee.employeeId')
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
    sourceDocumentType = relationship(u'DocumentType', primaryjoin='AccountingRecord.sourceDocumentTypeId == DocumentType.documentTypeId')
    stage = relationship(u'Stage')
    warehouse = relationship(u'Warehouse')

    def export_data(self):
        """
            Allow export an accounting record object
            :return:  Document header object in JSon format
        """
        return {
            'accountingRecordId': self.accountingRecordId,
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
            # 'creationDate': self.creationDate,
            # 'updateDate': self.updateDate,
            # 'isDeleted': self.isDeleted,
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
            # 'createdBy': self.createdBy,
            # 'updateBy': self.updateBy,
            'accountNumber': self.accountNumber,
            'bankCode': self.bankCode,
            'quoteNumber': self.quoteNumber,
        }

    def export_data_lot(self):
        """
            Allow export lot object
            :return: lot dict JSON
        """
        return {
            'lot': self.lot,
            'dueDate': self.dueDate
        }

    def import_data(self, data):
        """
            Allow create a new accounting record object from data
            :param data: information by new accounting record
            :exception: KeyError an error occurs when a key in data not is set
            :return: accounting record object in JSON format
        """
        try:
            if 'accountingRecordId' in data:
                self.accountingRecordId = data['accountingRecordId']
            if 'customerId' in data:
                self.customerId = data['customerId']
            if 'contractId' in data:
                self.contractId = data['contractId']
            if 'payrollConceptId' in data:
                self.payrollConceptId = data['payrollConceptId']
            if 'businessAgentId' in data:
                self.businessAgentId = data['businessAgentId']
            if 'productionOrderId' in data:
                self.productionOrderId = data['productionOrderId']
            if 'allThirdId' in data:
                self.allThirdId = data['allThirdId']
            if 'otherThirdId' in data:
                self.otherThirdId = data['otherThirdId']
            if 'payrollEntityId' in data:
                self.payrollEntityId = data['payrollEntityId']
            if 'dependencyId' in data:
                self.dependencyId = data['dependencyId']
            if 'warehouseId' in data:
                self.warehouseId = data['warehouseId']
            if 'mainThirdId' in data:
                self.mainThirdId = data['mainThirdId']
            if 'pucId' in data:
                self.pucId = data['pucId']
            if 'importId' in data:
                self.importId = data['importId']
            if 'providerId' in data:
                self.providerId = data['providerId']
            if 'measurementUnitId' in data:
                self.measurementUnitId = data['measurementUnitId']
            if 'stageId' in data:
                self.stageId = data['stageId']
            if 'sizeId' in data:
                self.sizeId = data['sizeId']
            if 'divisionId' in data:
                self.divisionId = data['divisionId']
            if 'cashRegisterId' in data:
                self.cashRegisterId = data['cashRegisterId']
            if 'colorId' in data:
                self.colorId = data['colorId']
            if 'partnerId' in data:
                self.partnerId = data['partnerId']
            if 'pieceId' in data:
                self.pieceId = data['pieceId']
            if 'itemId' in data:
                self.itemId = data['itemId']
            if 'roleEmployeeId' in data:
                self.roleEmployeeId = data['roleEmployeeId']
            if 'bankAccountId' in data:
                self.bankAccountId = data['bankAccountId']
            if 'cashierId' in data:
                self.cashierId = data['cashierId']
            if 'employeeId' in data:
                self.employeeId = data['employeeId']
            if 'financialEntityId' in data:
                self.financialEntityId = data['financialEntityId']
            if 'documentTypeId' in data:
                self.documentTypeId = data['documentTypeId']
            if 'sourceDocumentTypeId' in data:
                self.sourceDocumentTypeId = data['sourceDocumentTypeId']
            if 'branchId' in data:
                self.branchId = data['branchId']
            if 'sectionId' in data:
                self.sectionId = data['sectionId']
            if 'costCenterId' in data:
                self.costCenterId = data['costCenterId']
            if 'documentHeaderId' in data:
                self.documentHeaderId = data['documentHeaderId']
            if 'crossDocumentHeaderId' in data:
                self.crossDocumentHeaderId = data['crossDocumentHeaderId']
            if 'assetId' in data:
                self.assetId = data['assetId']
            if 'accountingDate' in data:
                self.accountingDate = converters.convert_string_to_date(data['accountingDate'])
            if 'dueDate' in data:
                self.dueDate = converters.convert_string_to_date(data['dueDate'])
            # if 'creationDate' in data:
            #     self.creationDate = data['creationDate']
            # if 'updateDate' in data:
            #     self.updateDate = data['updateDate']
            # if 'isDeleted' in data:
            #     self.isDeleted = data['isDeleted']
            if 'transfered' in data:
                self.transfered = data['transfered']
            if 'ivaToCost' in data:
                self.ivaToCost = data['ivaToCost']
            if 'niif' in data:
                self.niif = data['niif']
            if 'consumptionToCost' in data:
                self.consumptionToCost = data['consumptionToCost']
            if 'apportionment' in data:
                self.apportionment = data['apportionment']
            if 'foreignCurrency' in data:
                self.foreignCurrency = data['foreignCurrency']
            if 'quantity' in data:
                self.quantity = data['quantity']
            if 'simulatedQuantity' in data:
                self.simulatedQuantity = data['simulatedQuantity']
            if 'units' in data:
                self.units = data['units']
            if 'balance' in data:
                self.balance = data['balance']
            if 'baseValue' in data:
                self.baseValue = data['baseValue']
            if 'percentage' in data:
                self.percentage = data['percentage']
            if 'debit' in data:
                self.debit = data['debit']
            if 'simulatedDebit' in data:
                self.simulatedDebit = data['simulatedDebit']
            if 'credit' in data:
                self.credit = data['credit']
            if 'simulatedCredit' in data:
                self.simulatedCredit = data['simulatedCredit']
            if 'documentPrefix' in data:
                self.documentPrefix = data['documentPrefix']
            if 'documentNumber' in data:
                self.documentNumber = data['documentNumber']
            if 'crossPrefix' in data:
                self.crossPrefix = data['crossPrefix']
            if 'crossDocument' in data:
                self.crossDocument = data['crossDocument']
            if 'lot' in data:
                self.lot = data['lot']
            if 'sourcePrefix' in data:
                self.sourcePrefix = data['sourcePrefix']
            if 'bankName' in data:
                self.bankName = data['bankName']
            if 'cardNumber' in data:
                self.cardNumber = data['cardNumber']
            if 'sign' in data:
                self.sign = data['sign']
            if 'sourceDocument' in data:
                self.sourceDocument = data['sourceDocument']
            if 'comments' in data:
                self.comments = data['comments']
            # if 'createdBy' in data:
            #     self.createdBy = data['createdBy']
            # if 'updateBy' in data:
            #     self.updateBy = data['updateBy']
            if 'accountNumber' in data:
                self.accountNumber = data['accountNumber']
            if 'bankCode' in data:
                self.bankCode = data['bankCode']
            if 'quoteNumber' in data:
                self.quoteNumber = data['quoteNumber']
        except KeyError as e:
            raise ValidationError("Invalid accounting record: missing " + e.args[0])
        except Exception as e:
            raise InternalServerError(e)

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
    def validate_debits_credits(data):
        pass

    @staticmethod
    def get_lot_by_item_id(lot, item_id):
        """
        Allow search lot by item_id and lot string
        :param lot: lot string
        :param item_id: item id
        :return: Accounting record object
        """
        try:
            lot = session.query(AccountingRecord)\
                .filter(AccountingRecord.itemId == item_id, AccountingRecord.lot == lot).first()
            return lot
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def seach_balance(**kwargs):
        """
        Allow acquire
        :return:
        """
        by_param = kwargs.get('by_param')
        branch_id = kwargs.get('branch_id')
        bank_account = kwargs.get('bank_account')
        puc_id = kwargs.get('puc_id')
        cross_document = kwargs.get('cross_document')
        document_number = kwargs.get('document_number')
        import_id = kwargs.get('import_id')
        date = kwargs.get('date') if kwargs.get('date') else datetime.now()

        if by_param:
            if by_param == 'cash':
                balance = session.query(func.sum(AccountingRecord.debit -AccountingRecord.credit))\
                    .join(Branch, Branch.branchId == AccountingRecord.branchId)\
                    .join(PUC, and_(PUC.pucId == AccountingRecord.pucId,  PUC.cash == 1))\
                    .filter(AccountingRecord.accountingDate <= date, AccountingRecord.branchId == branch_id, AccountingRecord.cashRegisterId == None)\
                    .scalar()
                if not balance:
                    balance =0
                return jsonify(balance=balance)
            if by_param == 'bankaccount':
                balance = session.query(func.sum(AccountingRecord.debit -AccountingRecord.credit))\
                    .join(Branch, and_(Branch.branchId == AccountingRecord.branchId, Branch.branchId == branch_id))\
                    .join(BankAccount, and_(BankAccount.bankAccountId == AccountingRecord.bankAccountId,  BankAccount.bankAccountId == bank_account))\
                    .join(PUC, PUC.pucId == BankAccount.pucId)\
                    .filter(AccountingRecord.accountingDate <= date)\
                    .scalar()
                if not balance:
                    balance =0
                return jsonify(balance= balance)
            if by_param == 'import_balance':
                # Trae el saldo de la importacion y la fecha de la ultima factura de importacion
                balance = session.query(func.sum(AccountingRecord.debit - AccountingRecord.credit)) \
                    .join(Branch, Branch.branchId == AccountingRecord.branchId) \
                    .join(PUC, and_(PUC.pucId == AccountingRecord.pucId, PUC.pucId == puc_id)) \
                    .filter(AccountingRecord.accountingDate <= date, AccountingRecord.branchId == branch_id,
                            AccountingRecord.importId == import_id) \
                    .scalar()

                last_document = session.query(DocumentHeader.documentDate, DocumentHeader.documentNumber)\
                    .join(DocumentType, DocumentType.documentTypeId == DocumentHeader.documentTypeId)\
                    .filter(DocumentType.shortWord == 'FM',
                            DocumentHeader.importId == import_id,
                            DocumentHeader.annuled == 0)\
                    .order_by(DocumentHeader.documentDate).first()
                if not balance:
                    balance = 0
                return jsonify({'balance': balance, 'lastDate': last_document.documentDate,
                                'documentNumber': last_document.documentNumber})

            if by_param == 'giftvoucher_balance':
                # Trae el saldo de
                balance = session.query(func.sum(AccountingRecord.credit - AccountingRecord.debit)) \
                    .join(Branch, Branch.branchId == AccountingRecord.branchId) \
                    .join(PUC, and_(PUC.pucId == AccountingRecord.pucId, PUC.giftVoucher == 1)) \
                    .filter(AccountingRecord.crossDocument == cross_document,
                            AccountingRecord.branchId == branch_id) \
                    .scalar()

                if not balance:
                    balance = 0
                return jsonify({'balance': balance})

            if by_param == 'changenote_balance':
                # Trae el saldo de
                balance = session.query(func.sum(AccountingRecord.debit - AccountingRecord.credit)) \
                    .join(Branch, Branch.branchId == AccountingRecord.branchId) \
                    .join(PUC, and_(PUC.pucId == AccountingRecord.pucId, PUC.changeNote == 1)) \
                    .filter(AccountingRecord.documentNumber == document_number,
                            AccountingRecord.branchId == branch_id) \
                    .scalar()

                if not balance:
                    balance = 0
                return jsonify({'balance': balance})

    @staticmethod
    def get_accounting_record_preview(document_header_id):
        """
        Search accounting records according document_header_id (this is for accounting preview a.k.a balance a cero)
        :param document_header_id: document header id
        :return: accounting report
        """
        try:
            ar = aliased(AccountingRecord)
            wr = aliased(Warehouse)
            # TODO: Agregar cuando este creada la vista sql
            aat = aliased(AccountingAllThirds)
            p = aliased(PUC)
            # docD = aliased(DocumentDetail)
            # ddocD = aliased(DocumentDetail)
            # q = session.query(func.sum(ddocD.value).label('sum_iva'),
            #                   ddocD.iva,
            #                   func.row_number().over(order_by=ddocD.iva)) \
            #     .filter(ddocD.documentHeaderId == document_header_id) \
            #     .group_by(ddocD.iva) \
            #     .subquery()

            # TODO: Agregar cuando este creada la vista sql
            # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)
            # full_name_prov = Bundle('Full_Name_Prov', t.name, t.branchname)

            # TODO: Agregar validacion para libro 2 que es de niif
            previw_data = session.query(ar)


            # TODO: Cargar la imagen de la compañia
            # TODO: Cargar la vista de thirdcompany
            # TODO: Implementar groupby

            preview_data = previw_data.options(
                joinedload(ar.documentHeader, innerjoin=True).load_only('documentNumber'),
                joinedload(ar.branch, innerjoin=True).load_only('name', 'address1', 'phone1', 'phone2', 'phone3', 'fax',
                                                                'icaActivity1', 'icaRate1', 'icaActivity2', 'icaRate2',
                                                                'icaActivity3', 'icaRate3', 'icaActivity4', 'icaRate4',
                                                                'icaActivity5', 'icaRate5'),
                joinedload(ar.documentType, innerjoin=True).load_only('name', 'shortWord', 'documentTypeId'),
            ).add_columns(aat.allThirdId, aat.allThirdType, aat.name, aat.identificationNumber,aat.identificationDV)\
                .join(aat, and_(aat.allThirdId == ar.allThirdId, aat.allThirdType == ar.allThirdType), isouter=True)\
                .join(p, and_(p.pucId == ar.pucId), isouter=True)\
                .join(wr, and_(ar.warehouseId == wr.warehouseId, wr.branchId == ar.branchId), isouter=True)\
                .filter(ar.documentHeaderId == document_header_id, and_(or_(ar.debit > 0, ar.credit > 0), not_(and_(ar.debit > 0, ar.credit > 0))))\
                .order_by(p.pucClass,p.pucSubClass,p.account,ar.crossPrefix, ar.crossDocument, ar.dueDate,ar.pucId).all()

            first_data = preview_data[0][0]
            img = None if not first_data.branch.company.imageId \
                else session.query(Image).get(first_data.branch.company.imageId)

            header = first_data

            # locale.setlocale(locale.LC_ALL, 'es_CO')
            formatted_data = {
                'company_name': header.branch.company.name,
                'branch_name': header.branch.name,
                'branch_id': header.branch.branchId,
                'nit': '{0}-{1}'.format('{:,}'.format(int(header.branch.company.identificationNumber)),
                                        header.branch.company.identificationDV),
                'image': img,
                'document_type': header.documentType.name,
                'short_word': header.documentType.shortWord,
                'document_prefix': header.documentPrefix,
                'document_number': header.documentHeader.documentNumber,
                'accounting_date': header.accountingDate,
                'details': preview_data,
            }

            return DocumentAccountingPreview.make_preview_pdf(formatted_data)

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)
        # try:
        #     accounting_records = session.query(AccountingRecord)\
        #         .filter(AccountingRecord.documentHeaderId == document_header_id).all()
        #
        #     preview_data = {
        #         'libro': accounting_records.libro
        #     }
        #     """
        #     SELECT
        #         ar.Libro,
        #         ar.AccountingDate,
        #         ar.DocumentPrefix,
        #         dh.DocumentNumber,
        #         ISNULL(ar.CrossPrefix,'') AS CrossPrefix,
        #         ISNULL(ar.CrossDocument,'') AS CrossDocument,
        #         ar.Lot,
        #         ar.DueDate,
        #         ar.Quantity,
        #         ar.Debit,
        #         ar.Credit,
        #         referential.Companies.Code,
        #         referential.Companies.Name,
        #         referential.Companies.IdentificationNumber,
        #         referential.Companies.IdentificationDV,
        #         referential.Branches.Code AS BranchCode,
        #         referential.Branches.Name AS BranchName,
        #         referential.DefaultValues.QuantityDecimals,
        #         referential.DocumentTypes.ShortWord,
        #         referential.PUC.PUCClass,
        #         referential.PUC.PUCSubClass,
        #         referential.PUC.Account,
        #         referential.PUC.SubAccount,
        #         referential.PUC.Auxiliary1,
        #         referential.PUC.Auxiliary2,
        #         referential.PUC.Name AS PUCName,
        #         accounting.AllThirds.Name AS AllThirdName,
        #         accounting.AllThirds.IdentificationNumber AS Nit,
        #         accounting.AllThirds.IdentificationDV AS DV,
        #         accounting.AllThirds.AllThirdId,
        #         referential.Warehouses.Code AS WarehouseCode,
        #         referential.DocumentTypes.Name AS DocumentTypeName
        #     FROM  (
        #         select
        #                 ar1.*,
        #                 '1' as Libro,
        #                 CDate  from accounting.AccountingRecords ar1,
        #                 referential.GeneralParameters
        #
        #                 where DocumentHeaderId= @DocumentHeaderId
        #
        #         union all
        #         select
        #                 ar1.*,
        #                 '2' as Libro,
        #                 CDate from accounting.AccountingRecordsNIIF ar1,
        #                 referential.GeneralParameters
        #         where
        #                 DocumentHeaderId= @DocumentHeaderId
        #                 and
        #                 CDate=1 and Year(ar1.AccountingDate) > '2014'
        #
        #         union all
        #
        #         select
        #                 ar1.*,
        #                 '2' as Libro,
        #                 CDate from accounting.AccountingRecords ar1,
        #                 referential.GeneralParameters
        #         where
        #                 DocumentHeaderId= @DocumentHeaderId
        #                 and
        #                 ( NIIF =1 or NIIF IS NULL ) and CDate=1
        #                 and
        #                 Year(ar1.AccountingDate) > '2014') ar
        #
        #     INNER JOIN referential.Branches ON ar.BranchId = referential.Branches.BranchId
        #
        #     INNER JOIN referential.Companies ON referential.Branches.CompanyId = referential.Companies.CompanyId
        #
        #     INNER JOIN referential.DefaultValues ON referential.Branches.BranchId  = referential.DefaultValues.BranchId
        #
        #     INNER JOIN referential.PUC ON ar.PUCId = referential.PUC.PUCId
        #
        #     INNER JOIN referential.DocumentTypes ON ar.DocumentTypeId = referential.DocumentTypes.DocumentTypeId
        #
        #     LEFT OUTER JOIN referential.Warehouses ON ar.WarehouseId = referential.Warehouses.WarehouseId
        #     AND referential.Branches.BranchId = referential.Warehouses.BranchId
        #
        #     left outer JOIN accounting.AllThirds ON accounting.AllThirds.AllThirdId = ar.AllThirdId
        #
        #     inner join accounting.DocumentHeaders dh ON ar.DocumentHeaderId = dh.DocumentHeaderId
        #
        #     WHERE ar.DocumentHeaderId =@DocumentHeaderId  and ar.Libro like @Libro
        #
        #     ORDER BY
        #                 ar.Libro,
        #                 referential.Companies.Code,
        #                 BranchCode,
        #                 referential.PUC.PUCClass,
        #                 referential.PUC.PUCSubClass,
        #                 referential.PUC.Account,
        #                 referential.PUC.SubAccount,
        #                 referential.PUC.Auxiliary1,
        #                 referential.PUC.Auxiliary2,
        #                 AllThirdName,
        #                 accounting.AllThirds.AllThirdId,
        #                 WarehouseCode,
        #                 ar.AccountingDate
        #     """
        # except Exception as e:
        #     session.rollback()
        #     raise InternalServerError(e)

    @staticmethod
    def get_customer_status(customer_id, branch_id, document_date):
        """
        Allow to search customer credit available
        :param customer_id: customer id
        :param branch_id: branch id
        :param document_date: document date
        :return: dict object with 
        """
        # Metodo para buscar la cartera y estado del cliente
        try:
            # Busca el cupo de credito del cliente
            customer_credit = session.query(Customer.creditCapacity).filter(Customer.customerId == customer_id).first()

            document_date = converters.convert_string_to_date(document_date)

            # Query general para buscar los registros contables y calcular la cartera del cliente
            ar = session.query(
                func.sum(func.ifnull(AccountingRecord.debit, 0)) - func.sum(func.ifnull(AccountingRecord.credit, 0)))\
                .join(PUC, and_(AccountingRecord.pucId == PUC.pucId,
                                or_(PUC.customerAccountsReceivable == 1, PUC.loansPrivateConcepts == 1)))\
                .filter(AccountingRecord.crossDocumentHeaderId.isnot(None),
                        AccountingRecord.customerId == customer_id,
                        AccountingRecord.branchId == branch_id,
                        AccountingRecord.accountingDate <= document_date)

            # Filtro para cartera vencida
            query_due = ar.filter(func.ifnull(AccountingRecord.dueDate, AccountingRecord.accountingDate) < document_date)

            # Filtro para cartera Vigente
            query_valid = ar.filter(func.ifnull(AccountingRecord.dueDate, AccountingRecord.accountingDate) >= document_date)

            # Ejecuta queries
            due = query_due.all()
            valid = query_valid.all()

            due = due[0][0] if due[0][0] is not None else 0
            valid = valid[0][0] if valid[0][0] is not None else 0

            return {'customerCredit': customer_credit[0],
                    'valid': valid,
                    'due': due,
                    'available': customer_credit[0] - valid - due
                    }

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_accounting_record_by_document_header_id(document_header_id):
        """
        Allow get accounting records by document header id
        :param document_header_id: document header id
        :return: accounting records object
        """
        try:
            accounting_records = session.query(AccountingRecord) \
                .filter(AccountingRecord.documentHeaderId == document_header_id).all()
            return accounting_records
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_accounting_detail_inversions(puc_id, accounting_date, branch_id):
        # accounting_alias = aliased(AccountingRecord)
        puc_account = session.query(PUC).get(puc_id)
        puc_str = "{0}{1}{2}".format(puc_account.pucClass, puc_account.pucSubClass, puc_account.account)
        xpr = case([(AccountingRecord.debit != 0, 1)], else_=-1)
        query = session.query(AccountingRecord.branchId, AccountingRecord.mainThirdId, AccountingRecord.pucId,
                              AccountingRecord.crossPrefix, AccountingRecord.crossDocument,
                              func.sum(*[AccountingRecord.quantity * xpr]).label("balance"),
                              func.sum(AccountingRecord.debit).label("debit"), func.sum(AccountingRecord.credit).label("credit")) \
            .join(PUC, AccountingRecord.pucId == PUC.pucId) \
            .filter(func.date(AccountingRecord.accountingDate) <= accounting_date,
                    PUC.billingConceptsInvestment == 1,
                    AccountingRecord.branchId == branch_id,
                    PUC.pucClass+PUC.pucSubClass+PUC.account == puc_str) \
            .group_by(AccountingRecord.branchId, AccountingRecord.mainThirdId, AccountingRecord.pucId,
                      AccountingRecord.crossPrefix, AccountingRecord.crossDocument).subquery('ar')

        outer_query = session.query(*[query.c.branchId, query.c.mainThirdId, query.c.pucId, query.c.crossPrefix, query.c.crossDocument, query.c.balance, query.c.debit, query.c.credit])

        subquery = session.query(*[func.sum(AccountingRecord.debit) / case([(func.sum(AccountingRecord.quantity) == 0, 1)], else_=func.sum(AccountingRecord.quantity))]) \
            .filter(AccountingRecord.pucId == query.c.pucId,
                    AccountingRecord.branchId == query.c.branchId,
                    func.ifnull(AccountingRecord.mainThirdId, 0) == func.ifnull(query.c.mainThirdId, 0),
                    func.ifnull(AccountingRecord.crossPrefix, '') == func.ifnull(query.c.crossPrefix, ''),
                    func.ifnull(AccountingRecord.crossDocument, '') == func.ifnull(query.c.crossDocument, ''),
                    AccountingRecord.debit != 0) \
            .correlate(query)

        query = outer_query.add_column(func.ifnull(subquery.as_scalar(), 0).label("balance"))

        result = query.all()

        response = []
        for a in result:
            # Si el balance es mayor a cero
            if a[5] is not None and a[5] > 0:
                main_third = session.query(ThirdParty).get(a[1])
                appended = {
                    'branchId': a[0],
                    'thirdId': a[1],
                    'name': ThirdParty.string_name(main_third),
                    'pucId': a[2],
                    'crossPrefix': a[3],
                    'crossDocument': a[4],
                    'balance': a[5],
                    'debit': a[6],
                    'credit': a[7],
                    'baseValue': a[8]
                }
                response.append(appended)
        return response
