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
from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, String, SmallInteger, Table, func
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from datetime import datetime
from flask import g
from ...utils.converters import convert_string_to_date


class Serial(Base):
    """
        Database class
    """
    __tablename__ = 'serials'

    serialId = Column(Integer, primary_key=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    documentHeaderId = Column(ForeignKey(u'documentheaders.documentHeaderId'), index=True)
    documentDetailId = Column(ForeignKey(u'documentdetails.documentDetailId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    serialNumber = Column(String(30))
    type = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    documentdetail = relationship(u'DocumentDetail')
    documentheader = relationship(u'DocumentHeader')
    item = relationship(u'Item')
    warehouse = relationship(u'Warehouse')

    def export_data_simple(self):
        """
            Return data by a serial
            :return serial object in JSON format
        """
        return {
            'serialId': self.serialId,
            'serialNumber': self.serialNumber,
            'type': self.type,
        }

    def export_data(self):
        """
            Return data by a serial
            :return serial object in JSON format
        """
        return {
            'serialId': self.serialId,
            'warehouseId': self.warehouseId,
            'itemId': self.itemId,
            'documentHeaderId': self.documentHeaderId,
            'documentDetailId': self.documentDetailId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'serialNumber': self.serialNumber,
            'type': self.type,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }

    def import_data(self, data):
        """Allow import serial from data object
            :param data informatio by a new serial
            :exception KeyError an error occurs when key dont set in data
            :return create a new serial from data param
        """
        try:
            if 'serialId' in data:
                self.serialId = data['serialId']
            if 'warehouseId' in data:
                self.warehouseId = data['warehouseId']
            if 'itemId' in data:
                self.itemId = data['itemId']
            if 'documentHeaderId' in data:
                self.documentHeaderId = data['documentHeaderId']
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
            if 'type' in data:
                self.type = data['type']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
        except KeyError as e:
            raise ValidationError("Invalid serial: missing " + e.args[0])
        except Exception as e:
            raise e

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

    def update(self):
        """
            Allow update a serial in database
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
            Allow delete a serial record
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
    def get_serial_by_document_header_id(document_header_id):
        """
            Allow get serial list according document header id
            :param document_header_id: document header id
            :return: serial object list
        """
        try:
            serials = session.query(Serial).filter(Serial.documentHeaderId == document_header_id).all()
            return serials
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_serials(**kwargs):
        """
            Allow get serials according parameters (it's used for sales)
            :param kwargs: dict of parameters
            :return: list object
        """
        try:
            from .. import DocumentHeader
            item_id = kwargs.get('item_id')
            type_ = kwargs.get('type_')
            document_date = kwargs.get('document_date')
            document_date = convert_string_to_date(document_date)
            serials = session.query(Serial)\
                .join(DocumentHeader, DocumentHeader.documentHeaderId == Serial.documentHeaderId)\
                .filter(Serial.itemId == item_id, Serial.type == type_,
                        func.date(DocumentHeader.documentDate) <= document_date)\
                .all()
            return serials
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)