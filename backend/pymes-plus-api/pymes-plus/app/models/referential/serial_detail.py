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

from ... import Base, session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, String, SmallInteger, Table
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from datetime import datetime
from flask import g


class SerialDetail(Base):
    """
        Database class
    """
    __tablename__ = 'serialdetails'

    serialDetailId = Column(Integer, primary_key=True)
    documentDetailId = Column(ForeignKey(u'documentdetails.documentDetailId'), index=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    serialId = Column(ForeignKey(u'serials.serialId'), index=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    type = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    documentdetail = relationship(u'DocumentDetail')
    documentheader = relationship(u'DocumentHeader')
    serial = relationship(u'Serial')
    warehouse = relationship(u'Warehouse')

    def export_data(self):
        """
            Return serial detail dict
            :return serial object in JSON format
        """
        return {
            'serialDetailId': self.serialDetailId,
            'documentDetailId': self.documentDetailId,
            'documentHeaderId': self.documentHeaderId,
            'serialId': self.serialId,
            'warehouseId': self.warehouseId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'type': self.type,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }

    def import_data(self, data):
        try:
            if 'serialDetailId' in data:
                self.serialDetailId = data['serialDetailId']
            if 'documentDetailId' in data:
                self.documentDetailId = data['documentDetailId']
            if 'documentHeaderId' in data:
                self.documentHeaderId = data['documentHeaderId']
            if 'serialId' in data:
                self.serialId = data['serialId']
            if 'warehouseId' in data:
                self.warehouseId = data['warehouseId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'type' in data:
                self.type = data['type']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
        except Exception as e:
            raise e

    def save(self):
        """
            Allow save a serial detail in database
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
            Allow update a serial detail in database
            :exception: An error occurs when update not performance
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

    def delete(self):
        """
            Allow delete a serial detail record
            :return: None
        """
        try:
            session.delete(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_serial_detail_by_serial_id(serial_id):
        """
            Allow get serial detail list according serial id
            :param serial_id: serial id
            :return: serial detail object list
        """
        try:
            serial_details = session.query(SerialDetail).filter(SerialDetail.serialId == serial_id).all()
            return serial_details
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_serial_detail_by_document_header_id(document_header_id):
        """
            Allow get serial detail list according document header id
            :param document_header_id: document header id
            :return: serial detail object list
        """
        try:
            serial_details = session.query(SerialDetail).filter(SerialDetail.documentHeaderId == document_header_id)\
                .all()
            return serial_details
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)
