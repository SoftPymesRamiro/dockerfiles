# coding=utf-8
from datetime import datetime
from flask import jsonify
from ... import Base
from ... import session
from .sub_zones_2 import SubZone2
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class SubZone1(Base):
    __tablename__ = 'subzones1'

    subZone1Id = Column(Integer, primary_key=True, nullable=False)
    zoneId = Column(ForeignKey(u'zones.zoneId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(5))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    subZone2 = relationship("SubZone2", primaryjoin=subZone1Id == SubZone2.subZone1Id,
                            cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to subZone1

            :param  data
            :return subZone1 in JSON object

        """
        return {
            "subZone1Id" : data.subZone1Id,
            "zoneId" : data.zoneId,
            "creationDate" : data.creationDate,
            "updateDate" : data.updateDate,
            "isDeleted" : data.isDeleted,
            "code" : data.code,
            "name" : data.name,
            "createdBy" : data.createdBy,
            "updateBy" : data.updateBy,
            'subZones2': [] if data.subZone2 is None or len(data.subZone2) == 0
                else [SubZone2.export_data(sub2) for sub2 in data.subZone2]
        }


    def import_data(self, data):
        pass