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
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, and_, or_
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from ...exceptions import ValidationError, InternalServerError
from .section import Section
from flask import jsonify, g
from ... import session


class Division(Base):
    """
    """
    __tablename__ = 'divisions'
    divisionId = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(50))
    pucId = Column(Integer, ForeignKey('puc.pucId'))
    puc = relationship('PUC', foreign_keys=[pucId], lazy='joined')
    costCenterId = Column(Integer, ForeignKey('costcenters.costCenterId'))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    sections = relationship("Section",
                            primaryjoin=divisionId == Section.divisionId,
                            cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        return {
            'divisionId': data.divisionId,
            'name': data.name.encode('utf-8'),
            'code': data.code.encode('utf-8'),
            'costCenterId': data.costCenterId,
            'pucId': data.pucId,
            'puc': None if data.puc is None or data.pucId is None else {
                'pucId': data.puc.pucId,
                'account': '{0}{1}{2}{3}{4} {5}'.format(
                    data.puc.pucClass,
                    data.puc.pucSubClass,
                    data.puc.account,
                    data.puc.subAccount,
                    data.puc.auxiliary1,
                    data.puc.name),
                'percentage': data.puc.percentage,
                'pucAccount': '{0}{1}{2}{3}{4}'.format(
                    data.puc.pucClass,
                    data.puc.pucSubClass,
                    data.puc.account,
                    data.puc.subAccount,
                    data.puc.auxiliary1),
                'name': data.puc.name
            },
            'expenses': None if data.puc is None else 'Cuenta {}{}'.format(data.puc.pucClass, data.puc.pucSubClass),
            'createdBy': data.createdBy,
            'creationDate': data.creationDate,
            'updateBy': data.updateBy,
            'isDeleted': data.isDeleted,
            'updateDate': data.updateDate,
            'sections': [] if data.sections is None or len(data.sections) == 0
            else [Section.export_data(sect) for sect in data.sections]
        }

    def import_data(self, data):
        try:
            if "divisionId" in data:
                self.divisionId = data["divisionId"]
            self.name = data["name"]
            self.code = data["code"]
            self.costCenterId = data["costCenterId"]
            if "pucId" in data:
                self.pucId = data["pucId"]
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
            raise ValidationError("Invalid paymentMethod: missing " + e.args[0])
        return self

    @staticmethod
    def get_divisions():

        division = jsonify(data=[Division.export_data(division) for division in session.query(Division).order_by(Division.code).all()])
        return division

    @staticmethod
    def get_division_by_id(division_id):
        division = session.query(Division)\
            .filter(Division.divisionId == division_id).first()
        return division

    @staticmethod
    def get_division(division_id):
        division = session.query(Division).get(division_id)
        if division is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        division = Division.export_data(division)
        response = jsonify(division)
        return response

    @staticmethod
    def post_division(data):
        division = Division()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            # TODO: Colocar el nombre de autenticacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            division.import_data(data)

            session.add(division)
            session.commit()
            response = jsonify({"divisionId": division.divisionId})
        except KeyError as e:
            raise ValidationError("Invalid Division: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_division(division_id):
        division = session.query(Division).get(division_id)
        if division is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(division)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 500
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_division(division_id, data):
        if division_id != data["divisionId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not division_exist(data["divisionId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        division = session.query(Division).get(division_id)
        try:
            data["creationDate"] = division.creationDate
            data["createdBy"] = division.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            division = division.import_data(data)
            session.add(division)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid division: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def division_exist(division_id):
    return session.query(Division).filter(Division.divisionId == division_id).count()


def division_exist_by_code(division_code):
    return session.query(Division).filter(Division.code == division_code).count()

