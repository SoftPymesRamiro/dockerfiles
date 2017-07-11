# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 19-08-2016
#########################################################
from datetime import datetime
from ... import Base
from ... import session
from math import ceil
from .puc import PUC
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy import or_, and_, func
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, backref, defer, subqueryload
from ...exceptions import InternalServerError
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError, InternalServerError


class Society(Base):
    __tablename__ = 'societies'

    societyId = Column(Integer, primary_key=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(2))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    puc = relationship(u'PUC')

    def import_data(self, data):
        """
        Allow create contact from data parameter
        :param data: inforamtion of contact
        :raise: Keyerror
        :exception: An error occurs when a key in data is not set
        :return: A contact object in JSOn format
        """
        if 'societyId' in data:
            self.societyId = data['societyId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self

    def export_data(self):
        return {
            'societyId': self.societyId,
            'pucId': self.pucId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'code': self.code,
            'name': self.name.upper(),
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'puc': None if self.puc is None or self.pucId is None else {
                'pucId': self.puc.pucId,
                'pucAccount': '{0}{1}{2}{3}{4}'.format(self.puc.pucClass, self.puc.pucSubClass, self.puc.account,
                                                       self.puc.subAccount, self.puc.auxiliary1),
                'name': self.puc.name,
                'percentage': self.puc.percentage
            }
        }

    @staticmethod
    def export_data_simple(data):
        return {
            "code": data.code,
            "societyId": data.societyId,
            "name": data.name.upper(),
            'puc': None if data.puc is None or data.pucId is None else {
                'pucId': data.puc.pucId,
                'pucAccount': '{0}{1}{2}{3}{4}'.format(data.puc.pucClass, data.puc.pucSubClass,
                                                       data.puc.account, data.puc.subAccount,
                                                       data.puc.auxiliary1),
                'name': data.puc.name,
                'percentage': data.puc.percentage
            }
        }

    @staticmethod
    def get_society_by_id(society_id):
        society = session.query(Society).get(society_id)
        if society is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        provider = society.export_data()
        response = jsonify(provider)
        return response

    @staticmethod
    def get_society_by_search(**kwargs):
        """
        :param: kwargs
        :return: Return Search from specific params
        """
        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")
        list_societies = []

        # if simple:
        list_societies = [Society.export_data_simple(societies)
                          for societies
                          in session.query(Society)
                              .join(PUC, PUC.pucId == Society.pucId)
                              .filter(or_(True if search == "" else None,
                                          *[Society.name.contains(word) for word in words]))
                          ]
        # else:
        #     list_societies = [Society.export_data(societies)
        #                       for societies
        #                       in session.query(Society)
        #                       .join(PUC, PUC.pucId == Society.pucId)
        #                       .filter(or_(True if search == "" else None,
        #                                   *[Society.name.contains(word) for word in words]))
        #                       ]

        response = jsonify(data=list_societies)
        if len(list_societies) == 0:
            response = jsonify({'code': 404, 'message': 'Not found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_society(data):
        """
        Returns: Return id from saved data
        """

        society_exist = session.query(Society) \
                            .filter(Society.code == data['code']) \
                            .count() > 0

        if society_exist:
            response = jsonify({'code': 400, 'message': 'Code already exist'})
            response.status_code = 400
            return response

        society = Society()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        society.import_data(data)
        session.add(society)

        try:
            session.commit()
            response = jsonify(societyId=society.societyId)
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def put_society(society_id, data):
        """

        Args:
            society_id:
            data:

        Returns: Return id from saved data
        """

        if society_id != data['societyId']:
            response = jsonify({'code': 400, 'message': 'Bad Request'})
            response.status_code = 400
            return response

        society = session.query(Society).get(society_id)
        data['creationDate'] = society.creationDate
        data['updateDate'] = datetime.now()
        data['createdBy'] = society.createdBy
        data['updateBy'] = g.user['name']

        society = society.import_data(data)
        session.add(society)

        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_society(society_id):
        """

        Args:
            society_id:

        Returns: Return id from saved Data
        """
        society = session.query(Society).get(society_id)

        if society is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(society)

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
            print(e)
            session.rollback()
            raise InternalServerError(e)
