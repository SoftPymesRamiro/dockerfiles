# coding=utf-8
from datetime import datetime
from flask import jsonify
from ... import Base
from ... import session
from .sub_zones_3 import SubZone3
from .sub_inventory_group_1 import SubInventoryGroup1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class SubZone2(Base):
    __tablename__ = 'subzones2'

    subZone2Id = Column(Integer, primary_key=True, nullable=False)
    subZone1Id = Column(ForeignKey(u'subzones1.subZone1Id'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(5))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    subZone3 = relationship("SubZone3", primaryjoin=subZone2Id == SubZone3.subzone2Id,
                            cascade="all, delete, delete-orphan")


    @staticmethod
    def export_data(data):
        return {
            "subZone2Id" : data.subZone2Id,
            "subZone1Id" : data.subZone1Id,
            "creationDate" : data.creationDate,
            "updateDate" : data.updateDate,
            "isDeleted" : data.isDeleted,
            "code" : data.code,
            "name" : data.name,
            "createdBy" : data.createdBy,
            "updateBy" : data.updateBy,
            'subZones3': [] if data.subZone3 is None or len(data.subZone3) == 0
            else [SubZone3.export_data(sub3) for sub3 in data.subZone3]
        }


    def import_data(self, data):
        pass
