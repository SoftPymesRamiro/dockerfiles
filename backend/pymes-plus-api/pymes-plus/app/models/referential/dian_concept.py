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
from ... import Base
from flask import jsonify
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, VARBINARY
from sqlalchemy.orm import relationship, backref
from .dian_form_concept import DianFormConcept

class DianConcept(Base):
    __tablename__ = 'dianconcepts'

    dianConceptId = Column(Integer, primary_key=True)
    dianFormId = Column(ForeignKey(u'dianforms.dianFormId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    minimumValue = Column(DECIMAL(18, 2), default=0.0)
    code = Column(String(4))
    name = Column(String(200))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    dianform = relationship(u'DianForm', foreign_keys=[dianFormId])
    dianFormConcepts = relationship('DianFormConcept', lazy='dynamic')


    def export_data(self):
        """
        Allow obtain dian_form data in session
        :return: an dian_form object in Json format
        """
        return {
            'dianConceptId': self.dianConceptId,
            'dianFormId': self.dianFormId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'minimumValue': self.minimumValue,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'dianformconcepts': None if self.dianFormConcepts is None else[
                DianFormConcept.export_data(dian_form_concept) for dian_form_concept in self.dianFormConcepts
            ],
        }


    def import_data(self, data):
        """
        Allow create dian_form fro data information
        :param data: information of dian_form
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:  dian_form object
        """
        if 'dianConceptId' in data:
            self.dianConceptId = data['dianConceptId']
        if 'dianFormId' in data:
            self.dianFormId = data['dianFormId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'minimumValue' in data:
            self.minimumValue = data['minimumValue']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self
