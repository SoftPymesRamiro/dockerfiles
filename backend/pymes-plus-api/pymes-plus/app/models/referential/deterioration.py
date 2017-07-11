# coding=utf-8
from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT

from sqlalchemy.orm import relationship


class Deterioration(Base):
    __tablename__ = 'deteriorations'

    deteriorationId = Column(Integer, primary_key=True)
    deteriorationPucId = Column(ForeignKey(u'puc.pucId'), index=True)
    inventoryPucId = Column(ForeignKey(u'puc.pucId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    createdBy = Column(String(100))
    updateBy = Column(String(100))

    deteriorationPUC = relationship(u'PUC', primaryjoin='Deterioration.deteriorationPucId == PUC.pucId')
    # puc1 = relationship(u'PUC', primaryjoin='Deterioration.inventoryPucId == PUC.pucId')

