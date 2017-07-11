# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from datetime import datetime
from ... import session, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, DECIMAL
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from  sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError, InternalServerError


class RoleEmployee(Base):
    """RoleEmployee as a public model class.
    """
    __tablename__ = 'roleemployees'

    roleEmployeeId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    baseSalary = Column(DECIMAL(18, 4), default=0.0)
    code = Column(String(10))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    company = relationship(u'Company')

    def export_data(self):
        """
        Allow export role employee
        :return role employee object in JSON format
        """
        return {
            "roleEmployeeId": self.roleEmployeeId,
            "companyId": self.companyId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "baseSalary": self.baseSalary,
            "code": self.code,
            "name": self.name,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
        }

    def import_data(self, data):
        """
        Allow create data from information
        :param data information by new role employee
        :return role employee object in JSON format
        """
        if "roleEmployeeId" in data:
            self.roleEmployeeId = data['roleEmployeeId']

        self.companyId = data['companyId']

        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "baseSalary" in data:
            self.baseSalary = data['baseSalary']
        if "code" in data:
            self.code = data['code']
        if "name" in data:
            self.name = data['name']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def export_data_light(data):
        """
        Allow export role_employee
        :return role_employee object in JSON format
        """
        return {
            "roleEmployeeId": data.roleEmployeeId,
            "code": data.code,
            "baseSalary" :data.baseSalary,
            "name": "{0} {1}".format(data.code, data.name)
        }


    @staticmethod
    def get_role_employees_by_search(**kwargs):
        """
        Allow search role employees according to request params
        :param kwargs: request parameters
        :return: a role_employee object found
        """
        simple = kwargs.get("simple")
        company_id = kwargs.get("companyId")
        search = kwargs.get("search")
        words = kwargs.get("words")

        if simple:
            list_role_employees = [RoleEmployee.export_data_light(employee)
                                             for employee in session.query(RoleEmployee).
                                       filter(RoleEmployee.companyId == company_id).all()]

            return jsonify(data=list_role_employees)

        if search:
            text_search = "" if search is None else str(search).strip()
            words = text_search.split(' ', 1) if text_search is not None else None
            list_role_employees = [RoleEmployee.export_data(employee)
                             for employee in session.query(RoleEmployee)
                                       .filter(and_(RoleEmployee.companyId == company_id,
                    True if search == '' else or_(
                    or_(*[RoleEmployee.code.like('%{0}%'.format(s)) for s in words]),
                    or_(*[RoleEmployee.name.like('%{0}%'.format(s)) for s in words]),
                )))]

            if list_role_employees:
                response = jsonify(data=list_role_employees)

            return response

        else:
            list_role_employees = [RoleEmployee.export_data(employee)
                                for employee in session.query(RoleEmployee).
                                    filter(RoleEmployee.companyId == company_id).all()]
            return jsonify(data=list_role_employees)


    @staticmethod
    def get_role_employee(role_employee_id):
        """
            get role_employee for to give a identifier
            :param role_employee_id indentifier by seek role_employee
            :return role_employee object in JSON format
        """
        role_employee = session.query(RoleEmployee).get(role_employee_id)
        if role_employee is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        role_employee = role_employee.export_data()
        response = jsonify(role_employee)
        return response

    @staticmethod
    def post_role_employee(data):
        """

        :param data:
        :return:
        """
        role_employee = RoleEmployee()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']
        role_employee.import_data(data)
        session.add(role_employee)

        try:
            session.commit()
            response = jsonify(roleEmployeeId=role_employee.roleEmployeeId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_role_employee(role_employee_id, data):
        """

        :param role_employee_id:
        :param data:
        :return:
        """
        role_employee = session.query(RoleEmployee).get(role_employee_id)

        data["creationDate"] = role_employee.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = role_employee.createdBy
        data["updateBy"] = g.user['name']

        role_employee = role_employee.import_data(data)
        session.add(role_employee)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_role_employee(role_employee_id):
        """

        :param role_employee_id:
        :return:
        """
        role_employee = session.query(RoleEmployee).get(role_employee_id)

        if role_employee is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(role_employee)

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