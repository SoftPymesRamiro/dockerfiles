# coding=utf-8
from datetime import datetime
from ... import Base
from flask import jsonify
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship


class DocumentType(Base):
    __tablename__ = "documenttypes"

    documentTypeId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    needResolution = Column(TINYINT)
    isDeleted = Column(TINYINT)
    shortWord = Column(String(3))
    name = Column(String(200))
    isIncomePayment = Column(String(1))
    comments = Column(String(2000))
    url = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    def export_data(self):
        return {
            "documentTypeId": self.documentTypeId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "needResolution": self.needResolution,
            "isDeleted": self.isDeleted,
            "shortWord": self.shortWord,
            "name": self.name,
            "isIncomePayment": self.isIncomePayment,
            "comments": self.comments,
            "url": self.url,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
        }
