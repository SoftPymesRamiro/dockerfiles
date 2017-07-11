# coding=utf-8

from datetime import datetime
from flask import jsonify,g
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_, Table
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from sqlalchemy.orm import relationship
from math import ceil
from .puc import PUC
from ...exceptions import ValidationError
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError


economicactivitypuc = Table(
    'economicactivitypuc', Base.metadata,

    Column('economicActivityId', ForeignKey(u'economicactivities.economicActivityId'), primary_key=True, nullable=False),
    Column('pucId', ForeignKey(u'puc.pucId'), primary_key=True, nullable=False, index=True)
)


class EconomicActivity(Base):
    __tablename__ = 'economicactivities'

    economicActivityId = Column(Integer, primary_key=True, nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    percentage = Column(DECIMAL(4, 2), default=0.0)
    code = Column(String(3))
    name = Column(String(100))
    createdBy = Column(DateTime, default=datetime.now())
    updateBy = Column(DateTime, default=datetime.now())

    puc = relationship(u'PUC',
                       secondary=economicactivitypuc,
                       primaryjoin=economicActivityId == economicactivitypuc.c.economicActivityId,
                       secondaryjoin=PUC.pucId == economicactivitypuc.c.pucId,
                       lazy="dynamic",
                       )

    def export_data(self):
        """

        :return:
        """
        return {
            'economicActivityId': self.economicActivityId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'percentage': self.percentage,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def export_data_simple(self):
        """

        :return:
        """
        return {
            'economicActivityId': self.economicActivityId,
            'name': self.name.upper() + " " + str(self.percentage),
            'code': self.code
        }

    @staticmethod
    def export_data_simple_search(data, company_id):
        """

        :return:
        """
        puc = None if data.puc is None \
            else data.puc.filter(PUC.companyId == company_id).first()
        return {
            "economicActivityId": data.economicActivityId,
            'code': data.code,
            'name': data.name,
            'percentage': data.percentage,
            'puc': {
                "pucId": puc.pucId,
                "companyId": puc.companyId,
                "account": '{0}{1}{2}{3}{4}'.format(puc.pucClass,
                                            puc.subAccount,
                                            puc.pucSubClass,
                                            puc.subAccount,
                                            puc.auxiliary1),
                "percentage": puc.percentage,
                "name": puc.name,
            },
        }

    @staticmethod
    def get_economic_activities():
        economic_activity = jsonify(data=[economic_activity.export_data()
                                          for economic_activity in session.query(EconomicActivity)
                                    .order_by(EconomicActivity.code).all()])
        return economic_activity

    @staticmethod
    def get_economic_activity(economic_activity_id):
        economic_activity = session.query(EconomicActivity).get(economic_activity_id)
        if economic_activity is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        economic_activity = economic_activity.export_data()
        response = jsonify(economic_activity)
        return response

    @staticmethod
    def get_economic_activities_by_search(**kwargs):
        search = kwargs.get('search')
        words = kwargs.get('words')
        simple = kwargs.get('simple')
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')

        economic_activity_id = kwargs.get('economic_activity_id')
        company_id = kwargs.get('company_id')

        if simple is None and not economic_activity_id and not company_id:
            economic_activity = [economic_activity.export_data()
                                 for economic_activity in session.query(EconomicActivity).filter(
                                    or_(or_(*[EconomicActivity.name.contains(word) for word in words]),
                                    or_(*[EconomicActivity.code.contains(word) for word in words]))
            ).order_by(EconomicActivity.code)]

            response = jsonify(data=economic_activity)
            return response

        if simple is not None:
            economic_activity = [economic_activity.export_data_simple()
                                 for economic_activity in session.query(EconomicActivity).filter(
                        or_(
                            True if search == '' else None,
                            or_(*[EconomicActivity.name.contains(word) for word in words]),
                            or_(*[EconomicActivity.code.contains(word) for word in words])
                        )).order_by(EconomicActivity.code)
                         .limit(page_size)
                         .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(EconomicActivity).filter(
                    or_(
                        True if search == '' else None,
                        or_(*[EconomicActivity.name.contains(word) for word in words]),
                        or_(*[EconomicActivity.code.contains(word) for word in words])
                    )).count()

            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'economicActivities': economic_activity,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        if economic_activity_id and company_id:
            economic_activity = [EconomicActivity.export_data_simple_search(economic_activity, company_id)
                                 for economic_activity in session.query(EconomicActivity)
                                     .filter(and_(EconomicActivity.economicActivityId == economic_activity_id))]

            response = jsonify(data=economic_activity)
            return response


