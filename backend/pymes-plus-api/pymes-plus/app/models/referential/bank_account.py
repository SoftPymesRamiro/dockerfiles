# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"

from datetime import datetime
from ... import Base
from flask import jsonify, g
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_, func
from ...utils import converters

class BankAccount(Base):
    """
    """
    __tablename__ = "bankaccounts"

    bankAccountId = Column(Integer, primary_key=True)
    bankId = Column(Integer, ForeignKey(u'financialentities.financialEntityId'))
    cardTypeId = Column(Integer, ForeignKey(u'financialentities.financialEntityId'))
    branchId = Column(Integer)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    openingDate = Column(DateTime, default=datetime.now())
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    expirationDate = Column(DateTime, default=datetime.now())
    bankingTax = Column(TINYINT)
    isDeleted = Column(TINYINT)
    accountNumber = Column(String(50))
    office = Column(String(100))
    owner = Column(String(100))
    accountType = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    creditCapacity = Column(Integer)
    # overdraft = Column(Integer)

    financialEntity = relationship('FinancialEntity', foreign_keys=[bankId])
    financialEntity1 = relationship('FinancialEntity', foreign_keys=[cardTypeId])
    # branch = relationship('Branch')
    puc = relationship(u'PUC')

    def export_data(self):
        """
        :return all bank data
        """
        return {
            "bankAccountId": self.bankAccountId,
            "branchId": self.branchId,
            "accountNumber": self.accountNumber,
            "bank": None if self.financialEntity is None else{
                'financialEntityId': self.financialEntity.financialEntityId,
                'name': '{0} {1} {2} {3} - {4}'.format(
                    '' if self.financialEntity.thirdParty.tradeName is None
                    else self.financialEntity.thirdParty.tradeName,
                    '' if self.financialEntity.thirdParty.lastName is None
                    else self.financialEntity.thirdParty.lastName,
                    '' if self.financialEntity.thirdParty.maidenName is None
                    else self.financialEntity.thirdParty.maidenName,
                    '' if self.financialEntity.thirdParty.firstName is None
                    else self.financialEntity.thirdParty.firstName,
                    self.financialEntity.name
                    ),
            },
            "officeComplete": '{0} - {1}'.format(self.office, self.accountNumber),
            "bankId": self.bankId,
            "office": self.office,
            "owner": self.owner,
            "pucId": self.pucId,
            "puc": None if self.pucId is None or self.puc is None else{
                "pucId": self.puc.pucId,
                "account": '{0}{1}{2}{3}{4}'.format(self.puc.pucClass,
                                                    self.puc.pucSubClass,
                                                    self.puc.account,
                                                    self.puc.subAccount,
                                                    self.puc.auxiliary1),
                "name": self.puc.name,
            },
            "cardType": None if self.financialEntity1 is None else{
                'financialEntityId': self.financialEntity1.financialEntityId,
                'name': '{0} {1} {2} {3}'.format(
                    '' if self.financialEntity1.thirdParty.tradeName is None
                    else self.financialEntity1.thirdParty.tradeName,
                    '' if self.financialEntity1.thirdParty.lastName is None
                    else self.financialEntity1.thirdParty.lastName,
                    '' if self.financialEntity1.thirdParty.maidenName is None
                    else self.financialEntity1.thirdParty.maidenName,
                    '' if self.financialEntity1.thirdParty.firstName is None
                    else self.financialEntity1.thirdParty.firstName,
                    ),
            },
            "accountType": self.accountType,
            "openingDate": self.openingDate,
            "bankingTax": self.bankingTax,
            "createdBy": self.createdBy,
            "creationDate": self.creationDate,
            "updateBy": self.updateBy,
            "updateDate": self.updateDate,
            "creditCapacity": self.creditCapacity,
            "cardTypeId": self.cardTypeId,
            "expirationDate": self.expirationDate,
            "isDeleted": self.isDeleted,
            # "overdraft": self.overdraft,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """

        if 'bankAccountId' in data:
            self.bankAccountId = data['bankAccountId']
        if 'bankId' in data:
            self.bankId = data['bankId']
        if 'cardTypeId' in data:
            self.cardTypeId = data['cardTypeId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'openingDate' in data:
            self.openingDate = converters.convert_string_to_date(data['openingDate'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'expirationDate' in data:
            self.expirationDate = converters.convert_string_to_date(data['expirationDate'])
        if 'bankingTax' in data:
            self.bankingTax = data['bankingTax']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'accountNumber' in data:
            self.accountNumber = data['accountNumber']
        if 'office' in data:
            self.office = data['office']
        if 'owner' in data:
            self.owner = data['owner']
        if 'accountType' in data:
            self.accountType = data['accountType']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'creditCapacity' in data:
            self.creditCapacity = data['creditCapacity']
        # if 'overdraft' in data:
        #     self.overdraft = data['overdraft']

        return self

    @staticmethod
    def get_bank_account(bank_account_id):
        """

        :param bank_account_id:
        :return:
        """
        bank_account = session.query(BankAccount).get(bank_account_id)

        if bank_account is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        bank_account = bank_account.export_data()
        response = jsonify(bank_account)
        return response


    @staticmethod
    def search_bank_account(**kwargs):
        """
        :param: kwargs
        :return: Return Search from specific params
        """
        by_param = kwargs.get("by_param")
        branch_id = kwargs.get("branch_id")

        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        list_bank_account = []

        if by_param:
            f = None
            def export_by_param(data): return {}

            if by_param == 'transferaccount':
                f = (BankAccount.branchId == branch_id,
                     BankAccount.accountType != "T",)

                def export_by_param(data):
                    return {
                        'bankAccountId': data.bankAccountId,
                        'accountType': data.accountType,
                        'nameType': "CTA CORRIENTE" if data.accountType is "C" else "CTA AHORRO"
                        if data.accountType is "A" else "T. CRÉDITO",
                        'accountNumber': data.accountNumber,
                        'office': data.office,
                    }
            elif by_param == 'listdebitaccount':
                f = (BankAccount.branchId == branch_id,
                     BankAccount.accountType == "T",)

                def export_by_param(data):
                    return {
                        'bankAccountId': data.bankAccountId,
                        'accountType': data.accountType,
                        'nameType': "CTA CORRIENTE" if data.accountType is "C" else "CTA AHORRO"
                        if data.accountType is "A" else "T. CRÉDITO",
                        'accountNumber': data.accountNumber,
                        'office': data.office,
                    }

            elif by_param == 'currentaccount':
                f = (BankAccount.branchId == branch_id,
                     BankAccount.accountType == "C",)

                def export_by_param(data):
                    return {
                        'bankAccountId': data.bankAccountId,
                        'accountType': data.accountType,
                        'nameType': "CTA CORRIENTE" if data.accountType is "C" else "",
                        'accountNumber': data.accountNumber,
                        'office': data.office,
                        'bankName': (data.financialEntity.name + " " if
                        data.bankId and data.financialEntity else "") +'({0} {1} {2} {3})'.format(
                            '' if data.financialEntity.thirdParty.tradeName is None
                            else data.financialEntity.thirdParty.tradeName,
                            '' if data.financialEntity.thirdParty.lastName is None
                            else data.financialEntity.thirdParty.lastName,
                            '' if data.financialEntity.thirdParty.maidenName is None
                            else data.financialEntity.thirdParty.maidenName,
                            '' if data.financialEntity.thirdParty.firstName is None
                            else data.financialEntity.thirdParty.firstName,
                        ) if  data.financialEntity.thirdParty else "",
                    }

            bank_account = [export_by_param(bank_account)
                            for bank_account in session.query(BankAccount)
                                .filter(and_(*f)).all()]

            response = jsonify(data=bank_account)
            return response

        if search:
            list_bank_account = [BankAccount.export_data(bank_account) for bank_account
                                 in session.query(BankAccount)
                                     .filter(and_(
                    BankAccount.branchId == branch_id,
                    or_(True if search == "" else None,
                        or_(*[BankAccount.accountNumber.contains(word) for word in words],
                        *[BankAccount.office.contains(word) for word in words]))))
                                     .order_by(BankAccount.accountNumber)]

            response = jsonify(data=list_bank_account)
            if len(list_bank_account) == 0:
                response = jsonify({'code': 404, 'message': 'Not found'})
                response.status_code = 404

            return response

        else:
            bank_account = [BankAccount.export_data(bank_account)
                            for bank_account in session.query(BankAccount)
                                .filter(BankAccount.branchId == branch_id).all()]

            response = jsonify(data=bank_account)
            return response


    @staticmethod
    def post_bank_account(data):
        """

        :param data:
        :return:
        """
        if bank_account_exist(data['accountNumber'], data['branchId']):
            response = jsonify({'error': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        bank_Account = BankAccount()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        bank_Account.import_data(data)
        session.add(bank_Account)

        try:
            session.commit()
            response = jsonify(bankAccountId=bank_Account.bankAccountId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


    @staticmethod
    def put_bank_account(bank_account_id, data):
        """

        :param bank_account_id:
        :param data:
        :return:
        """
        if bank_account_id != data['bankAccountId']:
            response = jsonify({'error': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        bank_account = session.query(BankAccount).get(bank_account_id)

        if not bank_account:
            response = jsonify({'error': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        data['creationDate'] = bank_account.creationDate
        data['updateDate'] = datetime.now()
        data['createdBy'] = bank_account.createdBy
        data['updateBy'] = g.user['name']

        bank_account = bank_account.import_data(data)
        session.add(bank_account)

        try:
            session.commit()
            response = jsonify({'ok': 'ok'})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


    @staticmethod
    def delete_bank_account(bank_account_id):
        """

        :param bank_account_id:
        :return:
        """
        bank_account = session.query(BankAccount).get(bank_account_id)

        if bank_account is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(bank_account)

        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente', "ok": "ok"})
            response.status_code = 200
            return response
        except KeyError as e:
            session.rollback()
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


def bank_account_exist(bank_account_number,branch_id):
    return session.query(BankAccount).filter(BankAccount.branchId == branch_id,
                                             BankAccount.accountNumber == bank_account_number
                                             ).count()