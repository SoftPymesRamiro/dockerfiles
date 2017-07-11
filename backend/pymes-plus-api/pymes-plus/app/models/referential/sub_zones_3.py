# coding=utf-8
from datetime import datetime
from flask import jsonify
from ... import Base
from ... import session
from .sub_inventory_group_1 import SubInventoryGroup1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class SubZone3(Base):
    __tablename__ = 'subzones3'

    subZone3Id = Column(Integer, primary_key=True, nullable=False)
    subzone2Id = Column(ForeignKey(u'subzones2.subZone2Id'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(5))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to subZone1

            :param  data
            :return subZone1 in JSON object

        """
        return {
            "subZone3Id": data.subZone3Id,
            "subzone2Id": data.subzone2Id,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
        }

    def import_data(self, data):
        pass