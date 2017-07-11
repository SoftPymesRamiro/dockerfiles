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
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, and_
from sqlalchemy.orm import relationship
from .. import Branch, DocumentType
from ...exceptions import ValidationError, IntegrityError
from flask import jsonify, abort, g
from datetime import datetime


class Consecutive(Base):
    """ 
    This class
    """

    __tablename__ = 'consecutives'

    consecutiveId = Column(Integer, primary_key=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    billingResolutionId = Column(ForeignKey(u'billingresolutions.billingResolutionId'), index=True)
    documentTypeId = Column(ForeignKey(u'documenttypes.documentTypeId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    lastConsecutive = Column(Integer)

    billingresolution = relationship(u'BillingResolution', foreign_keys=[billingResolutionId])
    branch = relationship(u'Branch')
    documenttype = relationship(u'DocumentType', foreign_keys=[documentTypeId])

    def export_data_short(self):
        """
        
        """
        return {
            'consecutiveId': self.consecutiveId,
            'branchId': self.branchId,
            'billingResolutionId': self.billingResolutionId,
            'documentTypeId': self.documentTypeId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'lastConsecutive': int(self.lastConsecutive),
        }

    def export_data(self):
        """

        """
        return {
            'consecutiveId': self.consecutiveId,
            'branchId': self.branchId,
            'billingResolutionId': self.billingResolutionId,
            'documentTypeId': self.documentTypeId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'lastConsecutive': int(self.lastConsecutive),
            "name": '{0}{1}'.format("" if self.documentTypeId is None or self.documenttype is None else
                                    self.documenttype.shortWord + " - " + self.documenttype.name,
                                    "" if self.billingResolutionId is None or self.billingresolution is None else
                                    '{0}{1}{2}'.format(
                                        " " + self.billingresolution.resolution + ": " +
                                        "Factura de Venta " if self.billingresolution.resolutionType is "V" else
                                        "Factura POS " if self.billingresolution.resolutionType is "P" else
                                        "Cuenta de Cobro " if self.billingresolution.resolutionType is "C" else
                                        "",
                                        self.billingresolution.date + " " +
                                        "" if self.billingresolution.prefix is None else self.billingresolution.prefix,
                                        "({0})".format(self.billingresolution.consecutiveFrom + " - " +
                                                       self.billingresolution.consecutiveTo)
                                    )
                                    )
        }

    def import_data(self, data):
        """
        Allow create a consecutive from data parameter
        :param data: information of consecutive
        :raise: keyError
        :exception: An error occurs when a key in data is not set
        :return: consecutive object in JSON format
        """
        if "consecutiveId" in data:
            self.consecutiveId = data['consecutiveId']
        if "branchId" in data:
            self.branchId = data['branchId']
        if "billingResolutionId" in data:
            self.billingResolutionId = data['billingResolutionId']
        if "documentTypeId" in data:
            self.documentTypeId = data['documentTypeId']
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
        if "lastConsecutive" in data:
            self.lastConsecutive = data['lastConsecutive']

        return self

    @staticmethod
    def get_consecutive_by_search(**kwargs):
        short_word = kwargs.get('short_word')
        branch_id = kwargs.get('branch_id')
        billing_resolution_id = kwargs.get('billing_resolution_id')

        if branch_id and not short_word and not billing_resolution_id:
            consecutive = [Consecutive.export_data(import_query)
                           for import_query in session.query(Consecutive)
                               .filter(Consecutive.branchId == branch_id)]
            return jsonify(data=consecutive)

        elif short_word and branch_id:
            consecutive = session.query(Consecutive).join(DocumentType) \
                .filter(and_(DocumentType.shortWord == short_word,
                             Consecutive.branchId == branch_id,
                             Consecutive.billingResolutionId == billing_resolution_id
                                                       if billing_resolution_id else True)).first()
            if consecutive is None:
                document_type_id = session.query(DocumentType).filter(DocumentType.shortWord == short_word).all()

                new_consecutive = Consecutive()
                new_consecutive.branchId = branch_id
                new_consecutive.documentTypeId = document_type_id[0].documentTypeId
                new_consecutive.billingResolutionId = billing_resolution_id if billing_resolution_id else None
                new_consecutive.lastConsecutive = 0
                new_consecutive.isDeleted = 0
                new_consecutive.updateDate = datetime.now()
                new_consecutive.updateBy = g.user['name']
                new_consecutive.creationDate = datetime.now()
                new_consecutive.createdBy = g.user['name']

                session.add(new_consecutive)
                try:
                    session.commit()
                    consecutive = new_consecutive
                except Exception as e:
                    session.rollback()

            if consecutive is None:
                response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                response.status_code = 404
                return response

            response = jsonify(consecutive.export_data_short())
            return response

    @staticmethod
    def post_consecutive(data):
        """
        Allow create a consecutive
        :param data: information by change consecutive
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:
        """
        for to_change in data:
            # consecutive = Consecutive()

            if not "consecutiveId" in to_change:
                response = jsonify({'error': "Not Found", 'message': 'Not Found'})
                response.status_code = 404
                return response

            consecutive = session.query(Consecutive).get(to_change['consecutiveId'])
            to_change['creationDate'] = datetime.now()
            to_change['updateDate'] = datetime.now()
            to_change['createdBy'] = g.user['name']
            to_change['updateBy'] = g.user['name']

            consecutive.import_data(to_change)
            session.add(consecutive)

            try:
                session.flush()
            except Exception as e:
                session.rollback()
                response = jsonify({'code': 405, 'error': 'Method Not Allowed'})
                response.status_code = 405
                return response

        try:
            session.commit()
            # response = jsonify({'consecutiveId': consecutive.consecutiveId})
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            raise ValidationError('Invalid consecutive: missing ' + e.args[0])
        return response

    def consecutive_exist(consecutive_id):
        """
        Allow validate whether consecutive exist afor to give consecutive identifier
        :param consecutive_id: coutnry identifier to seek
        :return: consecutive object found
        """
        return session.query(Consecutive). \
            filter(Consecutive.consecutiveId == consecutive_id).count()
