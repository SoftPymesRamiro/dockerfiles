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

from ... import session, Base
from datetime import datetime
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify,g
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey


class Profession(Base):
    __tablename__ = 'professions'

    professionId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(3))
    name = Column(String(30))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    def export_data(self):
        """
            allow export profession
            :return profession object in JSON format
        """
        return {
            "professionId": self.professionId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "code": self.code,
            "name": self.name,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
        }

    def import_data(self, data):
        """
            allow create data from information
            :param data information by new profession
            :exception  An error occurs when a key in data is not set
            :return profession object in JSON format
        """
        if "professionId" in data:
            self.professionId = data['professionId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
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
            allow export profession
            :return profession object in JSON format
        """
        return {
            "professionId": data.professionId,
            "name": "{0} {1}".format(data.code, data.name)
        }

    @staticmethod
    def get_profession_by_search(**kwargs):
        """
        Allow search profession according to request params
        :param kwargs: request parameters
        :return: a profession object found
        """
        simple = kwargs.get("simple")

        if simple:
            list_professions = jsonify(data=[Profession.export_data_light(profession)
                                             for profession in session.query(Profession).all()])
            return list_professions
        else:
            list_professions = jsonify(data=[Profession.export_data(profession)
                                            for profession in session.query(Profession).all()])
            return list_professions

    @staticmethod
    def get_professions():
        """
        Allow obtain all currencies
        :return: JSON object with profession data
        """
        profession = jsonify(data=[profession.export_data() for profession
                                   in session.query(Profession).order_by(Profession.code).all()])
        return profession

    @staticmethod
    def post_profession(data):
        profession = Profession()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']

        profession.import_data(data)
        session.add(profession)

        try:
            session.commit()
            response = jsonify(professionId=profession.professionId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_profession(profession_id, data):

        profession = session.query(Profession).get(profession_id)

        data["creationDate"] = profession.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = profession.createdBy
        data["updateBy"] = g.user['name']

        profession = profession.import_data(data)
        session.add(profession)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_profession(profession_id):
        profession = session.query(Profession).get(profession_id)

        if profession is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(profession)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)