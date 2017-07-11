# coding=utf-8
from ... import Base, session
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYINT


class IVAType(Base):
    __tablename__ = 'ivatypes'

    ivaTypeId = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    createdBy = Column(String(50), nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50), nullable=False)
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT, default=0)

    def export_data(self):
        return {
            'ivaTypeId': self.ivaTypeId,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted
        }

    def export_data_name(self):
        return {
            'ivaTypeId': self.ivaTypeId,
            'code': self.code,
            'name': self.name
        }

    @staticmethod
    def get_iva_types():
        it = [i.export_data() for i in session.query(IVAType).all()]
        return it
