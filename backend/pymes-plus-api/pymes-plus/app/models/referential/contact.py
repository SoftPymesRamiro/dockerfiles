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
from ... import Base, session
from ...exceptions import InternalServerError
from math import ceil
from flask import jsonify
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy import or_, and_
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship, backref


class Contact(Base):
    __tablename__ = 'contacts'

    contactId = Column(Integer, primary_key=True)
    providerId = Column(ForeignKey(u'providers.providerId'), index=True)
    employeeId = Column(ForeignKey(u'employees.employeeId'), index=True)
    financialEntityId = Column(ForeignKey(u'financialentities.financialEntityId'), index=True)
    otherThirdId = Column(ForeignKey(u'otherthirds.otherThirdId'), index=True)
    payrollEntityId = Column(ForeignKey(u'payrollentities.payrollEntityId'), index=True)
    customerId = Column(ForeignKey(u'customers.customerId'), index=True)
    businessAgentId = Column(ForeignKey(u'businessagents.businessAgentId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    isMain = Column(TINYINT)
    name = Column(String(100))
    phone1 = Column(String(30))
    extension1 = Column(String(10))
    phone2 = Column(String(30))
    extension2 = Column(String(10))
    phone3 = Column(String(30))
    updateBy = Column(String(50))
    # lastName = Column(String(100))
    extension3 = Column(String(10))
    fax = Column(String(30))
    email1 = Column(String(100))
    email2 = Column(String(100))
    roleEmployee = Column(String(50))
    createdBy = Column(String(50))

    # businessagent = relationship(u'Businessagent')
    # customer = relationship(u'Customer')
    # employee = relationship(u'Employee')
    # financialentity = relationship(u'Financialentity')
    # otherthird = relationship(u'Otherthird')
    # payrollentity = relationship(u'Payrollentity')
    # provider = relationship(u'Provider')

    def export_data(self):
        """
        Allow export current contact info
        :return: a full contact object in JSON format
        """
        return {
            "contactId": self.contactId,
            "providerId": self.providerId,
            "employeeId": self.employeeId,
            "financialEntityId": self.financialEntityId,
            "otherThirdId": self.otherThirdId,
            "payrollEntityId": self.payrollEntityId,
            "customerId": self.customerId,
            "businessAgentId": self.businessAgentId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "isMain": self.isMain,
            "name": self.name,
            "phone1": self.phone1,
            "extension1": self.extension1,
            "phone2": self.phone2,
            "extension2": self.extension2,
            "phone3": self.phone3,
            "updateBy": self.updateBy,
            # "lastName": self.lastName,
            "extension3": self.extension3,
            "fax": self.fax,
            "email1": self.email1,
            "email2": self.email2,
            "roleEmployee": self.roleEmployee,
            "createdBy": self.createdBy,
        }

    def import_data(self, data):
        """
        Allow create contact from data parameter
        :param data: inforamtion of contact
        :raise: Keyerror
        :exception: An error occurs when a key in data is not set
        :return: A contact object in JSOn format
        """
        try:
            if "contactId" in data:
                self.contactId = data["contactId"]
            if "providerId" in data:
                self.providerId = data["providerId"]
            if "employeeId" in data:
                self.employeeId = data["employeeId"]
            if "financialEntityId" in data:
                self.financialEntityId = data["financialEntityId"]
            if "otherThirdId" in data:
                self.otherThirdId = data["otherThirdId"]
            if "payrollEntityId" in data:
                self.payrollEntityId = data["payrollEntityId"]
            if "customerId" in data:
                self.customerId = data["customerId"]
            if "businessAgentId" in data:
                self.businessAgentId = data["businessAgentId"]
            if "creationDate" in data:
                self.creationDate = data["creationDate"]
            if "updateDate" in data:
                self.updateDate = data["updateDate"]
            if "isDeleted" in data:
                self.isDeleted = data["isDeleted"]
            if "isMain" in data:
                self.isMain = data["isMain"]
            if "name" in data:
                self.name = data["name"]
            if "phone1" in data:
                self.phone1 = data["phone1"]
            if "extension1" in data:
                self.extension1 = data["extension1"]
            if "phone2" in data:
                self.phone2 = data["phone2"]
            if "extension2" in data:
                self.extension2 = data["extension2"]
            if "phone3" in data:
                self.phone3 = data["phone3"]
            if "updateBy" in data:
                self.updateBy = data["updateBy"]
            # if "lastName" in data:
            #     self.lastName = data["lastName"]
            if "extension3" in data:
                self.extension3 = data["extension3"]
            if "fax" in data:
                self.fax = data["fax"]
            if "email1" in data:
                self.email1 = data["email1"]
            if "email2" in data:
                self.email2 = data["email2"]
            if "roleEmployee" in data:
                self.roleEmployee = data["roleEmployee"]
            if "createdBy" in data:
                self.createdBy = data["createdBy"]
        except Exception as e:
            raise e

        return self

    @staticmethod
    def delete_contact(contact_id):
        """
        Allow delete a contact accordign to idenetifier
        :param contact_id: identifier by contact object
        :raise: Exception
        :exception: an error occurs when server or databse not performance
        :return: return a contact
        """
        contact = session.query(Contact).get(contact_id)

        if contact is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(contact)
        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

