# coding=utf-8
from ... import Base, session
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.dialects.mysql import TINYINT


class IdentificationType(Base):
    __tablename__ = 'identificationtypes'
    identificationTypeId = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(3), nullable=False)
    name = Column(String(50), nullable=False)
    createdBy = Column(String(50), nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50), nullable=False)
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT, default=0)
    identificationTypeDian = Column(String(4), nullable=False)

    def export_data(self):
        return {
            'identificationTypeId': self.identificationTypeId,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'identificationTypeDian': self.identificationTypeDian
        }

    def export_data_name(self):
        return {
            'identificationTypeId': self.identificationTypeId,
            'code': self.code,
            'name': self.name,
            'identificationTypeDian': self.identificationTypeDian
        }

    @staticmethod
    def get_identification_types():
        it = [i.export_data() for i in session.query(IdentificationType).all()]
        return it