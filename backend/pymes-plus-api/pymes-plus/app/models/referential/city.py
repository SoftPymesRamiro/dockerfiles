# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
from werkzeug import _internal

__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from datetime import datetime
from flask import jsonify,g
from math import ceil
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class City(Base):
    __tablename__ = 'cities'

    cityId = Column(Integer, primary_key=True, nullable=False)
    departmentId = Column(Integer, ForeignKey('departments.departmentId'))
    department = relationship('Department', lazy='joined', innerjoin=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(3))
    name = Column(String(50))
    indicative = Column(String(3))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    @staticmethod
    def export_data(data):
        """
        Allow export data of city
        :param data: input data
        :return: city in JSON format
        """
        return {
            'cityId': data.cityId,
            'departmentId': data.departmentId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'code': data.code,
            'name': data.name,
            'indicative': data.indicative,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy
        }

    def import_data(self, data):
        """
        Allow create a city object from data
        :param data: information by a new city
        :exception: KeyError an error occurs when a key in data is not set
        :return: an city object in JSON format
        """
        # try:
        if 'cityId' in data:
            self.cityId = data['cityId']
        self.departmentId = data['departmentId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        self.code = data['code']
        self.name = data['name']
        if 'indicative' in data:
            self.indicative = data['indicative']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        # except KeyError as e:
        #     raise ValidationError('Invalid cities: missing ' + e.args[0])
        return self

    @staticmethod
    def export_simple(data):
        """
        Allow export short data according to input
        :param data: information to export in short form
        :return: a cityn object in JSON format
        """
        return {
            'cityId': data.cityId,
            'name': data.name,
            'departmentId': data.departmentId,
            'indicative': data.indicative
        }

    @staticmethod
    def export_to_paginate(data):
        """
        Allow export data in groups by paginate in views
        :param data: information to paginate
        :return: a city object in JSON format
        """
        return {
            'cityId': data.cityId,
            'name': '{0}{1}{2}'.format(
                    data.name,
                    '' if data.department is None
                    else ' - {0}'.format(data.department.name),
                    '' if data.department is None and data.department.country is None
                    else ' - {0}'.format(data.department.country.name)),
            'code': data.code,
            'cityIndicative': data.indicative,
            'countryIndicative': '' if data.department.country is None else data.department.country.indicative
        }

    @staticmethod
    def get_cities():
        """
         Allow obtain all cities
        :return: An JSON object, with array with city objects in JSON format
        """
        city = jsonify(data=[City.export_data(city) for city in session.query(City).order_by(City.code).all()])
        return city

    @staticmethod
    def get_city(city_id):
        """
        Allow obtain a city for to give identifier
        :param city_id: identiifer by a city
        :return: a city object in JSON format
        """
        city = session.query(City).get(city_id)
        if city is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        city = City.export_data(city)
        response = jsonify(city)
        return response

    @staticmethod
    def get_cites_by_search(**kwargs):
        """
        Allow get city accoridin to search request arguments
        :param kwargs: request params
        :return: an array with city objects in JSON format
        """
        city_list = []
        simple = kwargs.get('simple')
        city_id = kwargs.get('city_id')
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')
        search = kwargs.get('search')
        words = kwargs.get('words')

        if simple:
            city = session.query(City.cityId,
                                 City.departmentId,
                                 City.name).filter(City.cityId == city_id).first()
            if city is None:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404
                return response
            city = city.export_simple(city)
            return jsonify(city)

        elif search:
            city_list = [City.export_to_paginate(city)
                         for city in session.query(City)
                             .filter(or_(
                                       True if search == '' else None,
                                       or_(*[City.name.like('%{0}%'.format(s)) for s in words]),
                                       ))
                             .limit(page_size)
                             .offset((int(page_number) -1) * int(page_size))
                         ]
            total_count = len(city_list)
            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'cities': city_list,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response

        response = jsonify(data=city_list)
        if len(city_list) == 0:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_city(data):
        """
        Allow update a city according to data information
        :param data: information by update city
        :exception; KeyErro -- An error occurs when a key in data is not set
        :return: status code and result
        """
        city = City()
        # if city_exists(data['city_id']) or city_exists_code(data['code']):
        #     response = jsonify({'error': 'Not Found', 'message': 'La ciudad ya existe'})
        #     response.status_code = 404
        #     return response
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            city.import_data(data)

            session.add(city)
            session.commit()
            response = jsonify({'cityId': city.cityId})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid city: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_city(city_id):
        """
        Allow delete a city according to identifier
        :param city_id: identifier by city to delete
        :return: dstatus code and result
        """
        city = session.query(City).get(city_id)
        if city is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(city)
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
    def put_city(city_id, data):
        """
        Allow update city according to ist identifier
        :param city_id: identifier by city
        :param data: information by update city
        :return: status coder and result
        """
        if city_id != data['cityId']:
            response = jsonify({'error': 'bad request', 'message': 'La ciudad ya existe'})
            response.status_code = 400
            return response
        if not city_exists(data['cityId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        city = session.query(City).get(city_id)

        try:
            data['creationDate'] = city.creationDate
            data['createdBy'] = city.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            city = city.import_data(data)
            session.add(city)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid city: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def city_exists(city_id):
    """
    Allow validate whether a city exist according to identifier
    :param city_id: identifier by city
    :return: an city object in JSON format
    """
    return session.query(City).filter(City.cityId == city_id).count()


def city_exists_code(code):
    """
    Allow validate whether a city exist according to identifier
    :param code: city code to seek
    :return: an city object in JSON format
    """
    return session.query(City).filter(City.code == code).count()





