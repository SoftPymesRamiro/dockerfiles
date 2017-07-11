# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from math import ceil
from flask import jsonify
from ... import Base
from ... import session
from .sub_zones_1 import SubZone1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_


class DiscountRule(Base):
    __tablename__ = 'discountrules'

    discountRuleId = Column(Integer, primary_key=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    zoneId = Column(ForeignKey(u'zones.zoneId'), index=True)
    subZone1Id = Column(ForeignKey(u'subzones1.subZone1Id'), index=True)
    subZone2Id = Column(ForeignKey(u'subzones2.subZone2Id'), index=True)
    subZone3Id = Column(ForeignKey(u'subzones3.subZone3Id'), index=True)
    discountListId = Column(ForeignKey(u'discountlists.discountListId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    ruleType = Column(String(2))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    customer = relationship(u'Customer', foreign_keys=[customerId])
    discountlist = relationship(u'Discountlist', foreign_keys=[discountListId])
    subzones1 = relationship(u'SubZone1', foreign_keys=[subZone1Id])
    subzones2 = relationship(u'SubZone2', foreign_keys=[subZone2Id])
    subzones3 = relationship(u'SubZone3', foreign_keys=[subZone3Id])
    zone = relationship(u'Zone', foreign_keys=[zoneId])

    discountRuleExceptions = relationship('DiscountRuleException')

    def export_data(self):
        """

        :return:
        """
        return {
            'discountRuleId' : self.discountRuleId,
            'customerId' : self.customerId,
            'zoneId' : self.zoneId,
            'subZone1Id' : self.subZone1Id,
            'subZone2Id' : self.subZone2Id,
            'subZone3Id' : self.subZone3Id,
            'discountListId' : self.discountListId,
            'creationDate' : self.creationDate,
            'updateDate' : self.updateDate,
            'isDeleted' : self.isDeleted,
            'ruleType' : self.ruleType,
            'createdBy' : self.createdBy,
            'updateBy' : self.updateBy
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'discountRuleId' in data:
            self.discountRuleId = data['discountRuleId']
        if 'customerId' in data:
            self.customerId = data['customerId']
        if 'zoneId' in data:
            self.zoneId = data['zoneId']
        if 'subZone1Id' in data:
            self.subZone1Id = data['subZone1Id']
        if 'subZone2Id' in data:
            self.subZone2Id = data['subZone2Id']
        if 'subZone3Id' in data:
            self.subZone3Id = data['subZone3Id']
        if 'discountListId' in data:
            self.discountListId = data['discountListId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'ruleType' in data:
            self.ruleType = data['ruleType']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self