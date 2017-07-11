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


class DiscountListItem(Base):
    __tablename__ = 'discountlistitems'

    discountListItemId = Column(Integer, primary_key=True)
    inventoryGroupId = Column(ForeignKey(u'inventorygroups.inventoryGroupId'), index=True)
    subInventoryGroup2Id = Column(ForeignKey(u'subinventorygroups2.subInventoryGroup2Id'), index=True)
    subInventoryGroup3Id = Column(ForeignKey(u'subinventorygroups3.subInventoryGroup3Id'), index=True)
    discountListId = Column(ForeignKey(u'discountlists.discountListId'), index=True)
    subInventoryGroup1Id = Column(ForeignKey(u'subinventorygroups1.subInventoryGroup1Id'), index=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer, default=0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    discountlist = relationship(u'Discountlist', foreign_keys=[discountListId])
    inventorygroup = relationship(u'InventoryGroup', foreign_keys=[inventoryGroupId])
    item = relationship(u'Item', foreign_keys=[itemId])
    subinventorygroups1 = relationship(u'SubInventoryGroup1', foreign_keys=[subInventoryGroup1Id])
    subinventorygroups2 = relationship(u'SubInventoryGroup2', foreign_keys=[subInventoryGroup2Id])
    subinventorygroups3 = relationship(u'SubInventoryGroup3', foreign_keys=[subInventoryGroup3Id])


    def export_data(self):
        """

        :return:
        """
        return {
            'discountListItemId': self.discountListItemId,
            'inventoryGroupId': self.inventoryGroupId,
            'subInventoryGroup2Id': self.subInventoryGroup2Id,
            'subInventoryGroup3Id': self.subInventoryGroup3Id,
            'discountListId': self.discountListId,
            'subInventoryGroup1Id': self.subInventoryGroup1Id,
            'itemId': self.itemId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'discountListItemId' in data:
            self.discountListItemId = data['discountListItemId']
        if 'inventoryGroupId' in data:
            self.inventoryGroupId = data['inventoryGroupId']
        if 'subInventoryGroup2Id' in data:
            self.subInventoryGroup2Id = data['subInventoryGroup2Id']
        if 'subInventoryGroup3Id' in data:
            self.subInventoryGroup3Id = data['subInventoryGroup3Id']
        if 'discountListId' in data:
            self.discountListId = data['discountListId']
        if 'subInventoryGroup1Id' in data:
            self.subInventoryGroup1Id = data['subInventoryGroup1Id']
        if 'itemId' in data:
            self.itemId = data['itemId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        return self