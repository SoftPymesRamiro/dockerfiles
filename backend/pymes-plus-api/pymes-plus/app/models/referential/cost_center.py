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
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, and_, or_
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from .division import Division
from .section import Section
from ...exceptions import ValidationError, InternalServerError
from flask import jsonify, g
from ... import session


class CostCenter(Base):
    __tablename__ = 'costcenters'
    costCenterId = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(50))
    branchId = Column(Integer, ForeignKey('branches.branchId'))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)
    divisions = relationship("Division",
                             primaryjoin=costCenterId == Division.costCenterId,
                             cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
        Allow export cost center object according to data information
        :param data: informationd e cost center to export
        :return: An cost center object in JSON format
        """
        return {
            'costCenterId': data.costCenterId,
            'name': data.name,
            'code': data.code,
            'branchId': data.branchId,
            'createdBy': data.createdBy,
            'creationDate': data.creationDate,
            'updateBy': data.updateBy,
            'isDeleted': data.isDeleted,
            'updateDate': data.updateDate,
            'divisions': [] if data.divisions is None or len(data.divisions) == 0
            else [Division.export_data(div) for div in data.divisions]
        }

    def import_data(self, data):
        """
        Allow create a cost-center from data parameter
        :param data: information of cost-center
        :raise: keyError
        :exception: An error occurs when a key in data is not set
        :return: cost-center object in JSON format
        """

        if "costCenterId" in data:
            self.costCenterId = data["costCenterId"]

        self.name = data["name"]
        self.code = data["code"]
        self.branchId = data["branchId"]

        if "createdBy" in data:
            self.createdBy = data["createdBy"]
        if "creationDate" in data:
            self.creationDate = data["creationDate"]
        if "updateBy" in data:
            self.updateBy = data["updateBy"]
        if "updateDate" in data:
            self.updateDate = data["updateDate"]
        if "isDeleted" in data:
            self.isDeleted = data["isDeleted"]

        return self

    @staticmethod
    def get_cost_centers():
        """
        Allow obtain all cost-centers
        :return: a JSON object with array the  cost centers object in JSON format
        """
        cost_centers = jsonify(data=[CostCenter.export_data(cost_center)
                                     for cost_center in session.query(CostCenter)
                                                               .order_by(CostCenter.code).all()])
        return cost_centers

    @staticmethod
    def get_cost_center(cost_center_id):
        """
        Allow obtain cost-center according to identifier
        :param cost_center_id: identifier by cost-center
        :return:  a JSON object with cost-center objecte in JSOn format
        """
        cost_center = session.query(CostCenter).get(cost_center_id)
        if cost_center is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        cost_center = cost_center.export_data(cost_center)
        response = jsonify(cost_center)
        return response

    @staticmethod
    def get_cost_centers_by_branch(branch_id):
        """
        Allow obtain cost-center according to branch_id
        :param branch_id: branch identifier
        :return: a cost-center object in JSON format
        """
        cost_centers = [CostCenter.export_data(cost_center)
                        for cost_center in session.query(CostCenter)
                                                  .options(joinedload(CostCenter.divisions)
                                                           .joinedload(Division.sections)
                                                           .joinedload(Section.dependencies))
                                                  .filter(CostCenter.branchId == branch_id)
                                                  .order_by(CostCenter.code)
                                                  .all()]
        response = jsonify(data=cost_centers)
        if len(cost_centers) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def post_cost_center(data):
        """
        Allow update a cost-center according to information param
        :param data: information by changed cost-center
        :raise: ValidationError
        :exception: An error occures when a key in data is not set
        :return: a JSON object
        """
        cost_center = CostCenter()
        # if cost_center_exist_by_code(data["code"]):
        #     # revisa si ya hay una forma con ese codigo
        #     response = jsonify({'error': 'bad request', 'message': 'El centro de costo ya existe'})
        #     response.status_code = 400
        #     return response

        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            # TODO: Colocar el nombre de autenticacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            cost_center.import_data(data)

            session.add(cost_center)
            session.commit()
            response = jsonify({"costCenterId": cost_center.costCenterId})
        except KeyError as e:
            raise ValidationError("Invalid CostCenter: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_cost_center(cost_center_id):
        """
        Allow delete a cost-center for to give identifier
        :param cost_center_id: identifier by cost-center to delete
        :return: status code and result
        """
        cost_center = session.query(CostCenter).get(cost_center_id)
        if cost_center is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(cost_center)
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

    @staticmethod
    def put_cost_center(cost_center_id, data):
        """
        Allow update a cost-center according to identifier
        :param cost_center_id: identifier by cost-center to update
        :param data: information by change to cost-center
        :raise: ValidationError
        :exception: An error occurs when a key in data is not set
        :return: status coder and result
        """
        if cost_center_id != data["costCenterId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not cost_center_exist(data["costCenterId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        cost_center = session.query(CostCenter).get(cost_center_id)
        try:
            data["creationDate"] = cost_center.creationDate
            data["createdBy"] = cost_center.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            cost_center = cost_center.import_data(data)
            session.add(cost_center)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid cost_center: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def cost_center_exist(cost_center_id):
    """
    Allow seek a cost center according to identifier
    :param cost_center_id: identifier by cost-center
    :return: int-- quentities of centers-cost that exist
    """
    return session.query(CostCenter).filter(CostCenter.costCenterId == cost_center_id).count()


def cost_center_exist_by_code(cost_center_code):
    """
    Allow seek a cost center according to center code
    :param cost_center_code: code fo cost center by seek
    :return: int-- quentities of centers-cost that exist
    """
    return session.query(CostCenter).filter(CostCenter.code == cost_center_code).count()

