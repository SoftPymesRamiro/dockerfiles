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
from flask import jsonify, g
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ...utils import converters


class BillingResolution(Base):
    __tablename__ = 'billingresolutions'

    billingResolutionId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    date = Column(DateTime, default=datetime.now())
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime)
    isActive = Column(TINYINT(1))
    isDeleted = Column(TINYINT(1))
    printable = Column(TINYINT(1), default=1, nullable=False)
    authorizedOrEnabled = Column(TINYINT(1))
    resolution = Column(String(50))
    resolutionType = Column(String(1))
    prefix = Column(String(5))
    months = Column(TINYINT(1))
    minimum = Column(TINYINT(1))
    consecutiveFrom = Column(String(10))
    consecutiveTo = Column(String(10))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    branch = relationship(u'Branch')

    def export_data(self):
        """
        Allow obtain BillingResolution data

        :return: all BillingResolution data
        """
        return {
            'billingResolutionId': self.billingResolutionId,
            'branchId': self.branchId,
            'date': self.date,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isActive': bool(self.isActive),
            'isDeleted': self.isDeleted,
            'printable': bool(self.printable),
            'authorizedOrEnabled': self.authorizedOrEnabled,
            'resolution': self.resolution,
            'months': self.months,
            'minimum': self.minimum,
            'resolutionType': self.resolutionType,
            'prefix': self.prefix,
            'consecutiveFrom': self.consecutiveFrom,
            'consecutiveTo': self.consecutiveTo,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }


    def import_data(self, data):
        """
        Allow create billing resolution fro data information
        :param data: information of billing resolution
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:  billing resolution object
        """
        if 'billingResolutionId' in data:
            self.billingResolutionId = data['billingResolutionId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'date' in data:
            self.date = converters.convert_string_to_date(data['date'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isActive' in data:
            self.isActive = data['isActive']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'printable' in data:
            self.printable = data['printable']
        if 'authorizedOrEnabled' in data:
            self.authorizedOrEnabled = data['authorizedOrEnabled']
        if 'resolution' in data:
            self.resolution = data['resolution']
        if 'resolutionType' in data:
            self.resolutionType = data['resolutionType']
        if 'prefix' in data:
            self.prefix = data['prefix']
        if 'months' in data:
            self.months = data['months']
        if 'minimum' in data:
            self.minimum = data['minimum']
        if 'consecutiveFrom' in data:
            self.consecutiveFrom = data['consecutiveFrom']
        if 'consecutiveTo' in data:
            self.consecutiveTo = data['consecutiveTo']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def get_billing_resolution(billing_resolution_id):
        """
        Allow obtain a billing_resolution for to give identifier
        :param billing_resolution_id: identiifer by a billing_resolution
        :return: a billing_resolution object in JSON format
        """
        billing_resolution = session.query(BillingResolution).get(billing_resolution_id)
        if billing_resolution is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        billing_resolution = BillingResolution.export_data(billing_resolution)
        response = jsonify(billing_resolution)
        return response


    @staticmethod
    def get_billing_resolution_bysearch(**kwargs):
        """
            find billing_resolution according to search values
            :param search
            :return a billing_resolution object in JSON format
        """
        branch_id = kwargs.get('branch_id')
        search = kwargs.get('search')
        words = kwargs.get('words')
        simple = kwargs.get('simple')

        if simple:
            billing_resolution = [BillingResolution.export_data(billing_resolution)
                                  for billing_resolution in session.query(BillingResolution)
                                      .filter(BillingResolution.branchId == branch_id)
                                      .order_by(BillingResolution.prefix)
                                      .all()]

            response = jsonify(data=billing_resolution)
            if len(billing_resolution) == 0:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404

            return response
        else:
            billing_resolution = [BillingResolution.export_data(billing_resolution)
                                 for billing_resolution in session.query(BillingResolution).filter(and_(
                    or_(or_(*[BillingResolution.resolution.contains(word) for word in words]),
                        or_(*[BillingResolution.prefix.contains(word) for word in words]),
                        or_(*[BillingResolution.consecutiveFrom.contains(word) for word in words]),
                        or_(*[BillingResolution.consecutiveTo.contains(word) for word in words])),
                        BillingResolution.branchId == branch_id
                    )
                ).order_by(BillingResolution.prefix)]

            response = jsonify(data=billing_resolution)
            return response

    @staticmethod
    def create_billing_resolution(data):
        """
        Allow create a new billing resolution
        :param data:
        :return:
        """
        billing_resolution_exist= session.query(BillingResolution) \
            .filter(and_(BillingResolution.resolution ==data['resolution'],
                         BillingResolution.resolutionType == data['resolutionType'],
                         BillingResolution.prefix == data['prefix'],
                         BillingResolution.consecutiveFrom == data['consecutiveFrom'],
                         )).count()

        if billing_resolution_exist > 0:
            response = jsonify({'error': 'bad request', 'message': 'Ya existe una resolucion con este codigo'})
            response.status_code = 400
            return response

        billing_resolution = BillingResolution()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data["updateBy"] = g.user['name']
        billing_resolution = billing_resolution.import_data(data)

        session.add(billing_resolution)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        return jsonify({"billingResolutionId": billing_resolution.billingResolutionId})

    @staticmethod
    def update_billing_resolution(billing_resolotion_id, data):
        """
        Allow update billing resolution according to identifier
        :param billing_resolotion_id: identifier by billing resolutions to update
        :param data: information to change in defult value
        :return: a billing resolution object
        """
        billing_resolution = session.query(BillingResolution).get(billing_resolotion_id)

        data["creationDate"] = billing_resolution.creationDate
        data["updateDate"] = datetime.now()
        data["createdBy"] = billing_resolution.createdBy
        data["updateBy"] = g.user['name']
        billing_resolution = billing_resolution.import_data(data)

        session.add(billing_resolution)
        try:
            session.commit()
            response = jsonify({"ok": "ok"})
            return response
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_billing_resolution(billing_resolution_id):
        """
            Allow delete Billing resolution according to identifier

            :param billing_resolution_id identifier by brand to delete
            :exception KeyError whether a key fail
            :return status code
        """
        billing_resolution = session.query(BillingResolution).get(billing_resolution_id)
        if billing_resolution is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(billing_resolution)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except KeyError as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def get_billing_resolution_by_branch(branch_id):
        """
        Allow get billing resolutions for sales
        :param branch_id: branch id
        :return: billing resolution list
        """
        try:
            billing_resolutions = session.query(BillingResolution).filter(BillingResolution.branchId == branch_id,
                                                                          BillingResolution.isDeleted == 0,
                                                                          or_(BillingResolution.resolutionType == 'V',
                                                                              BillingResolution.resolutionType == 'C'),
                                                                          BillingResolution.isActive == 1).all()
            return billing_resolutions
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)
