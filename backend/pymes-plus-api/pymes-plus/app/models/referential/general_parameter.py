# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 10-08-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"
__status__ = "develop"

from datetime import datetime
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from ...exceptions import InternalServerError


class GeneralParameter(Base):
    __tablename__ = 'generalparameters'

    generalParameterId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    controlNumber = Column(Integer)
    reteIVA = Column(Integer, default=1, nullable=False)
    reteICA = Column(Integer, default=1, nullable=False)
    ica = Column(Integer, default=1, nullable=False)
    isDeleted = Column(Integer, default=0)
    cDate = Column(Integer)
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    taxRoundValue = Column(TINYINT, default=1000, nullable=False)
    sessionExpired = Column(TINYINT, default=30, nullable=False)

    @staticmethod
    def get_general_parameter():
        try:
            return session.query(GeneralParameter).first()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
