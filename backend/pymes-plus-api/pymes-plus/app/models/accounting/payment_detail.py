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
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT, DECIMAL
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from ...utils import converters

class PaymentDetail(Base):
    __tablename__ = 'paymentdetails'

    paymentDetailId = Column(Integer, primary_key=True)
    paymentMethodId = Column(ForeignKey(u'paymentmethods.paymentMethodId'), index=True)
    bankCheckBookId = Column(ForeignKey(u'bankcheckbooks.bankCheckBookId'), index=True)
    finantialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    bankAccountId = Column(ForeignKey(u'bankaccounts.bankAccountId'), index=True)
    paymentReceiptId = Column(ForeignKey(u'paymentreceipts.paymentReceiptId'), index=True)
    dueDate = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    state = Column(TINYINT)
    isDeleted = Column(Integer, default=0)
    balance = Column(DECIMAL(18, 4), default=0.0)
    value = Column(DECIMAL(18, 4), default=0.0)
    prefixNumber = Column(String(5), default="")
    documentNumber = Column(String(10))
    cardNumber = Column(String(20))
    authorizationNumber = Column(String(20))
    beneficiary = Column(String(100))
    comments = Column(String(200))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    accountNumber = Column(String(50))
    bankName = Column(String(50))
    quoteNumber = Column(SMALLINT(6))

    bankAccount = relationship(u'BankAccount', foreign_keys=[bankAccountId])
    bankCheckBook = relationship(u'Bankcheckbook', foreign_keys=[bankCheckBookId])
    financialEntity = relationship(u'FinancialEntity', foreign_keys=[finantialEntityId])
    paymentMethod = relationship(u'PaymentMethod', foreign_keys=[paymentMethodId])
    paymentReceipt = relationship(u'PaymentReceipt', foreign_keys=[paymentReceiptId])

    def export_data(self):
        """

        :return:
        """
        return {
            "paymentDetailId": self.paymentDetailId,
            "paymentMethodId": self.paymentMethodId,
            'paymentType': None if self.paymentMethod is None else self.paymentMethod.paymentType,
            'paymentMethod': None if self.paymentMethod is None else self.paymentMethod.export_data(),
            "bankCheckBookId": self.bankCheckBookId,
            'bankCheckBook': None if self.bankCheckBook is None else self.bankCheckBook.export_data(),
            "finantialEntityId": self.finantialEntityId,
            'financialEntity': None if self.financialEntity is None else self.financialEntity.export_data(),
            "bankAccountId": self.bankAccountId,
            'bankAccount': None if self.bankAccount is None else self.bankAccount.export_data(),
            "paymentReceiptId": self.paymentReceiptId,
            # 'paymentReceipt': None if self.paymentReceipt is None else self.paymentReceipt.export_data(),
            "dueDate": self.dueDate,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "state": self.state,
            "isDeleted": self.isDeleted,
            "balance": self.balance,
            "value": self.value,
            "prefixNumber": self.prefixNumber,
            "documentNumber": self.documentNumber,
            "cardNumber": self.cardNumber,
            "authorizationNumber": self.authorizationNumber,
            "beneficiary": self.beneficiary,
            "comments": self.comments,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "accountNumber": self.accountNumber,
            "bankName": self.bankName,
            "quoteNumber": self.quoteNumber,
        }


    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'paymentDetailId' in data:
            self.paymentDetailId = data['paymentDetailId']
        if 'paymentMethodId' in data:
            self.paymentMethodId = data['paymentMethodId']
        if 'bankCheckBookId' in data:
            self.bankCheckBookId = data['bankCheckBookId']
        if 'finantialEntityId' in data:
            self.finantialEntityId = data['finantialEntityId']
        if 'bankAccountId' in data:
            self.bankAccountId = data['bankAccountId']
        if 'paymentReceiptId' in data:
            self.paymentReceiptId = data['paymentReceiptId']
        if 'dueDate' in data:
            self.dueDate = converters.convert_string_to_date(data['dueDate'])
        if 'creationDate' in data:
            self.creationDate = converters.convert_string_to_date(data['creationDate'])
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'state' in data:
            self.state = data['state']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'balance' in data:
            self.balance = data['balance']
        if 'value' in data:
            self.value = data['value']
        if 'prefixNumber' in data:
            self.prefixNumber = data['prefixNumber']
        if 'documentNumber' in data:
            self.documentNumber = str(data['documentNumber'])
        if 'cardNumber' in data:
            self.cardNumber = data['cardNumber']
        if 'authorizationNumber' in data:
            self.authorizationNumber = data['authorizationNumber']
        if 'beneficiary' in data:
            self.beneficiary = data['beneficiary']
        if 'comments' in data:
            self.comments = data['comments']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'accountNumber' in data:
            self.accountNumber = data['accountNumber']
        if 'bankName' in data:
            self.bankName = data['bankName']
        if 'quoteNumber' in data:
            self.quoteNumber = data['quoteNumber']

        if 'paymentType' in data:
            self.paymentType = data['paymentType']

        return self

    def save(self):
        """
        Allow save a payment detail in database
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
        Allow save a payment detail in database
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
    def get_payment_details_by_document_header_id(document_number):
        """
        Allow obtain a payment details from document header identifier
        :param id: document header identifier
        :return: a payment details object in JSON format
        """
        payment_detail = session.query(PaymentDetail).\
            filter(PaymentDetail.documentNumber == document_number).all()
        return payment_detail


    @staticmethod
    def get_payment_details_by_id(id):
        """
        Allow obtain a payment details from payment detail identifier
        :param id: document header identifier
        :return: a payment details object in JSON format
        """
        payment_detail = session.query(PaymentDetail)\
            .filter(PaymentDetail.paymentDetailId == id).all()
        return payment_detail

