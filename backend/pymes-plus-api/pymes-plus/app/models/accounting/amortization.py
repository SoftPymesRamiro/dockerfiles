# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"
__status__ = "develop"


from flask import jsonify, g
from ... import Base
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, load_only
from ...exceptions import ValidationError
from ...utils import converters
from ...exceptions import ValidationError
from datetime import datetime

class Amortization(Base):
    __tablename__ = 'amortizations'

    amortizationId = Column(Integer, primary_key=True)
    deferredPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    expensePUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    companyId = Column(Integer, ForeignKey("companies.companyId"))
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    company = relationship(u'Company')
    deferredPUC = relationship(u'PUC', foreign_keys=[deferredPUCId])
    expensePUC = relationship(u'PUC', foreign_keys=[expensePUCId])

    # puc = relationship(u'PUC')
    # deferredPUC = relationship(u'PUC', primaryjoin='Amortization.deferredPUCId == PUC.pucId')
    # expensePUC = relationship(u'PUC', primaryjoin='Amortization.expensePUCId == PUC.pucId')

    def export_data(self):
        """
            Allow export an accounting record object
            :return:  Document header object in JSon format
        """

        return {
            "amortizationId": self.amortizationId,
            "deferredPUCId": self.deferredPUCId,
            "deferredPuc": None if self.deferredPUCId is None or self.deferredPUC is None else{
                "pucId": self.deferredPUC.pucId,
                "account": '{0}{1}{2}{3}{4}'.format(self.deferredPUC.pucClass,
                                                    self.deferredPUC.pucSubClass,
                                                    self.deferredPUC.account,
                                                    self.deferredPUC.subAccount,
                                                    self.deferredPUC.auxiliary1),
                "name": self.deferredPUC.name,
            },
            "expensePUCId": self.expensePUCId,
            "expensePuc": None if self.expensePUCId is None or self.expensePUC is None else{
                "pucId": self.expensePUC.pucId,
                "account": '{0}{1}{2}{3}{4}'.format(self.expensePUC.pucClass,
                                                    self.expensePUC.pucSubClass,
                                                    self.expensePUC.account,
                                                    self.expensePUC.subAccount,
                                                    self.expensePUC.auxiliary1),
                "name": self.expensePUC.name,
            },
            "companyId": self.companyId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy
        }


    def import_data(self, data):
        """
            Allow create a new accounting record object from data
            :param data: information by new accounting record
            :exception: KeyError an error occurs when a key in data not is set
            :return: accounting record object in JSON format
        """
        if "amortizationId" in data:
            self.amortizationId = data['amortizationId']
        if "deferredPUCId" in data:
            self.deferredPUCId = data['deferredPUCId']
        if "expensePUCId" in data:
            self.expensePUCId = data['expensePUCId']
        if "companyId" in data:
            self.companyId = data['companyId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']

        return self


    @staticmethod
    def get_amortizations():
        """

        :return:
        """
        amortizations = jsonify(data=[amortizations.export_data(amortizations)
                                      for amortizations in session.query(Amortization)
                                .order_by(Amortization.amortizationId).all()])

        return amortizations

    @staticmethod
    def get_amortization_byid(amortization_id):
        """

        :param amortization_id:
        :return:
        """
        amortization = session.query(Amortization).get(amortization_id)

        if amortization is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        amortization = amortization.export_data()
        response = jsonify(amortization)
        return response


    @staticmethod
    def get_amortization_bycompanyid(company_id):
        """

        :param company_id:
        :return:
        """
        amortization_list = [amortization.export_data()
                       for amortization in session.query(Amortization)
                           .filter(Amortization.companyId == company_id)]

        if len(amortization_list) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404

        response = jsonify(data=amortization_list)
        return response


    # @staticmethod
    # def search_amortization(**kwargs):
    #     """
    #
    #     :param kwargs:
    #     :return:
    #     """
    #     search = kwargs.get('search')
    #     words = kwargs.get('words')
    #     simple = kwargs.get('simple')
    #     page_size = kwargs.get('page_size')
    #     page_number = kwargs.get('page_number')
    #
    #     economic_activity_id = kwargs.get('economic_activity_id')
    #     company_id = kwargs.get('company_id')


    @staticmethod
    def post_amortization(data):
        """

        :param data:
        :return:
        """
        amortization = Amortization()
        try:
            data['creationDate'] = datetime.now()
            data['updateDate'] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            data["isDeleted"] = 0

            amortization.import_data(data)
            session.add(amortization)

            session.commit()
            response = jsonify({'amortizationId': amortization.amortizationId})

        except KeyError as e:
            raise ValidationError('Invalid amortization: missing' + e.args[0])

        return response


    @staticmethod
    def put_amortization(amortization_id, data):
        """

        :param data:
        :param amortization_id:
        :return:
        """
        amortization = session.query(Amortization).get(amortization_id)

        try:
            data['creationDate'] = amortization.creationDate
            data['createdBy'] = amortization.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']
            data["isDeleted"] = 0

            amortization = amortization.import_data(data)
            session.add(amortization)

            session.commit()
            response = jsonify({'ok': 'ok'})

        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid amortization: missing' + e.args[0])

        return response


    @staticmethod
    def delete_amortization(amortization_id):
        """

        :return:
        """
        amortization = session.query(Amortization).get(amortization_id)
        if amortization is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(amortization)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
