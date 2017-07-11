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
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify, g
from ... import session


class Dependency(Base):
    """

    """
    __tablename__ = 'dependencies'
    dependencyId = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(50))
    pucId = Column(Integer, ForeignKey('puc.pucId'))
    puc = relationship('PUC', foreign_keys=[pucId], lazy='joined')
    sectionId = Column(Integer, ForeignKey('sections.sectionId'))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    @staticmethod
    def export_data(data):
        """
        Allow 
        :param data:
        :return:
        """
        return {
            'dependencyId': data.dependencyId,
            'name': data.name,
            'code': data.code,
            'sectionId': data.sectionId,
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
            'updateDate': data.updateDate
        }


    def import_data(self, data):
        try:
            if "dependencyId" in data:
                self.dependencyId = data["dependencyId"]
            self.name = data["name"]
            self.code = data["code"]
            self.sectionId = data["sectionId"]
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
    def get_dependencies():

        dependency = jsonify(data=[Dependency.export_data(dependency) for dependency in session.query(Dependency).order_by(Dependency.code).all()])
        return dependency

    @staticmethod
    def get_dependency_by_id(dependency_id):
        dependency = session.query(Dependency)\
            .filter(Dependency.dependencyId == dependency_id).first()
        return dependency

    @staticmethod
    def get_dependency(dependency_id):
        dependency = session.query(Dependency).get(dependency_id)
        if dependency is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        dependency = Dependency.export_data(dependency)
        response = jsonify(dependency)
        return response

    @staticmethod
    def post_dependency(data):
        dependency = Dependency()
        # if dependency_exist_by_code(data["code"]):
        #     # revisa si ya hay una dependencia con ese codigo
        #     response = jsonify({'error': 'bad request', 'message': 'La Dependency ya existe'})
        #     response.status_code = 400
        #     return response

        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            dependency.import_data(data)

            session.add(dependency)
            session.commit()
            response = jsonify({"dependencyId": dependency.dependencyId})
        except KeyError as e:
            raise ValidationError("Invalid Dependency: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_dependency(dependency_id):
        dependency = session.query(Dependency).get(dependency_id)
        if dependency is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(dependency)
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
    def put_dependency(dependency_id, data):
        if dependency_id != data["dependencyId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not dependency_exist(data["dependencyId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        dependency = session.query(Dependency).get(dependency_id)
        try:
            data["creationDate"] = dependency.creationDate
            data["createdBy"] = dependency.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            dependency = dependency.import_data(data)
            session.add(dependency)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid dependency: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def dependency_exist(dependency_id):
    return session.query(Dependency).filter(Dependency.dependencyId == dependency_id).count()


def dependency_exist_by_code(dependency_code):
    return session.query(Dependency).filter(Dependency.code == dependency_code).count()

