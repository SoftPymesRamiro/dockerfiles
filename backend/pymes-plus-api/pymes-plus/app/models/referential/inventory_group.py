# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from datetime import datetime
from flask import jsonify, g
from ... import Base
from ... import session
from .sub_inventory_group_1 import SubInventoryGroup1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class InventoryGroup(Base):
    __tablename__ = "inventorygroups"

    inventoryGroupId = Column(Integer, primary_key=True, nullable=False)
    companyId = Column(Integer, ForeignKey("companies.companyId"))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    commission = Column(DECIMAL(5, 2), default=0.0)
    discountPercentage = Column(DECIMAL(5, 2), default=0.0)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    subInventoryGroups1 = relationship("SubInventoryGroup1",
                                       primaryjoin=inventoryGroupId == SubInventoryGroup1.inventoryGroupId,
                                       cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):

        return {
            'inventoryGroupId': data.inventoryGroupId,
            'companyId': data.companyId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'commission': data.commission,
            'discountPercentage': data.discountPercentage,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'subInventoryGroups1': [] if data.subInventoryGroups1 is None or len(data.subInventoryGroups1) == 0
            else [SubInventoryGroup1.export_data(sub1) for sub1 in data.subInventoryGroups1]
        }

    def import_data(self, data):
        try:
            if "inventoryGroupId" in data:
                self.inventoryGroupId = data["inventoryGroupId"]
            self.name = data["name"]
            self.code = data["code"]
            self.companyId = data["companyId"]
            if "commission" in data:
                self.commission = data["commission"]
            if "discountPercentage" in data:
                self.discountPercentage = data["discountPercentage"]
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
        except KeyError as e:
            raise ValidationError("Invalid paymentMethod: missing " + e.args[0])
        return self

    @staticmethod
    def get_inventory_group_all():
        """
        Allow obtain all countries
        :return: JSON object with contry array, ordered by code
        """
        inventory = jsonify(data=[InventoryGroup.export_data(inventory)
                                  for inventory in session.query(InventoryGroup).
                            order_by(InventoryGroup.code).all()])
        return inventory


    @staticmethod
    def get_inventory_group_byId(inventory_group_id):
        inventory = session.query(InventoryGroup).get(inventory_group_id)
        if inventory is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        inventory = InventoryGroup.export_data(inventory)
        response = jsonify(inventory)
        return response

    @staticmethod
    def get_inventory_group_by_company(**kwargs):
        company_id = kwargs.get("company_id")
        inventory = [InventoryGroup.export_data(inventory)
                     for inventory in session.query(InventoryGroup)
                                             .filter(InventoryGroup.companyId == company_id)
                                             .order_by(InventoryGroup.code)
                                             .all()]

        response = jsonify(data=inventory)

        if len(inventory) == 0:
            response = jsonify({'error': "Not Found", 'code': 404, 'message': 'Not Found'})
            response.status_code = 404

        return response

    @staticmethod
    def post_inventory_group(data):
        inventory = InventoryGroup()

        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            inventory.import_data(data)

            session.add(inventory)
            session.commit()
            response = jsonify({"inventoryGroupId": inventory.inventoryGroupId})
        except KeyError as e:
            raise ValidationError("Invalid InventoryGroup: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_inventory_group(inventory_group_id):
        inventory = session.query(InventoryGroup).get(inventory_group_id)
        if inventory is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(inventory)
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

    @staticmethod
    def put_inventory_group(inventory_group_id, data):
        if inventory_group_id != data["inventoryGroupId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not inventory_exist(data["inventoryGroupId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        inventory = session.query(InventoryGroup).get(inventory_group_id)
        try:
            data["creationDate"] = inventory.creationDate
            data["createdBy"] = inventory.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            inventory = inventory.import_data(data)
            session.add(inventory)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid inventory: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def inventory_exist(inventory_group_id):
    return session.query(InventoryGroup).filter(InventoryGroup.inventoryGroupId == inventory_group_id).count()
