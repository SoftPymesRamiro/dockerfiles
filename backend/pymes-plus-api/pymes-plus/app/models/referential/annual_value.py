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
from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, String, SmallInteger
from sqlalchemy.orm import relationship
from flask import jsonify, g
from sqlalchemy import or_, and_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from ...utils import converters
from sqlalchemy.exc import IntegrityError as sqlIntegrityError



class AnnualValue(Base):
    __tablename__ = 'annualvalues'

    annualValueId = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('companies.companyId'))
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    transportAidPeriod = Column(Integer)
    uvtValue = Column(DECIMAL(14, 2), default=0.0)
    legalMinimumSalary = Column(DECIMAL(14, 2), default=0.0)
    transportAid = Column(DECIMAL(14, 2))
    exemptIncome = Column(DECIMAL(7, 4), default=0.0)
    epsEmployer = Column(DECIMAL(7, 4), default=0.0)
    afpEmployer = Column(DECIMAL(7, 4), default=0.0)
    minimumPercentageContributions = Column(DECIMAL(7, 4), default=0.0)
    basePercentageLaw1527 = Column(DECIMAL(7, 4), default=0.0)
    withholdingIVARate = Column(DECIMAL(7, 4), default=0.0)
    fspWorker = Column(DECIMAL(7, 4), default=0.0)
    layoffProvision = Column(DECIMAL(7, 4), default=0.0)
    vacationProvision = Column(DECIMAL(7, 4), default=0.0)
    bonusProvision = Column(DECIMAL(7, 4), default=0.0)
    layoffInterestProvision = Column(DECIMAL(7, 4), default=0.0)
    ipc = Column(DECIMAL(5, 3), default=0.0)
    afpHighRiskEmployer = Column(DECIMAL(7,4), default=0.0)
    ccfEmployer = Column(DECIMAL(7, 4), default=0.0)
    icbfEmployer = Column(DECIMAL(7, 4), default=0.0)
    senaEmployer = Column(DECIMAL(7, 4), default=0.0)
    epsWorker = Column(DECIMAL(7, 4), default=0.0)
    afpWorker = Column(DECIMAL(7, 4), default=0.0)
    year = Column(String(4))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    payrollContribution = Column(Integer)
    transportAidTopSML = Column(SmallInteger)
    epsWorkerTopSML = Column(SmallInteger)
    afpWorkerTopSML = Column(SmallInteger)
    fspWorkerFromSML = Column(SmallInteger)
    arpWorkerTopSML = Column(SmallInteger)
    exemptIncomeUVT = Column(SmallInteger)
    senaFromSML = Column(SmallInteger)

    company = relationship("Company", lazy='joined', innerjoin=True)

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'annualValueId' in data:
            self.annualValueId = data["annualValueId"]
        if 'companyId' in data:
            self.companyId = data["companyId"]
        if 'creationDate' in data:
            self.creationDate = data["creationDate"]
        if 'updateDate' in data:
            self.updateDate = data["updateDate"]
        if 'isDeleted' in data:
            self.isDeleted = data["isDeleted"]
        if 'transportAidPeriod' in data:
            self.transportAidPeriod = data["transportAidPeriod"]
        if 'uvtValue' in data:
            self.uvtValue = data["uvtValue"]
        if 'legalMinimumSalary' in data:
            self.legalMinimumSalary = data["legalMinimumSalary"]
        if 'transportAid' in data:
            self.transportAid = data["transportAid"]
        if 'exemptIncome' in data:
            self.exemptIncome = data["exemptIncome"]
        if 'epsEmployer' in data:
            self.epsEmployer = data["epsEmployer"]
        if 'afpEmployer' in data:
            self.afpEmployer = data["afpEmployer"]
        if 'minimumPercentageContributions' in data:
            self.minimumPercentageContributions = data["minimumPercentageContributions"]
        if 'basePercentageLaw1527' in data:
            self.basePercentageLaw1527 = data["basePercentageLaw1527"]
        if 'withholdingIVARate' in data:
            self.withholdingIVARate = data["withholdingIVARate"]
        if 'fspWorker' in data:
            self.fspWorker = data["fspWorker"]
        if 'layoffProvision' in data:
            self.layoffProvision = data["layoffProvision"]
        if 'vacationProvision' in data:
            self.vacationProvision = data["vacationProvision"]
        if 'bonusProvision' in data:
            self.bonusProvision = data["bonusProvision"]
        if 'layoffInterestProvision' in data:
            self.layoffInterestProvision = data["layoffInterestProvision"]
        if 'ipc' in data:
            self.ipc = data["ipc"]
        if 'afpHighRiskEmployer' in data:
            self.afpHighRiskEmployer = data["afpHighRiskEmployer"]
        if 'ccfEmployer' in data:
            self.ccfEmployer = data["ccfEmployer"]
        if 'icbfEmployer' in data:
            self.icbfEmployer = data["icbfEmployer"]
        if 'senaEmployer' in data:
            self.senaEmployer = data["senaEmployer"]
        if 'epsWorker' in data:
            self.epsWorker = data["epsWorker"]
        if 'afpWorker' in data:
            self.afpWorker = data["afpWorker"]
        if 'year' in data:
            self.year = data["year"]
        if 'createdBy' in data:
            self.createdBy = data["createdBy"]
        if 'updateBy' in data:
            self.updateBy = data["updateBy"]
        if 'payrollContribution' in data:
            self.payrollContribution = data["payrollContribution"]
        if 'transportAidTopSML' in data:
            self.transportAidTopSML = data["transportAidTopSML"]
        if 'epsWorkerTopSML' in data:
            self.epsWorkerTopSML = data["epsWorkerTopSML"]
        if 'afpWorkerTopSML' in data:
            self.afpWorkerTopSML = data["afpWorkerTopSML"]
        if 'fspWorkerFromSML' in data:
            self.fspWorkerFromSML = data["fspWorkerFromSML"]
        if 'arpWorkerTopSML' in data:
            self.arpWorkerTopSML = data["arpWorkerTopSML"]
        if 'exemptIncomeUVT' in data:
            self.exemptIncomeUVT = data["exemptIncomeUVT"]
        if 'senaFromSML' in data:
            self.senaFromSML = data["senaFromSML"]

        return self

    def export_data(self):
        return {
            'annualValueId': self.annualValueId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'transportAidPeriod': self.transportAidPeriod,
            'uvtValue': self.uvtValue,
            'legalMinimumSalary': self.legalMinimumSalary,
            'transportAid': self.transportAid,
            'exemptIncome': self.exemptIncome,
            'epsEmployer': self.epsEmployer,
            'afpEmployer': self.afpEmployer,
            'minimumPercentageContributions': self.minimumPercentageContributions,
            'basePercentageLaw1527': self.basePercentageLaw1527,
            'withholdingIVARate': self.withholdingIVARate,
            'fspWorker': self.fspWorker,
            'layoffProvision': self.layoffProvision,
            'vacationProvision': self.vacationProvision,
            'bonusProvision': self.bonusProvision,
            'layoffInterestProvision': self.layoffInterestProvision,
            'ipc': self.ipc,
            'afpHighRiskEmployer': self.afpHighRiskEmployer,
            'ccfEmployer': self.ccfEmployer,
            'icbfEmployer': self.icbfEmployer,
            'senaEmployer': self.senaEmployer,
            'epsWorker': self.epsWorker,
            'afpWorker': self.afpWorker,
            'year': self.year,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'payrollContribution': self.payrollContribution,
            'transportAidTopSML': self.transportAidTopSML,
            'epsWorkerTopSML': self.epsWorkerTopSML,
            'afpWorkerTopSML': self.afpWorkerTopSML,
            'fspWorkerFromSML': self.fspWorkerFromSML,
            'arpWorkerTopSML': self.arpWorkerTopSML,
            'exemptIncomeUVT': self.exemptIncomeUVT,
            'senaFromSML': self.senaFromSML,
        }


    @staticmethod
    def search_values(**kwargs):
        """
        Search annual values according to params
        :param kwargs:
        :return:
        """
        simple = kwargs.get("simple")
        year = kwargs.get("year")
        companyId = kwargs.get("companyId")
        by_param = kwargs.get("by_param")
        code = kwargs.get("code")
        search = kwargs.get('search')
        words = kwargs.get('words')
        annual_values = [annual_val.export_data() for annual_val in
                         session.query(AnnualValue).filter(AnnualValue.year == year,
                                                           AnnualValue.companyId == companyId).all()]

        return jsonify(data=annual_values)

