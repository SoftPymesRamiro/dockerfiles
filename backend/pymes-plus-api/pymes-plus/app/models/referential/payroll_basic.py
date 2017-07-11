from datetime import datetime
from flask import jsonify
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from sqlalchemy.orm import relationship, backref


class PayrollBasic(Base):
    __tablename__ = 'payrollbasics'

    payrollBasicId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey('branches.branchId'), index=True)
    payrollFrom = Column(DateTime, default=datetime.now())
    payrollThru = Column(DateTime, default=datetime.now())
    liquidatedDate = Column(DateTime, default=datetime.now())
    accountedDate = Column(DateTime, default=datetime.now())
    acumulatedDate = Column(DateTime, default=datetime.now())
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    lastPaymentPeriod = Column(TINYINT(1))
    payrollLiquidated = Column(TINYINT(1))
    payrollAccounted = Column(TINYINT(1))
    payrollAcumulated = Column(TINYINT(1))
    isDeleted = Column(TINYINT(1))
    year = Column(String(4))
    month = Column(String(2))
    paymentPeriod = Column(String(1))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    payrollType = Column(TINYINT(4))

    branch = relationship('Branch')

    def export_data(self):
        return {
            'payrollBasicId': self.payrollBasicId,
            'branchId': self.branchId,
            'payrollFrom': self.payrollFrom,
            'payrollThru': self.payrollThru,
            'liquidatedDate': self.liquidatedDate,
            'accountedDate': self.accountedDate,
            'acumulatedDate': self.acumulatedDate,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'lastPaymentPeriod': self.lastPaymentPeriod,
            'payrollLiquidated': self.payrollLiquidated,
            'payrollAccounted': self.payrollAccounted,
            'payrollAcumulated': self.payrollAcumulated,
            'isDeleted': self.isDeleted,
            'year': self.year,
            'month': self.month,
            'paymentPeriod': self.paymentPeriod,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'payrollType': self.payrollType,
        }
