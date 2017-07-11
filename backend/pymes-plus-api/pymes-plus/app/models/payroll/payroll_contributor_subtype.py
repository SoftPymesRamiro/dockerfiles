# coding=utf-8
# !/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from ... import session, Base
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify
from sqlalchemy import String, Integer, Column, DateTime


class PayrollContributorSubtype(Base):
    """

    """
    __tablename__ = 'payrollcontributorsubtypes'

    payrollContributorSubtypeId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(1))
    name = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    def export_data(self):
        """
            allow export size
            :return size object in JSON format
        """
        return {
            "payrollContributorSubtypeId" : self.payrollContributorSubtypeId,
            "creationDate" : self.creationDate,
            "updateDate" : self.updateDate,
            "isDeleted" : self.isDeleted,
            "code" : self.code,
            "name" : self.name,
            "createdBy" : self.createdBy,
            "updateBy" : self.updateBy,
        }

    def import_data(self, data):
        """
            allow create data from information
            :param data infromation by new size
            :exception  An error occurs when a key in data is not set
            :return size object in JSON format
        """
        try:

            if "payrollContributorSubtypeId" in data:
                self.payrollContributorSubtypeId = data['payrollContributorSubtypeId']
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

        except KeyError as e:
            raise ValidationError("Invalid color: missing " + e.args[0])
        return self

    @staticmethod
    def export_data_light(data):
        """
            allow export PayrollContributorSubtypes
            :return PayrollContributorSubtypes object in JSON format
        """
        return {
            "id": data.payrollContributorSubtypeId,
            "name": "{0} {1}".format(data.code, data.name)
        }


    @staticmethod
    def get_payroll_contributor_subtypes_by_search(**kwargs):
        """
        Allow search role employees according to request params
        :param kwargs: request parameters
        :return: a PayrollContributorSubtypes object found
        """
        simple = kwargs.get("simple")

        if simple:
            list_payroll_contributor_subtypess = jsonify(data=[PayrollContributorSubtype.export_data_light(payroll_contributor_subtypes)
                                             for payroll_contributor_subtypes
                                                               in session.query(PayrollContributorSubtype).all()])


            return list_payroll_contributor_subtypess
