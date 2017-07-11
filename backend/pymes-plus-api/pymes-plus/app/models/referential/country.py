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
from flask import jsonify, g
from ... import Base
from .department import Department
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Country(Base):
    """

    """
    __tablename__ = 'countries'

    countryId = Column(Integer, primary_key=True, nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(3))
    name = Column(String(50))
    dianCode = Column(String(3))
    indicative = Column(String(3))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    departments = relationship("Department",
                               primaryjoin=countryId == Department.countryId,
                               cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
        Allow obtain country from data
        :param data: infotmation to export
        :return: country object in JSOn format
        """
        return {
            'countryId': data.countryId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'code': data.code,
            'name': data.name,
            'dianCode': data.dianCode,
            'indicative': data.indicative,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'departments': [] if data.departments is None or len(data.departments) == 0
            else [Department.export_data(dep) for dep in data.departments]
        }

    def import_data(self, data):
        """
        Allow import country from data
        :param data: information by new country
        :raise: KeyError
        :exception: An error occurs when an key in data si not set
        :return: country object in JSON format
        """
        if 'countryId' in data:
            self.countryId = data['countryId']

        self.code = data['code']
        self.name = data['name']
        self.indicative = data['indicative']

        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'dianCode' in data:
            self.dianCode = data['dianCode']
        if'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def get_countries():
        """
        Allow obtain all countries
        :return: JSON object with contry array, ordered by code
        """
        country = jsonify(data=[Country.export_data(country) for country in session.query(Country).order_by(Country.code).all()])
        return country

    @staticmethod
    def get_country(country_id):
        """
        Allow obtain a country according to identifier
        :param country_id: country identifier
        :return: JSON object whit country object
        """
        country = session.query(Country).get(country_id)
        if country is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        country = country.export_data(country)
        response = jsonify(country)
        return response

    @staticmethod
    def post_country(data):
        """
        Allow create a country
        :param data: information by change country
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:
        """
        country = Country()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        if country_exist_by_code(data['code']):
            response = jsonify({'code': 400, 'message': 'country code already exits'})
            response.status_code = 400
            return response

        country.import_data(data)
        session.add(country)


        try:
            session.commit()
            response = jsonify({'countryId': country.countryId})
        except KeyError as e:
            raise ValidationError('Invalid country: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_country(country_id):
        """
        Allow delete a country according to identifier
        :param country_id: country identifier to eliminate
        :return:
        """
        country = session.query(Country).get(country_id)
        if country is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(country)
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
    def put_country(country_id, data):
        """
        Allow update an country identifier
        :param country_id: country identifier to update
        :param data:  information to change country data
        :return:
        """
        if country_id != data['countryId']:
            response = jsonify({'error': 'bad request', 'message': 'El pais ya existe'})
            response.status_code = 400
            return response

        if not country_exist(data['countryId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        country = session.query(Country).get(country_id)

        try:
            data['creationDate'] = country.creationDate
            data['createdBy'] = country.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            country = country.import_data(data)
            session.add(country)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid country: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def country_exist(country_id):
    """
    Allow validate whether country exist afor to give country identifier
    :param country_id: coutnry identifier to seek
    :return: country object found
    """
    return session.query(Country).filter(Country.countryId == country_id).count()

def country_exist_by_code(code):
    """
    Allow validate whether country exist afor to give country identifier
    :param country_id: coutnry identifier to seek
    :return: country object found
    """
    return session.query(Country).filter(Country.code == code ).count()


