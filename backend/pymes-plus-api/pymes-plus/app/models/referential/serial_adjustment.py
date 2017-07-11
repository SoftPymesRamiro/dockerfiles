# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 07-07-2017
#########################################################
__author__ = "SoftPymes"
__credits__ = ["david"]

from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, or_
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ... import session


class SerialAdjustment(Base):
    __tablename__ = 'serialadjustments'

    serialAdjustmentId = Column(Integer, primary_key=True)
    serialId = Column(ForeignKey(u'serials.serialId'), index=True)
    documentDetailId = Column(ForeignKey(u'documentdetails.documentDetailId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    serialNumber = Column(String(30))
    oldSerialNumber = Column(String(30))
    action = Column(String(1))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    documentDetail = relationship(u'DocumentDetail')
    serial = relationship(u'Serial')

    def export_data(self):
        return {
            'serialAdjustmentId': self.serialAdjustmentId,
            'serialId': self.serialId,
            'documentDetailId': self.documentDetailId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'serialNumber': self.serialNumber,
            'oldSerialNumber': self.oldSerialNumber,
            'action': self.action,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'serial': self.serial.export_data_simple()
        }

    def import_data(self, data):
        try:
            if 'serialAdjustmentId' in data:
                self.serialAdjustmentId = data['serialAdjustmentId']
            if 'serialId' in data:
                self.serialId = data['serialId']
            if 'documentDetailId' in data:
                self.documentDetailId = data['documentDetailId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'serialNumber' in data:
                self.serialNumber = data['serialNumber']
            if 'oldSerialNumber' in data:
                self.oldSerialNumber = data['oldSerialNumber']
            if 'action' in data:
                self.action = data['action']
            if 'comments' in data:
                self.comments = data['comments']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
        except Exception as e:
            raise ValidationError(e)

    def save(self):
        """
            Allow save a serial in database
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