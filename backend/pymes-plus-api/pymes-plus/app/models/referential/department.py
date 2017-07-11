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
from .city import City
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Department(Base):
    """
    """
    __tablename__ = 'departments'

    departmentId = Column(Integer, primary_key=True, nullable=False)
    countryId = Column(Integer, ForeignKey('countries.countryId'))
    country = relationship('Country', lazy='joined', innerjoin=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(2))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    cities = relationship("City",
                          primaryjoin=departmentId == City.departmentId,
                          cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
        Allow export departament data
        :param data: departament info
        :return: departamente object in JSON format
        """
        return {
            'departmentId': data.departmentId,
            'countryId': data.countryId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'name': data.name,
            'code': data.code,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'cities': [] if data.cities is None or len(data.cities) == 0
            else [City.export_data(cit) for cit in data.cities]
        }

    def import_data(self, data):
        """
        Allow create departament from data
        :param data: information by new departament
        :raise: KeyError
        :exception: an error occurs when key in data is not set
        :return: a
        """
        try:
            if 'departmentId' in data:
                self.departmentId = data['departmentId']
            if 'countryId' in data:
                self.countryId = data['countryId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            self.code = data['code']
            self.name = data['name']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
        except KeyError as e:
            raise ValidationError('Invalid departments: missing ' + e.args[0])
        return self

    @staticmethod
    def get_departments():
        """
        Allow obtain all departaments
        :return:
        """
        department = jsonify(data=[Department.export_data(department)
                                   for department in session.query(Department)
                             .order_by(Department.code).all()])
        return department

    @staticmethod
    def get_department_by_country(country_id):
        """
        Allow obtain departament for to give country identifier
        :param country_id:country indentifier
        :return: a departament
        """
        departments = [Department.export_data(department)
                       for department in session.query(Department)
                           .filter(Department.countryId == country_id)]

        if len(departments) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404

        response = jsonify(data=departments)
        return response

    @staticmethod
    def get_department(department_id):
        """

        :param department_id:
        :return:
        """
        department = session.query(Department).get(department_id)
        if department is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        department = department.export_data(department)
        response = jsonify(department)
        return response

    @staticmethod
    def post_department(data):
        """
        Allow create a new departament
        :param data: information by new departament
        :raise: KeyError
        :exception:An error occurs when key in data is not set
        :return:
        """
        department = Department()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            # TODO: colocar el nombre de autenticacion
            data['createdBy'] = g.user['name']
            data['updateBy'] = g.user['name']
            department.import_data(data)

            session.add(department)
            session.commit()
            response = jsonify({'departmentId': department.departmentId})
        except KeyError as e:
            raise ValidationError('Invalid department: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_department(department_id):
        """
        Allow delete departament for to give departament identifier
        :param department_id: departament identifierto delete
        :return: Void
        """
        department = session.query(Department).get(department_id)
        if department is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(department)
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
    def put_department(department_id, data):
        """
        Allow update a departament according to identifier
        :param department_id: identifier by departament to update
        :param data: information to change
        :return: a departament object
        """
        if department_id != data['departmentId']:
            response = jsonify({'error': 'bad request', 'message': 'El departamento ya existe'})
            response.status_code = 400
            return response
        if not department_exists(data['departmentId']):
            response = jsonify({'error': 'bad request', 'message': 'Not Found'})
            response.status_code = 404
            return response
        department = session.query(Department).get(department_id)

        try:
            data['creationDate'] = department.creationDate
            data['createdBy'] = department.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            department = department.import_data(data)
            session.add(department)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid department: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def department_exists(department_id):
    """
    Allow validate a departanment identifier
    :param department_id: departament identifier
    :return:an departament object found
    """
    return session.query(Department).filter(Department.departmentId == department_id).count()


