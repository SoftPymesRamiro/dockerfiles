# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from datetime import datetime
from ... import Base, session
from flask import jsonify
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT


class CashRegister(Base):
    __tablename__ = 'cashregisters'

    cashRegisterId = Column(Integer, primary_key=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    warehouseId = Column(ForeignKey(u'warehouses.warehouseId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT(1))
    useWeight = Column(TINYINT(1))
    rtsEnable = Column(TINYINT(1))
    commandNewLine = Column(TINYINT(1))
    factor = Column(DECIMAL(18, 4), default=0.0)
    code = Column(String(3))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    weightPort = Column(String(10))
    weightRate = Column(String(10))
    weightParity = Column(String(10))
    weightBits = Column(String(10))
    weightStops = Column(String(10))
    command = Column(String(50))
    returnScale = Column(String(10))
    returnScanner = Column(String(10))

    branch = relationship(u'Branch')
    costcenter = relationship(u'CostCenter')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    section = relationship(u'Section')
    warehouse = relationship(u'Warehouse')

    def export_data(self):
        """
        Allow export data of chash register
        :return:
        """
        return {
            'cashRegisterId': self.cashRegisterId,
            'dependencyId': self.dependencyId,
            'warehouseId': self.warehouseId,
            'divisionId': self.divisionId,
            'costCenterId': self.costCenterId,
            'sectionId': self.sectionId,
            'branchId': self.branchId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'useWeight': self.useWeight,
            'rtsEnable': self.rtsEnable,
            'commandNewLine': self.commandNewLine,
            'factor': self.factor,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'weightPort': self.weightPort,
            'weightRate': self.weightRate,
            'weightParity': self.weightParity,
            'weightBits': self.weightBits,
            'weightStops': self.weightStops,
            'command': self.command,
            'returnScale': self.returnScale,
            'returnScanner': self.returnScanner,
        }
