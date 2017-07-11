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
from ...models import PaymentDetail

class Bankcheckbook(Base):
    __tablename__ = 'bankcheckbooks'

    bankCheckBookId = Column(Integer, primary_key=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    state = Column(Integer)
    isDeleted = Column(Integer)
    prefix = Column(String(5), default="")
    initialCheck = Column(String(10))
    finalCheck = Column(String(10))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    lastConsecutive = Column(Integer)

    bankaccount = relationship(u'BankAccount')
    paymentDetail = relationship(u'PaymentDetail', lazy='dynamic')
    # paymentDetail = relationship(u'PaymentDetail', primaryjoin=bankCheckBookId == PaymentDetail.bankCheckBookId,
    #                          cascade='all, delete-orphan')

    def export_data(self):
        """

        :return:
        """
        return {
            "bankCheckBookId": self.bankCheckBookId,
            "bankAccountId": self.bankAccountId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "state": bool(self.state),
            "isDeleted": self.isDeleted,
            "prefix": self.prefix,
            "initialCheck": self.initialCheck,
            "range": '{0} - {1}'.format(self.initialCheck, self.finalCheck),
            "finalCheck": self.finalCheck,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "lastConsecutive": self.lastConsecutive,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if "bankCheckBookId" in data:
            self.bankCheckBookId = data['bankCheckBookId']
        if "bankAccountId" in data:
            self.bankAccountId = data['bankAccountId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "state" in data:
            self.state = data['state']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "prefix" in data:
            self.prefix = data['prefix']
        if "initialCheck" in data:
            self.initialCheck = data['initialCheck']
        if "finalCheck" in data:
            self.finalCheck = data['finalCheck']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']
        if "lastConsecutive" in data:
            self.lastConsecutive = data['lastConsecutive']

        return self

    @staticmethod
    def get_bank_checkbooks():
        """
        Allow obtain all bank_checkbooks ordered by bankCheckBookId
        :return all list bank_checkbooks
        """
        list_bank_checkbooks = [Bankcheckbook.export_data(bank_checkbook)
                                for bank_checkbook in session.query(Bankcheckbook)
                              .order_by(Bankcheckbook.bankCheckBookId).all()]

        list_bank_checkbooks = jsonify(data=list_bank_checkbooks)
        return list_bank_checkbooks

    @staticmethod
    def get_bank_checkbook(bank_checkbooks_id):
        """

        :param bank_checkbooks_id:
        :return:
        """
        bank_checkbook = session.query(Bankcheckbook).get(bank_checkbooks_id)

        if bank_checkbook is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        bank_checkbook = bank_checkbook.export_data()
        response = jsonify(bank_checkbook)
        return response

    @staticmethod
    def get_bank_checkbooks_bybank(bank_checkbooks_id):
        """

        :param bank_checkbooks_id:
        :return:
        """
        def export_data_bybank(data):
            return {
                "bankCheckBookId": data.bankCheckBookId,
                "bankAccountId": data.bankAccountId,
                "range": '{0} - {1}'.format(data.initialCheck, data.finalCheck),
                "prefix": data.prefix,
                "initialCheck": data.initialCheck,
                "finalCheck": data.finalCheck,
                "state": bool(data.state),
                "lastConsecutive": data.lastConsecutive,
                "canChange": any(p for p in data.paymentDetail if p.bankCheckBookId == data.bankCheckBookId),
            }

        list_bank_checkbooks = [export_data_bybank(bank_checkbooks) for bank_checkbooks in session.query(Bankcheckbook)\
            .join(PaymentDetail, PaymentDetail.bankCheckBookId == Bankcheckbook.bankCheckBookId, isouter=True)
            .filter(Bankcheckbook.bankAccountId == bank_checkbooks_id)]

        response = jsonify(data=list_bank_checkbooks)
        return response


    @staticmethod
    def post_bank_checkbooks(data):
        """
            Allow create a new bankchekbook
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        for single in data:

            if 'bankCheckBookId' in single and bank_checkbook_exist(single['bankCheckBookId']) > 0:

                bank_checkbook_id = single['bankCheckBookId']
                bank_checkbook = session.query(Bankcheckbook).get(bank_checkbook_id)

                single['creationDate'] = bank_checkbook.creationDate
                single['updateDate'] = datetime.now()
                single['createdBy'] = bank_checkbook.createdBy
                single['updateBy'] = g.user['name']

                bank_checkbook = bank_checkbook.import_data(single)
                session.add(bank_checkbook)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            else: # Creo un nuevo checkbook
                bank_checkbook = Bankcheckbook()

                single['creationDate'] = datetime.now()
                single['updateDate'] = datetime.now()
                single['createdBy'] = g.user['name']
                single['updateBy'] = g.user['name']
                bank_checkbook.import_data(single)

                try:
                    session.add(bank_checkbook)
                    session.flush()
                except KeyError as e:
                    raise ValidationError('Invalid list_bank_checkbook: missing' + e.args[0])
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

        try:

            session.commit()
            response = jsonify({'ok': 'ok'})
            return response

        except KeyError as e:
            raise ValidationError('Invalid list_bank_checkbook: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)


    @staticmethod
    def delete_bank_checkbooks(bank_checkbooks_id):
        """

        :param bank_checkbooks_id:
        :return:
        """
        bank_account = session.query(Bankcheckbook).get(bank_checkbooks_id)

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


def bank_checkbook_exist(bank_checkbook_id):
    return session.query(Bankcheckbook)\
        .filter(Bankcheckbook.bankCheckBookId == bank_checkbook_id).count()

