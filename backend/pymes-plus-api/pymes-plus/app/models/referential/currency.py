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
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Currency(Base):
    """

    """
    __tablename__ = 'currencies'
    currencyId = Column(Integer, primary_key=True)
    code = Column(String(3))
    name = Column(String(50))
    symbol = Column(String(3))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        """
        Allow export data in country object
        :return: country object in json format
        """
        return {
            'currencyId': self.currencyId,
            'code': self.code,
            'name': self.name,
            'symbol': self.symbol,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'updateDate': self.updateDate
        }

    @staticmethod
    def export_data_simple(data):
        """
        Allow export data in short form
        :param data: currency information to map by export
        :return: currency object
        """
        return {
            'currencyId': data.currencyId,
            'code': data.code,
            'name': data.name,
            'symbol': data.symbol
        }

    def import_data(self, data):
        """
        Allow create new currency from data
        :param data: information by new currency
        :raise: KeyError
        :exception: An error occurs when key in data no is set
        :return: currency object
        """
        try:
            if 'currencyId' in data:
                self.currencyId = data['currencyId']
            if 'code' in data:
                self.code = data['code']
            if 'name' in data:
                self.name = data['name']
            if 'symbol' in data:
                self.symbol = data['symbol']
            if "createdBy" in data:
                self.createdBy = data["createdBy"]
            if "creationDate" in data:
                self.creationDate = data["creationDate"]
            if "updateBy" in data:
                self.updateBy = data["updateBy"]
            if "updateDate" in data:
                self.updateDate = data["updateDate"]
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
        except KeyError as e:
            raise ValidationError("Invalid currencies: missing " + e.args[0])
        return self

    @staticmethod
    def get_currencies():
        """
        Allow obtain all currencies
        :return: JSON object with currency data
        """
        currency = jsonify(data=[currency.export_data() for currency in session.query(Currency).order_by(Currency.code).all()])
        return currency

    @staticmethod
    def get_currency(currency_id):
        """
        Allow obtain currency according to identifier
        :param currency_id: currency identifier to change
        :return: currency object
        """
        currency = session.query(Currency).get(currency_id)
        if currency is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        currency = currency.export_data()
        response = jsonify(currency)
        return response

    @staticmethod
    def get_currency_by_search(**kwargs):
        """
        Allow search currency according request params
        :param kwargs: request parameters
        :return: An JSON object with currencies found
        """
        search = kwargs.get("search")
        words = kwargs.get("words")
        simple = kwargs.get("simple")
        to_search = kwargs.get("to_search")

        currencies = []

        if simple:
            currencies = [Currency.export_data_simple(coin)
                          for coin in session.query(Currency.name, Currency.currencyId,
                                                  Currency.symbol, Currency.code).all()]

        elif search or search == "":
            currencies = [coin.export_data()
                          for coin in session.query(Currency).filter(
                          or_(
                              True if search == '' else None,
                              or_(*[Currency.name.like('%{0}%'.format(s)) for s in words]),
                              or_(*[Currency.code.like('%{0}%'.format(s)) for s in words]),
                              or_(*[Currency.symbol.like('%{0}%'.format(s)) for s in words])
                          )).order_by(Currency.name)]
        elif to_search:
            currencies = [Currency.export_data_simple(coin)
                          for coin
                          in session.query(Currency)
                                    .filter(or_(
                                                True if search == "" else None,
                                                or_(*[Currency.symbol.like('%{0}%'.format(s))
                                                      for s in words]),
                                                or_(*[Currency.name.like('%{0}%'.format(s))
                                                      for s in words])
                                            ))]

        response = jsonify(data=currencies)
        return response

    @staticmethod
    def post_currency(data):
        """
        Allow create currencies from data
        :param data: informatioon by new curency
        :raise: KeyError
        :exception: An error occurs when key i data is not set
        :return: JSON object with currency identifier
        """
        currency = Currency()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            # TODO: Colocar el nombre de autenticacion
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            currency.import_data(data)

            session.add(currency)
            session.commit()
            response = jsonify({'currencyId': currency.currencyId})
        except KeyError as e:
            raise ValidationError('Invalid currency: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_currency(currency_id):
        """
        Allow delete an currency for to give currency identifier
        :param currency_id: currency identifier to delete
        :return: status code and result
        """
        currency = session.query(Currency).get(currency_id)
        if currency is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(currency)
        try:
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
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_currency(currency_id, data):
        """
        Allow update a currency for to give currency identifier
        :param currency_id: currency identifier to update
        :param data: information de currency toi change
        :return: status core and result
        """
        if currency_id != data['currencyId']:
            response = jsonify({'error': 'bad request', 'message': 'El item ya existe'})
            response.status_code = 400
            return response
        if not currency_exist(data['currencyId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        currency = session.query(Currency).get(currency_id)

        try:
            data['creationDate'] = currency.creationDate
            data['createdBy'] = currency.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            currency = currency.import_data(data)
            session.add(currency)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid currency: missing' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def currency_exist(currency_id):
    """
    Allow validate whether a curency exist according its identifier
    :param currency_id: currencty identifier
    :return: currency object
    """
    return session.query(Currency).filter(Currency.currencyId == currency_id).count()