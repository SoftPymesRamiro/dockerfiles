# coding=utf-8
from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT

from sqlalchemy.orm import relationship
from ... import session

class Depreciation(Base):
    __tablename__ = 'depreciations'

    depreciationId = Column(Integer, primary_key=True)
    depreciationPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    assetPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    expensePUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    assetPUC = relationship(u'PUC', primaryjoin='Depreciation.assetPUCId == PUC.pucId')
    # company = relationship(u'Company')
    depreciationPUC = relationship(u'PUC', primaryjoin='Depreciation.depreciationPUCId == PUC.pucId')
    expensePUC = relationship(u'PUC', primaryjoin='Depreciation.expensePUCId == PUC.pucId')

    def export_data(self):
        """
        Allow export depreciation short description
        :return: depreciation object in JSOn format
        """
        return {
            'depreciationId': self.depreciationId,
            'depreciationPUCId': self.depreciationPUCId,
            'assetPUCId': self.assetPUCId,
            'expensePUCId': self.expensePUCId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'assetPUC': self.assetPUC,
            'depreciationPUC': self.depreciationPUC,
            'expensePUC': self.expensePUC
        }

    def import_data(self, data):
        """

        :param data: json company with branch and partners
        :return: return an company object from json
        """
        if 'depreciationId' in data:
            self.depreciationId = data["depreciationId"]
        if 'depreciationPUCId' in data:
            self.depreciationPUCId = data["depreciationPUCId"]
        if 'assetPUCId' in data:
            self.assetPUCId = data["assetPUCId"]
        if 'expensePUCId' in data:
            self.expensePUCId = data["expensePUCId"]
        if 'companyId' in data:
            self.companyId = data["companyId"]
        if 'creationDate' in data:
            self.creationDate = data["creationDate"]
        if 'updateDate' in data:
            self.updateDate = data["updateDate"]
        if 'isDeleted' in data:
            self.isDeleted = data["isDeleted"]
        if 'createdBy' in data:
            self.createdBy = data["createdBy"]
        if 'updateBy' in data:
            self.updateBy = data["updateBy"]
        if 'assetPUC' in data:
            self.assetPUC = data["assetPUC"]
        if 'depreciationPUC' in data:
            self.depreciationPUC = data["depreciationPUC"]
        if 'expensePUC' in data:
            self.expensePUC = data["expensePUC"]

        return self


    @staticmethod
    def get_list_deprecation(company_id):
        """
        Allow return a list Depreciation by company id (is used in accounting records)
        :param company_id: company id
        :return: puc list
        """
        try:
            list_deprecation = session.query(Depreciation)\
                .filter(Depreciation.companyId == company_id)
            return list_deprecation
        except Exception as e:
            session.rollback()
            raise e
