# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################

__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"
__status__ = "develop"


from ... import Base
from sqlalchemy import String, Integer, Column


class AccountingAllThirds(Base):
    """AccountingRecord as a public model class.

    """
    __tablename__ = 'accountingallthirds'

    accountingallthirdsid = Column(String(36), primary_key=True)
    allThirdId = Column(Integer)
    allThirdType = Column(String(2))
    name = Column(String(353))
    identificationNumber = Column(String(50))
    identificationDV = Column(String(1))

    def export_data(self):
        """

        :return:
        """
        return {
            'accountingallthirdsid': self.accountingallthirdsid,
            'allThirdId': self.allThirdId,
            'allThirdType': self.allThirdType,
            'name': self.name,
            'identificationNumber': self.identificationNumber,
            'identificationDV': self.identificationDV
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'accountingallthirdsid' in data:
            self.accountingallthirdsid = data['accountingallthirdsid']
        if 'allThirdId' in data:
            self.allThirdId = data['allThirdId']
        if 'allThirdType' in data:
            self.allThirdType = data['allThirdType']
        if 'name' in data:
            self.name = data['name']
        if 'identificationNumber' in data:
            self.identificationNumber = data['identificationNumber']
        if 'identificationDV ' in data:
            self.identificationDV = data['identificationDV']
