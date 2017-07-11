from datetime import datetime
from ... import Base
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from ...utils import converters
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from ...exceptions import InternalServerError, ValidationError


class EconomicActivityPercentage(Base):
    __tablename__ = 'economicactivitypercentages'

    economicActivityPercentageId = Column(Integer, primary_key=True)
    economicActivityId = Column(ForeignKey(u'economicactivities.economicActivityId'), index=True)
    percentageDate = Column(DateTime, default=datetime.now())
    percentage = Column(DECIMAL(4, 2), default=0.0)

    economicActivity = relationship(u'EconomicActivity')

    @staticmethod
    def get_percentage(branch_id, document_date):
        try:
            from .. import Branch
            date_cree = datetime(year=2013, month=5, day=1)
            if not (branch_id or document_date):
                raise ValidationError('Faltan los parametros de sucursal y fecha de documento')
            if converters.convert_string_to_date(document_date) < date_cree:
                return 0
            economic_id = session.query(Branch.economicActivityId).filter(Branch.branchId == branch_id).first()

            sub_query = session.query(func.max(EconomicActivityPercentage.percentage).label('percentage'))\
                .filter(EconomicActivityPercentage.economicActivityId == economic_id[0],
                        EconomicActivityPercentage.percentageDate <= document_date)

            percentage = session.query(EconomicActivityPercentage.percentage)\
                .filter(EconomicActivityPercentage.economicActivityId == economic_id[0],
                        EconomicActivityPercentage.percentage.in_(sub_query)).all()
            if not percentage:
                branch = session.query(Branch).filter(Branch.branchId == branch_id).first()
                return branch.withholdingCREEPUC.percentage

            return percentage[0][0]
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)