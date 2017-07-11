# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from datetime import datetime
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from flask import jsonify
from ...exceptions import ValidationError, InternalServerError


class Rol(Base):
    """Rol as a public model class.

    note::

    """
    __tablename__ = "roles"

    rolId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT, default=0)
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    def export_data(self):
        """
        Allow export rol option object to json
        :return: json object
        """
        return {
            "rolId": self.rolId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "name": self.name,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
        }

    def import_data(self, data):
        """
        Allow import data object to convert to rol object
        :param data: json data
        :return: Rol object
        """
        try:
            if 'rolId' in data:
                self.rolId = data['rolId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'name' in data:
                self.name = data['name']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
            return self
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_roles():
        """
        Allow obtain all roles
        :return: JSON object with array de roles objects in JSON fomat
        """
        roles = jsonify(data=[color.export_data() for color in session.query(Rol).filter(Rol.isDeleted == 0)
                        .order_by(Rol.name).all()])
        return roles

    @staticmethod
    def get_roles_by_search(search):
        """
        Allow get roles according a search pattern
        :param search: string search
        :return: role list object
        """
        try:
            text_search = "" if search is None else search.strip()
            words = text_search.split(' ', 1) if text_search is not None else None
            roles = [rol.export_data()
                     for rol in session.query(Rol)
                         .filter(and_(Rol.isDeleted == 0,
                                      or_(True if search == "" else None,
                                          or_(*[Rol.name.like('%{0}%'.format(s))
                                                for s in words]))
                                      ))
                     ]
            # return jsonify(userList=users)
            return roles
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

