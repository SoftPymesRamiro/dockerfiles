from ... import Base, Session
from sqlalchemy import Integer, ForeignKey, String, Column, DECIMAL, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship


class PayrollConcept(Base):
    __tablename__ = 'payrollconcepts'

    payrollConceptId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    thirdId = Column(ForeignKey(u'thirdpartys.thirdPartyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    salaryBase = Column(Integer)
    transportAidBase = Column(Integer)
    vacationBase = Column(Integer)
    epsBase = Column(Integer)
    afpBase = Column(Integer)
    arpBase = Column(Integer)
    typePayrollConcept = Column(Integer)
    redistributable = Column(Integer)
    ccfBase = Column(Integer)
    icbfBase = Column(Integer)
    senaBase = Column(Integer)
    withholdingTaxBase = Column(Integer)
    modify = Column(Integer)
    isDeleted = Column(Integer)
    maxValue = Column(DECIMAL(16, 2), default=0.0)
    factor = Column(DECIMAL(8, 4), default=0.0)
    salaryPercentBase = Column(DECIMAL(6, 2), default=0.0)
    transportAidPercentBase = Column(DECIMAL(6, 2), default=0.0)
    vacationPercentBase = Column(DECIMAL(6, 2), default=0.0)
    epsPercentBase = Column(DECIMAL(6, 2), default=0.0)
    afpPercentBase = Column(DECIMAL(6, 2), default=0.0)
    arpPercentBase = Column(DECIMAL(6, 2), default=0.0)
    ccfPercentBase = Column(DECIMAL(6, 2), default=0.0)
    icbfPercentBase = Column(DECIMAL(6, 2), default=0.0)
    senaPercentBase = Column(DECIMAL(6, 2), default=0.0)
    withholdingTaxPercentBase = Column(DECIMAL(6, 2), default=0.0)
    code = Column(String(4))
    name = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    unity = Column(Integer)

    company = relationship(u'Company')
    puc = relationship(u'PUC', foreign_keys=[pucId])
    thirdparty = relationship(u'ThirdParty')

    def export_data(self):
        return {
            'payrollConceptId': self.payrollConceptId,
            'companyId': self.companyId,
            'pucId': self.pucId,
            'puc': self.puc.export_data_name_and_id() if self.puc else None,
            'thirdId': self.thirdId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'salaryBase': self.salaryBase,
            'transportAidBase': self.transportAidBase,
            'vacationBase': self.vacationBase,
            'epsBase': self.epsBase,
            'afpBase': self.afpBase,
            'arpBase': self.arpBase,
            'typePayrollConcept': self.typePayrollConcept,
            'redistributable': self.redistributable,
            'ccfBase': self.ccfBase,
            'icbfBase': self.icbfBase,
            'senaBase': self.senaBase,
            'withholdingTaxBase': self.withholdingTaxBase,
            'modify': self.modify,
            'isDeleted': self.isDeleted,
            'maxValue': self.maxValue,
            'factor': self.factor,
            'salaryPercentBase': self.salaryPercentBase,
            'transportAidPercentBase': self.transportAidPercentBase,
            'vacationPercentBase': self.vacationPercentBase,
            'epsPercentBase': self.epsPercentBase,
            'afpPercentBase': self.afpPercentBase,
            'arpPercentBase': self.arpPercentBase,
            'ccfPercentBase': self.ccfPercentBase,
            'icbfPercentBase': self.icbfPercentBase,
            'senaPercentBase': self.senaPercentBase,
            'withholdingTaxPercentBase': self.withholdingTaxPercentBase,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'unity': self.unity
        }

    def import_data(self, data):
        """
        :param data: json company with branch and partners
        :return: return an company object from json
        """
        if 'payrollConceptId' in data:
            self.payrollConceptId = data['payrollConceptId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'thirdId' in data:
            self.thirdId = data['thirdId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'salaryBase' in data:
            self.salaryBase = data['salaryBase']
        if 'transportAidBase' in data:
            self.transportAidBase = data['transportAidBase']
        if 'vacationBase' in data:
            self.vacationBase = data['vacationBase']
        if 'epsBase' in data:
            self.epsBase = data['epsBase']
        if 'afpBase' in data:
            self.afpBase = data['afpBase']
        if 'arpBase' in data:
            self.arpBase = data['arpBase']
        if 'typePayrollConcept' in data:
            self.typePayrollConcept = data['typePayrollConcept']
        if 'redistributable' in data:
            self.redistributable = data['redistributable']
        if 'ccfBase' in data:
            self.ccfBase = data['ccfBase']
        if 'icbfBase' in data:
            self.icbfBase = data['icbfBase']
        if 'senaBase' in data:
            self.senaBase = data['senaBase']
        if 'withholdingTaxBase' in data:
            self.withholdingTaxBase = data['withholdingTaxBase']
        if 'modify' in data:
            self.modify = data['modify']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'maxValue' in data:
            self.maxValue = data['maxValue']
        if 'factor' in data:
            self.factor = data['factor']
        if 'salaryPercentBase' in data:
            self.salaryPercentBase = data['salaryPercentBase']
        if 'transportAidPercentBase' in data:
            self.transportAidPercentBase = data['transportAidPercentBase']
        if 'vacationPercentBase' in data:
            self.vacationPercentBase = data['vacationPercentBase']
        if 'epsPercentBase' in data:
            self.epsPercentBase = data['epsPercentBase']
        if 'afpPercentBase' in data:
            self.afpPercentBase = data['afpPercentBase']
        if 'arpPercentBase' in data:
            self.arpPercentBase = data['arpPercentBase']
        if 'ccfPercentBase' in data:
            self.ccfPercentBase = data['ccfPercentBase']
        if 'icbfPercentBase' in data:
            self.icbfPercentBase = data['icbfPercentBase']
        if 'senaPercentBase' in data:
            self.senaPercentBase = data['senaPercentBase']
        if 'withholdingTaxPercentBase' in data:
            self.withholdingTaxPercentBase = data['withholdingTaxPercentBase']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'unity' in data:
            self.unity = data['unity']

        return self