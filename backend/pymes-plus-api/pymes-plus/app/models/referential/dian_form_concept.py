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

class DianFormConcept(Base):
    __tablename__ = 'dianformconcepts'

    dianFormConceptId = Column(Integer, primary_key=True)
    pucId = Column(ForeignKey('puc.pucId'), index=True)
    dianConceptId = Column(ForeignKey(u'dianconcepts.dianConceptId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    value1Source = Column(String(1))
    identificationSource = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    dianconcept = relationship(u'DianConcept', foreign_keys=[dianConceptId])
    puc = relationship(u'PUC', foreign_keys=[pucId])

    def export_data(self):
        """
        Allow obtain dian_form data in session
        :return: an dian_form object in Json format
        """
        return {
            'dianFormConceptId': self.dianFormConceptId,
            'pucId': self.pucId,
            "puc": None if self.pucId is None or self.puc is None else{
                "pucId": self.puc.pucId,
                "pucAccount": '{0}{1}{2}{3}{4} {5}'.format(self.puc.pucClass,
                                                           self.puc.pucSubClass,
                                                           self.puc.account,
                                                           self.puc.subAccount,
                                                           self.puc.auxiliary1,
                                                           self.puc.name),
                "name": self.puc.name,
            },
            'dianConceptId': self.dianConceptId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'value1Source': self.value1Source,
            'identificationSource': self.identificationSource,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def import_data(self, data):
        """
        Allow create dian_form fro data information
        :param data: information of dian_form
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:  dian_form object
        """
        if 'dianFormConceptId' in data:
            self.dianFormConceptId = data['dianFormConceptId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'dianConceptId' in data:
            self.dianConceptId = data['dianConceptId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'value1Source' in data:
            self.value1Source = data['value1Source']
        if 'identificationSource' in data:
            self.identificationSource = data['identificationSource']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self
