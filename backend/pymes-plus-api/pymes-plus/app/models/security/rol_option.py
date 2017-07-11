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
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ...exceptions import ValidationError, InternalServerError
from .option import Option
from .user_branch_role import UserBranchRole


class RolOption(Base):
    """
    RolOption public class model
    """
    __tablename__ = 'roloptions'

    rolOptionId = Column(Integer, primary_key=True)
    optionId = Column(ForeignKey(u'options.optionId'), index=True)
    rolId = Column(ForeignKey(u'roles.rolId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    c = Column(Integer)
    r = Column(Integer)
    u = Column(Integer)
    d = Column(Integer)
    isDeleted = Column(Integer, default=0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    option = relationship(u'Option')
    role = relationship(u'Rol')

    def export_data(self):
        """
        Allow export roloption object to json
        :return: Json object
        """
        return{
            'rolOptionId': self.rolOptionId,
            'optionId': self.optionId,
            'rolId': self.rolId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'c': self.c,
            'r': self.r,
            'u': self.u,
            'd': self.d,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def export_data_custom(self):
        """
        Allow export roloption object to json
        :return: Json object
        """
        return {
            'rolOptionId': self.rolOptionId,
            'optionId': self.optionId,
            'rolId': self.rolId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'c': self.c,
            'r': self.r,
            'u': self.u,
            'd': self.d,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            # 'optionCode': self.option.code,
            'optionName': self.option.name
        }

    def import_data(self, data):
        """
        Allow import data to convert to rol option object
        :param data: json data
        :return: RolOption object
        """
        try:
            if 'rolOptionId' in data:
                self.rolOptionId = data['rolOptionId']
            if 'optionId' in data:
                self.optionId = data['optionId']
            if 'rolId' in data:
                self.rolId = data['rolId']
            if 'creationDate' in data:
                self.creationDate = data['creationDate']
            if 'updateDate' in data:
                self.updateDate = data['updateDate']
            if 'c' in data:
                self.c = data['c']
            if 'r' in data:
                self.r = data['r']
            if 'u' in data:
                self.u = data['u']
            if 'd' in data:
                self.d = data['d']
            if 'isDeleted' in data:
                self.isDeleted = data['isDeleted']
            if 'createdBy' in data:
                self.createdBy = data['createdBy']
            if 'updateBy' in data:
                self.updateBy = data['updateBy']
            return self
        except Exception as e:
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def is_authorized(code_option, option, user_id, branch_id):
        try:
            keyword = {option: 1}
            options = session.query(RolOption) \
                .filter_by(**keyword) \
                .join(Option, RolOption.optionId == Option.optionId) \
                .join(UserBranchRole, RolOption.rolId == UserBranchRole.rolId) \
                .filter(UserBranchRole.userId == user_id,
                        UserBranchRole.branchId == branch_id,
                        Option.code == code_option) \
                .first()
            return options
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)
