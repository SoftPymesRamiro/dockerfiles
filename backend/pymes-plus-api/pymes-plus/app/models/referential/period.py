# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from math import ceil
from flask import jsonify,g
from ... import Base
from ... import session
from .sub_zones_1 import SubZone1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from ...utils import converters

class Period(Base):
    __tablename__ = 'periods'

    periodId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer, default=0)
    annualPercent = Column(DECIMAL(6, 3), default=0.0)
    dailyPercent = Column(DECIMAL(6, 3), default=0.0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    typePeriod = Column(String(2))
    initialDay = Column(TINYINT)
    finalDay = Column(TINYINT)

    company = relationship(u'Company')

    def export_data(self):
        """
            allow obtain data according to discount list
            :param  data
            :return zone in JSON object
        """
        return {
            'periodId': self.periodId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'annualPercent': self.annualPercent,
            'dailyPercent': self.dailyPercent,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'typePeriod': self.typePeriod,
            'initialDay': self.initialDay,
            'finalDay': self.finalDay
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'periodId'  in data:
            self.periodId = data['periodId']
        if 'companyId'  in data:
            self.companyId = data['companyId']
        if 'creationDate'  in data:
            self.creationDate = data['creationDate']
        if 'updateDate'  in data:
            self.updateDate = data['updateDate']
        if 'isDeleted'  in data:
            self.isDeleted = data['isDeleted']
        if 'annualPercent'  in data:
            self.annualPercent = data['annualPercent']
        if 'dailyPercent'  in data:
            self.dailyPercent = data['dailyPercent']
        if 'createdBy'  in data:
            self.createdBy = data['createdBy']
        if 'updateBy'  in data:
            self.updateBy = data['updateBy']
        if 'typePeriod'  in data:
            self.typePeriod = data['typePeriod']
        if 'initialDay'  in data:
            self.initialDay = data['initialDay']
        if 'finalDay'  in data:
            self.finalDay = data['finalDay']

        return self

    @staticmethod
    def get_periods():
        """
         Allow obtain all discount list
        :return: An JSON object, with array with discount list objects in JSON format
        """
        period_list = [Period.export_data(period_list)
                                      for period_list in session.query(Period)
                                .order_by(Period.finalDay).all()]
        period_list = jsonify(data=period_list)
        return period_list

    @staticmethod
    def get_periods_company(company_id):
        """
         Allow obtain all discount list
        :return: An JSON object, with array with discount list objects in JSON format
        """
        period_list = [Period.export_data(period_list)
                                      for period_list in session.query(Period)
                           .filter(Period.companyId==company_id)
                           .order_by(Period.finalDay).all()]
        period_list = jsonify(data=period_list)
        return period_list

    @staticmethod
    def get_period(period_id):
        """
            Allow obtain a period for to give a identifier
            :param period_id identifier by period
            :return period object in JSON format
        """
        period = session.query(Period).get(period_id)
        if period is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        period = period.export_data()
        response = jsonify(period)
        return response

    @staticmethod
    def get_period_bysearch(**kwargs):
        """
        Allow get period according to search request arguments
        :param kwargs: request params
        :return: an array with discount list objects in JSON format
        """
        response = jsonify({'code': 400, 'message': 'bad request'})
        response.status_code = 400
        return response


    @staticmethod
    def post_period(data):
        """
        Allow create a new period
        :param data
        :exception KeyError whether key fail in data
        :return status in JSON Object
        """
        for period in data:

            if 'periodId' in period:

                obj_period = session.query(Period).get(period['periodId'])

                period['creationDate'] = obj_period.creationDate
                period['createdBy'] = obj_period.createdBy
                period['updateDate'] = datetime.now()
                period['updateBy'] = g.user['name']

                obj_period.import_data(period)
                session.add(obj_period)

                try:
                    session.flush()
                except:
                    session.rollback()
                    raise
            else:

                obj_period = Period()

                period['creationDate'] = datetime.now()
                period['updateDate'] = datetime.now()
                period['createdBy'] = g.user['name']
                period['updateBy'] = g.user['name']

                obj_period.import_data(period)
                session.add(obj_period)

                try:
                    session.flush()
                except:
                    session.rollback()
                    raise

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            raise ValidationError('Invalid list_discount_list: missing' + e.args[0])
        return response


    @staticmethod
    def put_period(period_id, data):
        """
        Allow update a period according to its identifier
        :param period_id: identifier by period
        :param data: information by period
        :return: period object in JSON format
        """
        response = jsonify({'code': 400, 'message': 'bad request'})
        response.status_code = 400
        return response

    @staticmethod
    def delete_period(period_id):
        """
            Allow delete period accoding to identifier
            :param period_id identifier by period to delete
            :exception KeyError whether a key fail
            :return status code
        """
        period = session.query(Period).get(period_id)

        if period is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        try:
            session.delete(period)
            session.commit()

            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            session.rollback()
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)


def list_period_exist(name):
    """
    Allow obtain a list period accoridn to identifier
    :param period_id: identifier by list period
    :return: a array period objects in JSON format
    """
    pass