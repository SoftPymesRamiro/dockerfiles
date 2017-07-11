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
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from sqlalchemy import or_, and_, func
from ...utils import converters

class PaymentReceipt(Base):
    __tablename__ = 'paymentreceipts'

    paymentReceiptId = Column(Integer, primary_key=True)
    documentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    firstQuota = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer, default=0)
    firstValue = Column(DECIMAL(18, 4), default=0.0)
    paymentNumber = Column(String(10))
    cashReceipt = Column(String(10))
    periodicityQuota = Column(String(1))
    comments = Column(String(200))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    quotaNumbers = Column(Integer)

    documentheader = relationship(u'DocumentHeader', foreign_keys=[documentHeaderId])
    documenttype = relationship(u'DocumentType', foreign_keys=[documentTypeId])

    paymentDetails = relationship(u'PaymentDetail',
                                      primaryjoin='PaymentDetail.paymentReceiptId == PaymentReceipt.paymentReceiptId')

    def export_data(self):
        return {
            'paymentReceiptId': self.paymentReceiptId,
            'documentTypeId': self.documentTypeId,
            'documentHeaderId': self.documentHeaderId,
            'firstQuota': self.firstQuota,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'firstValue': self.firstValue,
            'paymentNumber': self.paymentNumber,
            'cashReceipt': self.cashReceipt,
            'periodicityQuota': self.periodicityQuota,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'quotaNumbers': self.quotaNumbers,
            'paymentDetails': None if self.paymentDetails is None else [payment_details.export_data()
                                                                        for payment_details in self.paymentDetails]
        }

    def import_data(self, data):
        if 'paymentReceiptId' in data:
            self.paymentReceiptId  = data['paymentReceiptId']
        if 'documentTypeId' in data:
            self.documentTypeId  = data['documentTypeId']
        if 'documentHeaderId' in data:
            self.documentHeaderId  = data['documentHeaderId']
        if 'firstQuota' in data:
            self.firstQuota  = converters.convert_string_to_date(data['firstQuota'])
        if 'creationDate' in data:
            self.creationDate  = converters.convert_string_to_date(data['creationDate'])
        if 'updateDate' in data:
            self.updateDate  = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted  = data['isDeleted']
        if 'firstValue' in data:
            self.firstValue  = data['firstValue']
        if 'paymentNumber' in data:
            self.paymentNumber  = data['paymentNumber']
        if 'cashReceipt' in data:
            self.cashReceipt  = data['cashReceipt']
        if 'periodicityQuota' in data:
            self.periodicityQuota  = data['periodicityQuota']
        if 'comments' in data:
            self.comments  = data['comments']
        if 'createdBy' in data:
            self.createdBy  = data['createdBy']
        if 'updateBy' in data:
            self.updateBy  = data['updateBy']
        if 'quotaNumbers' in data:
            self.quotaNumbers  = data['quotaNumbers']
        return self

    def save(self):
        """
        Allow save a payment receipt in database
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

            return self.paymentReceiptId
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)


    def update(self):
        """
        Allow save a payment receipt in database
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
    def get_receipt_by_document_identifier(identifier):
        """
        Allow obtain a Payment Receipt according to identifier
        :param identifier: document Header number
        :return: a JSON object with Payment Receipt information
        """
        payment_receipts = session.query(PaymentReceipt). \
            filter(PaymentReceipt.documentHeaderId == identifier).first()
        return payment_receipts

    @staticmethod
    def get_payment_receipts_by_id(id):
        """
        Allow obtain a payment receipts from payment receipt identifier
        :param id: document header identifier
        :return: a payment receipts object in JSON format
        """
        payment_receipts = session.query(PaymentReceipt) \
            .filter(PaymentReceipt.paymentDetailId == id).all()
        return payment_receipts




