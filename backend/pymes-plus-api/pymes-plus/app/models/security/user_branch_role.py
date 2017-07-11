# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify
import jwt
import os


class UserBranchRole(Base):
    """UserBranchRole as a public model class.

    note::

    """
    __tablename__ = 'userbranchroles'

    userBranchRolId = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    rolId = Column(Integer, ForeignKey("roles.rolId"))
    rol = relationship("Rol")
    userId = Column(Integer, ForeignKey("users.userId"))
    user = relationship("User")
    # aspNetUserId = Column(Integer, ForeignKey('aspnetusers.id'))
    # aspNetUser = relationship('AspNetUsers')
    branchId = Column(Integer, ForeignKey("branches.branchId"))
    branch = relationship("Branch")
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=None)
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=None)
    processDate = Column(DateTime, default=None)
    isDeleted = Column(Integer, default=0)

    def import_data(self, data):
        """
        Allow create a new user branch role from
        :param data: information by new user branch
        :return: new user branch role object in JSON format
        """
        try:
            if "rolId" in data:
                self.rolId = data["rolId"]
            if "userId" in data:
                self.userId = data["userId"]
            if "branchId" in data:
                self.branchId = data["branchId"]
            # if "aspNetUserId" in data:
            #     self.aspNetUserId = data["aspNetUserId"]
            if "branchId" in data:
                self.branchId = data["branchId"]
            if "createdBy" in data:
                self.createdBy = data["createdBy"]
            if "creationDate" in data:
                self.creationDate = datetime.strptime(str(data["creationDate"]), '%a, %d %b %Y %H:%M:%S %Z')
            if "updateBy" in data:
                self.updateBy = data["updateBy"]
            if "updateDate" in data:
                self.updateDate = datetime.strptime(str(data["updateDate"]), '%a, %d %b %Y %H:%M:%S %Z')
            if "processDate" in data:
                self.processDate = datetime.strptime(str(data["processDate"]), '%a, %d %b %Y %H:%M:%S %Z')
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
        except KeyError as e:
            raise ValidationError("Invalid userbranchrole: missing " + e.args[0])
        return self

    def export_data(self):
        """
        Allow extract a user branch role object

        :return:
        """
        return {
            "userBranchRolId": self.userBranchRolId,
            "rolId": self.rolId,
            "userId": self.userId,
            "branchId": self.branchId,
            # "aspNetUserId": self.aspNetUserId,
            "createdBy": self.createdBy,
            "creationDate": self.creationDate,
            "updateBy": self.updateBy
        }

    @staticmethod
    def delete_user_branch_role(id):
        """
        Allow delete a user branch role
        :param id:identifier by the user branch role to delete
        :return: status code
        """
        ubr = session.query(UserBranchRole).get(id)
        if ubr is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(ubr)
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
