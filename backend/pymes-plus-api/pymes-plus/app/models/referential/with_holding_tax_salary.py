# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey
from sqlalchemy.orm import relationship
from  sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ... import session


class Withholdingtaxsalary(Base):
    __tablename__ = 'withholdingtaxsalaries'

    withholdingTaxSalaryId = Column(Integer, primary_key=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    initialUVT = Column(DECIMAL(9, 2), default=0.0)
    finalUVT = Column(DECIMAL(9, 2), default=0.0)
    percentage = Column(DECIMAL(5, 2), default=0.0)
    description = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    additionalUVT = Column(Integer)
    tableType = Column(Integer, default=2, nullable=False)


    def export_data(self):
        """

        :return return withholdingtaxsalaries in JSON object
        """
        return {
            'withholdingTaxSalaryId': self.withholdingTaxSalaryId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'initialUVT': self.initialUVT,
            'finalUVT': self.finalUVT,
            'percentage': self.percentage,
            'description': self.description,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'additionalUVT': self.additionalUVT,
            'tableType': self.tableType
        }


    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'withholdingTaxSalaryId' in data:
            self.withholdingTaxSalaryId = data['withholdingTaxSalaryId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'initialUVT' in data:
            self.initialUVT = data['initialUVT']
        if 'finalUVT' in data:
            self.finalUVT = data['finalUVT']
        if 'percentage' in data:
            self.percentage = data['percentage']
        if 'description' in data:
            self.description = data['description']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'additionalUVT' in data:
            self.additionalUVT = int(float(data['additionalUVT']))
        if 'tableType' in data:
            self.tableType = data['tableType']

        return self


    @staticmethod
    def get_withholdingtaxsalaries():
        """
        Allow obtain all pieces
        :return: JSON object with pieces array, ordered by code
        """
        withholdingtaxsalaries = [Withholdingtaxsalary.export_data(piece)
                     for piece in session.query(Withholdingtaxsalary).order_by(Withholdingtaxsalary.initialUVT).all()]

        withholdingtaxsalaries = jsonify(data=withholdingtaxsalaries)
        return withholdingtaxsalaries

    @staticmethod
    def get_withholdingtaxsalaries_byid(withholdingtaxsalaries_id):
        """
        return a withholdingtaxsalaries according to withholdingtaxsalaries id
        :param withholdingtaxsalaries_id  identifier by withholdingtaxsalaries
        :return withholdingtaxsalaries found for give to id in JSON object
        """
        with_holding_tax_salaries = session.query(Withholdingtaxsalary).get(withholdingtaxsalaries_id)
        with_holding_tax_salaries = with_holding_tax_salaries.export_data()
        return jsonify(with_holding_tax_salaries)


    @staticmethod
    def post_withholdingtaxsalaries(data):
        """
            create a withholdingtaxsalaries
            :paramdata by new withholdingtaxsalaries
            :raise: Exception
            :exception: data bad formed
            :return status code
        """

        for to_change in data:

            if not "withholdingTaxSalaryId" in to_change:
                withholdingtaxsalaries = Withholdingtaxsalary()

                to_change["creationDate"] = datetime.now()
                to_change["updateDate"] = datetime.now()
                to_change["createdBy"] = g.user['name']
                to_change["updateBy"] = g.user['name']

                withholdingtaxsalaries = withholdingtaxsalaries.import_data(to_change)
                session.add(withholdingtaxsalaries)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    response = jsonify({'code': 405, 'error': 'Method Not Allowed'})
                    response.status_code = 405
                    return response
            else:
                withholdingtaxsalaries = session.query(Withholdingtaxsalary).get(to_change['withholdingTaxSalaryId'])
                to_change['creationDate'] = datetime.now()
                to_change['updateDate'] = datetime.now()
                to_change['createdBy'] = g.user['name']
                to_change['updateBy'] = g.user['name']

                withholdingtaxsalaries.import_data(to_change)
                session.add(withholdingtaxsalaries)

                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    response = jsonify({'code': 405, 'error': 'Method Not Allowed'})
                    response.status_code = 405
                    return response

        try:
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            raise ValidationError('Invalid withholdingtaxsalaries: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_withholdingtaxsalaries(withholdingtaxsalaries_id):
        """
            delete a withholdingtaxsalaries for to gieve a identifier
            :param withholdingtaxsalaries_id: identifier by withholdingtaxsalaries
            :exception: An error occurred wheter bad formed data in database or keys no assigned
            :return status
        """
        withholdingtaxsalaries = session.query(Withholdingtaxsalary).get(withholdingtaxsalaries_id)

        if withholdingtaxsalaries is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(withholdingtaxsalaries)
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
            session.rollback()
            raise InternalServerError(e)


def withholdingtaxsalaries_exist(warehouse_id):
    """
        seek a warehouse for to give a warehouse id

        :param warehouse_id: identifier by warehouse
        :return warehouse data according to identifier

    """
    return session.query(Withholdingtaxsalary).filter(Withholdingtaxsalary.warehouseId == warehouse_id).count()