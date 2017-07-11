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
from ... import Base, session
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from pymysql.err import IntegrityError as sqlIntegrityError
from ...utils import converters
from sqlalchemy.dialects.mssql import DATE
from sqlalchemy import or_, and_, func

class ExchangeRate(Base):
    __tablename__ = 'exchangerates'

    exchangeRateId = Column(Integer, primary_key=True)
    currencyId = Column(ForeignKey(u'currencies.currencyId'), index=True)
    date = Column(DateTime, default=datetime.now())
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT, default=0)
    rate = Column(DECIMAL(9, 4), default=0.0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    currency = relationship(u'Currency', foreign_keys=[currencyId])

    def export_data(self):
        """

        :return:
        """
        return {
            'exchangeRateId': self.exchangeRateId,
            'currencyId': self.currencyId,
            'date': self.date,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'rate': self.rate,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'currency': None if self.currency is None else self.currency.export_data()
        }

    @staticmethod
    def export_data_simple(data):
        return {
            'exchangeRateId': data.exchangeRateId,
            'date': data.date,
            'rate': data.rate,
            'currency': None if data.currency is None else data.currency.export_data()
        }

    # @staticmethod
    # def export_data_currency(data):
    #     currency_data = None if data.currency is None else data.currency.export_data()
    #     if currency_data:
    #         currency_data['exchangeRateId'] = data.exchangeRateId
    #         currency_data['date'] = data.date
    #         currency_data['rate'] = data.rate
    #
    #     return currency_data


    def import_data(self, data):
        try:
            if "exchangeRateId" in data:
                self.exchangeRateId = data['exchangeRateId']
            if "currencyId" in data:
                self.currencyId = data['currencyId']
            if "date" in data:
                self.date = converters.convert_string_to_date(data['date'])
            if "creationDate" in data:
                self.creationDate = data['creationDate']
            if "updateDate" in data:
                self.updateDate = data['updateDate']
            if "isDeleted" in data:
                self.isDeleted = data['isDeleted']
            if "rate" in data:
                self.rate = data['rate']
            if "createdBy" in data:
                self.createdBy = data['createdBy']
            if "updateBy" in data:
                self.updateBy = data['updateBy']
        except KeyError as e:
            print(e)
        return self


    @staticmethod
    def search_exchange_rates(**kwargs):
        """

        :param kwargs:
        :return:
        """
        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")

        text_search = "" if search is None else str(search).strip()
        words = text_search.split(' ', 1) if text_search is not None else None
        list_exchange = [ExchangeRate.export_data_simple(exchange_rate)
               for exchange_rate in session.query(ExchangeRate).filter(True if search == '' else or_(
                or_(*[ExchangeRate.currency.code.like('%{0}%'.format(s)) for s in words]),
                or_(*[ExchangeRate.currency.name.like('%{0}%'.format(s)) for s in words]),
                or_(*[ExchangeRate.currency.symbol.like('%{0}%'.format(s)) for s in words]),
            ))]

        response = jsonify(data=list_exchange)


    @staticmethod
    def get_all_exchange_rates():
        list_exchange = [ExchangeRate.export_data(ex)
                         for ex in session.query(ExchangeRate)
                             .order_by(ExchangeRate.date.desc())]

        response = []
        if list_exchange:
            response = jsonify(data=list_exchange)

        return response

    @staticmethod
    def get_currency_rate(**kwargs):
        """
        Allow get current tax by currency id
        :param kwarg:
        :return:
        """
        currency_date = kwargs.get('currency_date')
        currency_id = kwargs.get('currency_id')

        exchange_rate = session.query(ExchangeRate) \
                .filter(func.cast(ExchangeRate.date, DATE) == currency_date,
                        ExchangeRate.currencyId ==currency_id).first()

        if exchange_rate is None:
            response = {'rate': 0, 'currency': None}
            return response

        exchange_rate = exchange_rate.export_data()
        return exchange_rate


    @staticmethod
    def get_exchange_rate(exchange_rate_id):
        exchange_rate = session.query(ExchangeRate) \
                .get(exchange_rate_id)

        if exchange_rate is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        exchange_rate = exchange_rate.export_data()
        response = jsonify(exchange_rate)
        return response


    @staticmethod
    def post_exchange_rate(data):
        """
            Allow create a new exchange_rate
            :param data
            :exception KeyError whether key fail in data
            :return status in JSON Object
        """
        exchange_rates = ExchangeRate()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            exchange_rates.import_data(data)

            session.add(exchange_rates)
            session.commit()
            response = jsonify({'exchangeRateId': exchange_rates.exchangeRateId})
        except KeyError as e:
            raise ValidationError('Invalid list_exchange_rates: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def put_exchange_rate(exchange_rate_id, data):
        """
        Allow update a exchange_rate according to its identifier
        :param exchange_rate_id: identifier by exchange_rate
        :param data: informtion by exchange_rate
        :return: exchange_rate object in JSON format
        """
        if exchange_rate_id != data['exchangeRateId']:
            response = jsonify({'error': 'bad request', 'message': 'La marca ya existe'})
            response.status_code = 400
            return response

        list_exchange_rates = session.query(ExchangeRate).get(exchange_rate_id)

        try:
            data['creationDate'] = list_exchange_rates.creationDate
            data['createdBy'] = list_exchange_rates.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            list_exchange_rates = list_exchange_rates.import_data(data)
            session.add(list_exchange_rates)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid list_exchange_rates: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def delete_exchange_rate(exchange_rate_id):
        """
            Allow delete exchange_rate accoding to identifier
            :param exchange_rate_id identifier by exchange_rate to delete
            :exception KeyError whether a key fail
            :return status code
        """
        list_exchange_rates = session.query(ExchangeRate).get(exchange_rate_id)
        if list_exchange_rates is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(list_exchange_rates)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

