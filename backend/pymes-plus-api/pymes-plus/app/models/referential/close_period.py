# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from datetime import datetime, date
from ...utils.converters import convert_string_to_date
from ... import Base
from ... import session
from ...utils.converters import convert_string_to_date
from flask import jsonify, g
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.dialects.mysql import DATE
from sqlalchemy.orm import relationship
from sqlalchemy import or_, and_, func, extract
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
import copy

class ClosePeriod(Base):
    """

    """
    __tablename__ = 'closeperiods'

    closeDayId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime)
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    dayClosed = Column(DATE, default=date.today())

    branch = relationship(u'Branch')

    @staticmethod
    def export_data(data):
        """
        Allow export data by closed-periods

        :return: return a closed period in JSON format
        """
        return {
            'closeDayId': data.closeDayId,
            'branchId': data.branchId,
            'creationDate': str(data.creationDate),
            'updateDate': str(data.updateDate),
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'dayClosed': str(data.dayClosed),
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        # try:
        if 'closeDayId' in data:
            self.closeDayId = data['closeDayId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'dayClosed' in data:
            self.dayClosed = data['dayClosed']
        # except Exception as e:
        #     raise e
        return self


    @staticmethod
    def get_close_periods():
        """
         Allow obtain all close periods
        :return: An JSON object, with array with closeperiods objects in JSON format
        """
        close_periods = jsonify(data=[ClosePeriod.export_data(city)
                             for city in session.query(ClosePeriod).all()])

        return close_periods

    @staticmethod
    def get_close_period_by_search(**kwargs):
        """

        :param kwargs:
        :return:
        """
        day = kwargs.get('day')
        year = kwargs.get('year')
        branch_id = kwargs.get('branch_id')

        if day:
            if not "/" in day:
                day_parsed = convert_string_to_date(day)
            else:
                day_parsed = datetime.strptime(day, "%d/%m/%Y")

            close_day = session.query(ClosePeriod).filter(ClosePeriod.branchId == branch_id,
                                                          ClosePeriod.dayClosed == day_parsed.date()).count() == 1

            response = jsonify(close_day=close_day)
            return response

        if year:
            if not "/" in year:
                year_parsed = convert_string_to_date(year)
            else:
                year_parsed = datetime.strptime(year, "%d/%m/%Y")

            close_days = [ClosePeriod.export_data(close_days)
                                       for close_days in session.query(ClosePeriod)
                                 .filter(ClosePeriod.branchId == branch_id,
                                         extract('year', ClosePeriod.dayClosed)== year_parsed.year)
                                 .all()]

            close_days = jsonify(data=close_days)
            return close_days

    @staticmethod
    def post_close_periods(data):
        close_periods = session.query(ClosePeriod)\
                              .filter(ClosePeriod.branchId == data['branchId'],
                                      ClosePeriod.dayClosed.isnot(None),
                                      extract('year', ClosePeriod.dayClosed) == data['year']).all()

        if close_periods is None or close_periods is []:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        try:
            [session.delete(cls_del) for cls_del in close_periods]
            # for cls_del in close_periods:
            #     session.delete(cls_del)
            #     session.flush()
            session.flush()
            close_period = ClosePeriod()
            close_period.branchId = data['branchId']
            close_period.createdBy = g.user['name']
            close_period.creationDate = datetime.now()
            close_period.updateBy = g.user['name']
            close_period.updateDate = datetime.now()

            for day in data['january']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['february']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['march']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['april']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['may']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['june']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['july']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['august']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['september']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['october']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            for day in data['november']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))
            for day in data['december']:
                close_period.dayClosed = convert_string_to_date(day)
                session.add(copy.deepcopy(close_period))

            session.commit()
            response = jsonify({"ok": "ok"})
            return response

        except KeyError as e:
            session.rollback()
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)



