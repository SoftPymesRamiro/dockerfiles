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
from .dependency import Dependency
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify, g
from ... import session


class Section(Base):
    __tablename__ = 'sections'
    sectionId = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(50))
    pucId = Column(Integer, ForeignKey('puc.pucId'))
    puc = relationship('PUC', foreign_keys=[pucId], lazy='joined')
    divisionId = Column(Integer, ForeignKey('divisions.divisionId'))
    dependencies = relationship("Dependency",
                                primaryjoin=sectionId == Dependency.sectionId,
                                cascade="all, delete, delete-orphan")
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    @staticmethod
    def export_data(data):
        """
            :param data
        """
        return {
            'sectionId': data.sectionId,
            'name': data.name,
            'code': data.code,
            'divisionId': data.divisionId,
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
            'dependencies': [] if data.dependencies is None or len(data.dependencies) == 0
            else [Dependency.export_data(dep) for dep in data.dependencies]
        }

    def import_data(self, data):
        """
            :param data
        """
        try:
            if "sectionId" in data:
                self.sectionId = data["sectionId"]
            self.name = data["name"]
            self.code = data["code"]
            self.divisionId = data["divisionId"]
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
    def get_sections():
        """
        """
        section = jsonify(data=[Section.export_data(section)
                                for section in session.query(Section).order_by(Section.code).all()])
        return section

    @staticmethod
    def get_section_by_id(section_id):
        section = session.query(Section)\
            .filter(Section.sectionId == section_id).first()
        return section

    @staticmethod
    def get_section(section_id):
        """
        """
        section = session.query(Section).get(section_id)
        if section is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        section = Section.export_data(section)
        response = jsonify(section)
        return response

    @staticmethod
    def post_section(data):
        section = Section()
        """
        """
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            section.import_data(data)

            session.add(section)
            session.commit()
            response = jsonify({"sectionId": section.sectionId})
        except KeyError as e:
            raise ValidationError("Invalid Section: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_section(section_id):
        """
            allow delete a section for to give identifier
            :param section_id identifier to section to delete
            :exception KeyError an error occurs when a key no set in data
            :return section object
        """
        section = session.query(Section).get(section_id)
        if section is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(section)
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
    def put_section(section_id, data):
        """
            allow update section for to give a identifier
            :param section_id identifier by  section to update
            :param data information by a section object
            :exception KeyError, a error occurs when a key in data not set
            :return section object in JSON format
        """
        if section_id != data["sectionId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not section_exist(data["sectionId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        section = session.query(Section).get(section_id)
        try:
            data["creationDate"] = section.creationDate
            data["createdBy"] = section.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            section = section.import_data(data)
            session.add(section)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid section: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        return response


def section_exist(section_id):
    """
        allow obtain a section according to identifier
        :param section_id identifier by section
        :return section object in JSON format
    """
    return session.query(Section).filter(Section.sectionId == section_id).count()
