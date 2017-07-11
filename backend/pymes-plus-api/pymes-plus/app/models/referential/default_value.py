# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from datetime import datetime
from ... import Base
from flask import jsonify, g
from ... import session
from ...exceptions import InternalServerError
from .default_value_report import DefaultValueReport
from .document_type import DocumentType
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, Table
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship

# FinancialEntitiesBankAccounts = Table(
#     'financialentitiesbankaccounts', Base.metadata,
#     Column('financialEntityId', ForeignKey(u'financialEntities.financialEntityId'), index=True),
#     Column('bankAccountId', ForeignKey(u'bankAccounts.bankAccountId'), index=True),
#     UniqueConstraint('financialEntityId', 'bankAccountId', name='UC_financialEntityId_bankAccountId')
# )


class FinancialEntitiesBankAccounts(Base):
    __tablename__ = "financialentitiesbankaccounts"
    financialEntitiesBankAccountsId = Column(Integer, primary_key=True)
    financialEntityId = Column(Integer, ForeignKey("financialentities.financialEntityId"))
    bankAccountId = Column(Integer, ForeignKey("bankaccounts.bankAccountId"))

    financialEntity = relationship("FinancialEntity", foreign_keys=[financialEntityId])
    bankAccount = relationship("BankAccount", foreign_keys=[bankAccountId])

class DefaultValue(Base):
    """

    """
    __tablename__ = "defaultvalues"

    defaultValueId = Column(Integer, primary_key=True)
    costCenterId = Column(Integer, ForeignKey("costcenters.costCenterId"))
    costCenter = relationship("CostCenter")
    sectionId = Column(Integer, ForeignKey("sections.sectionId"))
    section = relationship("Section")
    branchId = Column(Integer, ForeignKey("branches.branchId"))
    branch = relationship("Branch")
    debitAccountId = Column(Integer, ForeignKey("bankaccounts.bankAccountId"))
    bankAccount = relationship("BankAccount")
    currencyId = Column(Integer, ForeignKey("currencies.currencyId"))
    currency = relationship("Currency")
    divisionId = Column(Integer, ForeignKey("divisions.divisionId"))
    division = relationship("Division")
    dependencyId = Column(Integer, ForeignKey("dependencies.dependencyId"))
    dependency = relationship("Dependency")
    productionWarehouseId = Column(Integer, ForeignKey("warehouses.warehouseId"))
    productionWarehouse = relationship("Warehouse", foreign_keys=[productionWarehouseId])
    sourceWarehouseId = Column(Integer, ForeignKey("warehouses.warehouseId"))
    sourceWarehouse = relationship("Warehouse", foreign_keys=[sourceWarehouseId])
    destinyWarehouseId = Column(Integer, ForeignKey("warehouses.warehouseId"))
    destinyWarehouse = relationship("Warehouse", foreign_keys=[destinyWarehouseId])
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    allowNegativeStock = Column(TINYINT)
    printDescription = Column(TINYINT)
    disccount2TaxBase = Column(TINYINT)
    activateOtherDisccount = Column(TINYINT)
    activateTip = Column(TINYINT)
    posAlwaysCash = Column(TINYINT)
    hideCost = Column(TINYINT)
    provisionMethod = Column(TINYINT)
    isDeleted = Column(TINYINT)
    printPOSComments = Column(TINYINT)
    controlCreditLimit = Column(TINYINT)
    controlPastPortfolio = Column(TINYINT)
    manualUnitValue = Column(TINYINT)
    invoiceText = Column(String(2000))
    posText = Column(String(200))
    commentsGiftVoucher = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    iprfid = Column(String(50))
    quantityDecimals = Column(TINYINT(4))
    valueDecimals = Column(TINYINT(4))
    paymentBy = Column(TINYINT(4), default=2, nullable=False)
    descriptionFrom = Column(TINYINT(4))
    lastDayPay = Column(TINYINT(4))
    alertAfter = Column(TINYINT(4))
    alertBefore = Column(TINYINT(4))
    posRoundValue = Column(SMALLINT(6), default=1, nullable=False)
    autoPrint = Column(TINYINT(6), default=1, nullable=False)

    purchaseCostCenterId = Column(TINYINT(6), default=None, nullable=True)
    purchaseDivisionId = Column(TINYINT(6), default=None, nullable=True)
    purchaseSectionId = Column(TINYINT(6), default=None, nullable=True)
    purchaseDependencyId = Column(TINYINT(6), default=None, nullable=True)

    treasuryCostCenterId = Column(TINYINT(6), default=None, nullable=True)
    treasuryDivisionId = Column(TINYINT(6), default=None, nullable=True)
    treasurySectionId = Column(TINYINT(6), default=None, nullable=True)
    treasuryDependencyId = Column(TINYINT(6), default=None, nullable=True)

    defaultValueReport = relationship("DefaultValueReport",
                                      primaryjoin=defaultValueId == DefaultValueReport.defaultValueId)


    def export_data(self):
        """
        Allow export default-value object
        :return: default value object
        """
        account_names = {"C": "CTA CORRIENTE",
                         "A": "CTA AHORRO"}
        return {
            "defaultValueId": self.defaultValueId,
            "costCenterId": self.costCenterId,
            "costCenter": None if self.costCenter is None or self.costCenterId is None else {
                "costCenterId": self.costCenterId,
                "code": self.costCenter.code,
                "name": self.costCenter.name
            },
            "sectionId": self.sectionId,
            "section": None if self.section is None or self.sectionId is None else {
                "sectionId": self.sectionId,
                "code": self.section.code,
                "name": self.section.name
            },
            "branchId": self.branchId,
            "debitAccountId": self.debitAccountId,
            "bank": None if self.bankAccount is None or self.debitAccountId is None else {
                "bankAccountId": self.bankAccount.bankAccountId,
                "accountType": self.bankAccount.accountType,
                "nameType": account_names.get(self.bankAccount.accountType, "T. CRÉDITO").encode('utf-8'),
                "accountNumber": self.bankAccount.accountNumber,
                "office": self.bankAccount.office
            },
            "currencyId": self.currencyId,
            "currency": None if self.currency is None or self.currencyId is None else {
                "currencyId": self.currency.currencyId,
                "code": self.currency.code,
                "name": self.currency.name,
                "symbol": self.currency.symbol
            },
            "divisionId": self.divisionId,
            "division": None if self.division is None or self.divisionId is None else {
                "divisionId": self.divisionId,
                "code": self.division.code,
                "name": self.division.name
            },
            "dependencyId": self.dependencyId,
            "dependency": None if self.dependency is None or self.dependencyId is None else {
                "dependencyId": self.dependencyId,
                "code": self.dependency.code,
                "name": self.dependency.name
            },
            "productionWarehouseId": self.productionWarehouseId,
            'productionWarehouse': None if self.productionWarehouse is None or self.productionWarehouseId is None else {
                'productionWarehouseId': self.productionWarehouseId,
                'code': self.productionWarehouse.code,
                'name': self.productionWarehouse.name,
                'typeWarehouse': self.productionWarehouse.typeWarehouse
            },
            "sourceWarehouseId": self.sourceWarehouseId,
            'sourceWarehouse': None if self.sourceWarehouse is None or self.sourceWarehouseId is None else {
                'sourceWarehouseId': self.sourceWarehouseId,
                'code': self.sourceWarehouse.code,
                'name': self.sourceWarehouse.name,
                'typeWarehouse': self.sourceWarehouse.typeWarehouse
            },
            "destinyWarehouseId": self.destinyWarehouseId,
            'destinyWarehouse': None if self.destinyWarehouse is None or self.destinyWarehouseId is None else {
                'destinyWarehouseId': self.destinyWarehouseId,
                'code': self.destinyWarehouse.code,
                'name': self.destinyWarehouse.name,
                'typeWarehouse': self.destinyWarehouse.typeWarehouse
            },
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "allowNegativeStock": self.allowNegativeStock,
            "printDescription": self.printDescription,
            "disccount2TaxBase": self.disccount2TaxBase,
            "activateOtherDisccount": self.activateOtherDisccount,
            "activateTip": self.activateTip,
            "posAlwaysCash": self.posAlwaysCash,
            "hideCost": self.hideCost,
            "provisionMethod": self.provisionMethod,
            "isDeleted": self.isDeleted,
            "printPOSComments": self.printPOSComments,
            "controlCreditLimit": self.controlCreditLimit,
            "controlPastPortfolio": self.controlPastPortfolio,
            "manualUnitValue": self.manualUnitValue,
            "invoiceText": self.invoiceText,
            "posText": self.posText,
            "commentsGiftVoucher": self.commentsGiftVoucher,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "iprfid": self.iprfid,
            "quantityDecimals": self.quantityDecimals,
            "valueDecimals": self.valueDecimals,
            "paymentBy": self.paymentBy,
            "descriptionFrom": self.descriptionFrom,
            "lastDayPay": self.lastDayPay,
            "alertAfter": self.alertAfter,
            "alertBefore": self.alertBefore,
            "posRoundValue": self.posRoundValue,
            "purchaseCostCenterId": self.purchaseCostCenterId,
            "autoPrint": self.autoPrint,
            "purchaseSectionId": self.purchaseSectionId,
            "purchaseDivisionId": self.purchaseDivisionId,
            "purchaseDependencyId": self.purchaseDependencyId,
            "treasuryCostCenterId": self.treasuryCostCenterId,
            "treasurySectionId": self.treasurySectionId,
            "treasuryDivisionId": self.treasuryDivisionId,
            "treasuryDependencyId": self.treasuryDependencyId,
        }

    def import_data(self, data):
        """
        Allow create default value fro data information
        :param data: information of default value
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:  default value object
        """

        if "defaultValueId" in data:
            self.defaultValueId = data["defaultValueId"]
        if "costCenterId" in data:
            self.costCenterId = data["costCenterId"]
        if "sectionId" in data:
            self.sectionId = data["sectionId"]
        if "branchId" in data:
            self.branchId = data["branchId"]
        if "debitAccountId" in data:
            self.debitAccountId = data["debitAccountId"]
        if "currencyId" in data:
            self.currencyId = data["currencyId"]
        if "divisionId" in data:
            self.divisionId = data["divisionId"]
        if "dependencyId" in data:
            self.dependencyId = data["dependencyId"]
        if "productionWarehouseId" in data:
            self.productionWarehouseId = data["productionWarehouseId"]
        if "sourceWarehouseId" in data:
            self.sourceWarehouseId = data["sourceWarehouseId"]
        if "destinyWarehouseId" in data:
            self.destinyWarehouseId = data["destinyWarehouseId"]
        if "creationDate" in data:
            self.creationDate = data["creationDate"]
        if "updateDate" in data:
            self.updateDate = data["updateDate"]
        if "allowNegativeStock" in data:
            self.allowNegativeStock = data["allowNegativeStock"]
        if "printDescription" in data:
            self.printDescription = data["printDescription"]
        if "disccount2TaxBase" in data:
            self.disccount2TaxBase = data["disccount2TaxBase"]
        if "activateOtherDisccount" in data:
            self.activateOtherDisccount = data["activateOtherDisccount"]
        if "activateTip" in data:
            self.activateTip = data["activateTip"]
        if "posAlwaysCash" in data:
            self.posAlwaysCash = data["posAlwaysCash"]
        if "hideCost" in data:
            self.hideCost = data["hideCost"]
        if "provisionMethod" in data:
            self.provisionMethod = data["provisionMethod"]
        if "isDeleted" in data:
            self.isDeleted = data["isDeleted"]
        if "printPOSComments" in data:
            self.printPOSComments = data["printPOSComments"]
        if "controlCreditLimit" in data:
            self.controlCreditLimit = data["controlCreditLimit"]
        if "controlPastPortfolio" in data:
            self.controlPastPortfolio = data["controlPastPortfolio"]
        if "manualUnitValue" in data:
            self.manualUnitValue = data["manualUnitValue"]
        if "invoiceText" in data:
            self.invoiceText = data["invoiceText"]
        if "posText" in data:
            self.posText = data["posText"]
        if "commentsGiftVoucher" in data:
            self.commentsGiftVoucher = data["commentsGiftVoucher"]
        if "createdBy" in data:
            self.createdBy = data["createdBy"]
        if "updateBy" in data:
            self.updateBy = data["updateBy"]
        if "iprfid" in data:
            self.iprfid = data["iprfid"]
        if "quantityDecimals" in data:
            self.quantityDecimals = data["quantityDecimals"]
        if "valueDecimals" in data:
            self.valueDecimals = data["valueDecimals"]
        if "paymentBy" in data:
            self.paymentBy = data["paymentBy"]
        if "descriptionFrom" in data:
            self.descriptionFrom = data["descriptionFrom"]
        if "lastDayPay" in data:
            self.lastDayPay = data["lastDayPay"]
        if "alertAfter" in data:
            self.alertAfter = data["alertAfter"]
        if "alertBefore" in data:
            self.alertBefore = data["alertBefore"]
        if "posRoundValue" in data:
            self.posRoundValue = data["posRoundValue"]
        if "purchaseCostCenterId" in data:
            self.purchaseCostCenterId = data['purchaseCostCenterId']
        if "purchaseSectionId" in data:
            self.purchaseSectionId = data['purchaseSectionId']
        if "purchaseDivisionId" in data:
            self.purchaseDivisionId = data['purchaseDivisionId']
        if "purchaseDependencyId" in data:
            self.purchaseDependencyId = data['purchaseDependencyId']
        if "treasuryCostCenterId" in data:
            self.treasuryCostCenterId = data['treasuryCostCenterId']
        if "treasurySectionId" in data:
            self.treasurySectionId = data['treasurySectionId']
        if "treasuryDivisionId" in data:
            self.treasuryDivisionId = data['treasuryDivisionId']
        if "treasuryDependencyId" in data:
            self.treasuryDependencyId = data['treasuryDependencyId']
        if "autoPrint" in data:
            self.autoPrint = data['autoPrint']
        return self

    @staticmethod
    def export_data_decimals(data):
        """
        Allow obtain defult values data in short o simple model}
        :param data: infortamtion of default-value
        :return: default-value object
        """
        return {
            "quantityDecimals": data.quantityDecimals,
            "valueDecimals": data.valueDecimals,
            "branchId": data.branchId
        }

    @staticmethod
    def get_default_values():
        """
        Allow obteain all default values
        :return:
        """
        list_default = jsonify(data=[default.export_data() for default in session.query(DefaultValue).all()])
        return list_default

    @staticmethod
    def get_default_value_by_id(default_value_id):
        """
        Allow obtain default value by id
        :param default_value_id: identifier default value
        :return: return default value
        :return: return default value
        """
        default_value = session.query(DefaultValue).get(default_value_id)
        if default_value is None:
            response = jsonify({'code': 404, 'error': 'Not Found'})
            response.status_code = 404
            return response

        default_value = default_value.export_data()
        return jsonify(default_value)

    @staticmethod
    def get_default_values_by_search(**kwargs):
        """
        Allow search default values according to
        :param kwargs:
        :return:
        """
        try:
            branch_id = kwargs.get("branch_id")
            by_branch = kwargs.get("by_branch")
            to_decimals = kwargs.get("to_decimals")

            default_value = {}
            res = []
            if by_branch:
                default_value = session.query(DefaultValue).filter(DefaultValue.branchId == branch_id).first()

                if default_value is None or default_value == {}:
                    response = jsonify({'code': 404, 'message': 'Not Found'})
                    response.status_code = 404
                    return response

                default_value = default_value.export_data()
                financial_entities = DefaultValue.get_financial_entities_bank_accounts(branch_id)
                if len(financial_entities):
                    res = [DefaultValue.export_data_financial(a) for a in financial_entities]
                else:
                    res = []
                default_value['bankAccountFinancialEntity'] = res

            elif to_decimals:
                default_value = session.query(DefaultValue.quantityDecimals,
                                              DefaultValue.valueDecimals,
                                              DefaultValue.branchId).filter(DefaultValue.branchId == branch_id).first()

                if default_value is None or default_value == {}:
                    response = jsonify({'code': 404, 'message': 'Not Found'})
                    response.status_code = 404
                    return response

                default_value = DefaultValue.export_data_decimals(default_value)

            response = jsonify(default_value)
            return response

        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def post_default_value(data):
        """
        Allow create a new default value
        :param data:
        :return:
        """
        if session.query(DefaultValue).filter(DefaultValue.branchId == data["branchId"]).count() > 0:
            response = jsonify({'code': 400, 'message': 'Ya existen valores por defecto creados.'})
            response.status_code = 400
            return response

        default_value = DefaultValue()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']
        default_value = default_value.import_data(data)

        session.add(default_value)

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        default_value_report = [def_val_rep.export_data() for def_val_rep in
                                session.query(DefaultValueReport)
                                       .filter(DefaultValueReport.defaultValueId.is_(None)).all()]

        for report in default_value_report:
            new_report = DefaultValueReport()
            documentTypeId = session.query(DocumentType.documentTypeId)\
                .filter(DocumentType.shortWord == report["shortWord"]).first()
            new_report.documentTypeId = documentTypeId[0]
            new_report.defaultValueId = default_value.defaultValueId
            new_report.name = report["name"]
            new_report.reportName = report["reportName"]
            new_report.size = report["size"]
            new_report.format = report["format"]
            new_report.selected = report["selected"]
            new_report.isDeleted = report["isDeleted"]
            new_report.shortWord = report["shortWord"]
            new_report.createdBy = g.user['name']
            new_report.updateBy = g.user['name']
            new_report.creationDate = datetime.now()
            new_report.updateDate = datetime.now()

            session.add(new_report)
            try:
                session.flush()
            except Exception as ex:
                session.rollback()
                raise InternalServerError(ex)

        DefaultValue.save_financial_entities_bank_accounts(data, default_value.branchId)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        return jsonify({"defaultValueId": default_value.defaultValueId})


    @staticmethod
    def put_default_value(default_value_id, data):
        """
        Allow update default value according to identifier
        :param default_value_id: identifier by default values to update
        :param data: information to change in defult value
        :return: a default value object
        """
        from .. import Branch, BankAccount

        if default_value_id != data["defaultValueId"]:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        if not default_value_exist(default_value_id):
            response = jsonify({'code': 404, 'message': 'Not found'})
            response.status_code = 404
            return response

        default_value = session.query(DefaultValue).get(default_value_id)

        data["creationDate"] = default_value.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = default_value.createdBy
        data["updateBy"] = g.user['name']
        default_value = default_value.import_data(data)

        session.add(default_value)

        DefaultValue.save_financial_entities_bank_accounts(data, default_value.branchId)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_default_value_by_branch_id(branch_id):
        """
        Allow return a default value by branch id
        :param branch_id: branch id
        :return: default value object
        """
        try:
            default_value = session.query(DefaultValue).filter(DefaultValue.branchId == branch_id).first()
            return default_value
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_financial_entities_bank_accounts(branch_id):
        try:
            from .. import Branch, BankAccount
            bank_financial = session.query(FinancialEntitiesBankAccounts) \
                .join(BankAccount, BankAccount.bankAccountId == FinancialEntitiesBankAccounts.bankAccountId) \
                .join(Branch, Branch.branchId == BankAccount.branchId) \
                .filter(Branch.branchId == branch_id)\
                .all()
            return bank_financial
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def save_financial_entities_bank_accounts(data, branch_id):
        try:
            from .. import Branch, BankAccount
            bank_financial = session.query(FinancialEntitiesBankAccounts) \
                .join(BankAccount, BankAccount.bankAccountId == FinancialEntitiesBankAccounts.bankAccountId) \
                .join(Branch, Branch.branchId == BankAccount.branchId) \
                .filter(Branch.branchId == branch_id).all()
                # .delete(synchronize_session='fetch')
            d = [session.delete(a) for a in bank_financial]
            session.flush()
            if 'bankAccountFinancialEntity' in data:
                for i in data['bankAccountFinancialEntity']:
                    a = FinancialEntitiesBankAccounts()
                    a.financialEntityId = i['financialEntity']['financialEntityId']
                    a.bankAccountId = i['bankAccount']['bankAccountId']
                    session.add(a)
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def export_data_financial(data):
        return {
            'bankAccount': {
                        'bankAccountId': data.bankAccountId,
                        'accountType': data.bankAccount.accountType,
                        'nameType': "CTA CORRIENTE" if data.bankAccount.accountType is "C" else "CTA AHORRO"
                        if data.bankAccount.accountType is "A" else "T. CRÉDITO",
                        'accountNumber': data.bankAccount.accountNumber,
                        'office': data.bankAccount.office,
                    },
            'financialEntity': {
                        'financialEntityId': data.financialEntityId,
                        'completeName': str(data.financialEntity)
                    }
        }


def default_value_exist(default_value_id):
    """
    Allow seek a default value for to the give identifier
    :param default_value_id: identifier by default value
    :return: a default value found
    """
    return session.query(DefaultValue).filter(DefaultValue.defaultValueId == default_value_id).count()