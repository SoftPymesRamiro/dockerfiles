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
from .sub_inventory_group_2 import SubInventoryGroup2
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from flask import jsonify,g
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class SubInventoryGroup1(Base):
    __tablename__ = "subinventorygroups1"

    subInventoryGroup1Id = Column(Integer, primary_key=True, nullable=False)
    inventoryGroupId = Column(Integer, ForeignKey('inventorygroups.inventoryGroupId'))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    commission = Column(DECIMAL(5, 2), default=0.0)
    discountPercentage = Column(DECIMAL(5, 2), default=0.0)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    subInventoryGroups2 = relationship("SubInventoryGroup2",
                                       primaryjoin=subInventoryGroup1Id == SubInventoryGroup2.subInventoryGroup1Id,
                                       cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to SubInventoryGroup
            :param  data
            :return SubInventoryGroup in JSON object

        """
        return {
            'subInventoryGroup1Id': data.subInventoryGroup1Id,
            'inventoryGroupId': data.inventoryGroupId,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'commission': data.commission,
            'discountPercentage': data.discountPercentage,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'subInventoryGroups2': [] if data.subInventoryGroups2 is None or len(data.subInventoryGroups2) == 0
            else [SubInventoryGroup2.export_data(sub2) for sub2 in data.subInventoryGroups2]
        }

    def import_data(self, data):
        """
            allow create a new  SubInventoryGroup from data element
            :param data information de new SubInventoryGroup
            :exception An erro occurrs when data not contains key needed by SubInventoryGroup
            :return SubInventoryGroup object
        """
        # try:
        if "subInventoryGroup1Id" in data:
            self.subInventoryGroup1Id = data["subInventoryGroup1Id"]

        self.name = data["name"]
        self.code = data["code"]

        self.inventoryGroupId = data["inventoryGroupId"]
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
        # except KeyError as e:
        #     raise ValidationError("Invalid paymentMethod: missing " + e.args[0])
        return self

    @staticmethod
    def get_sub_inventory_groups_1():
        """
            :return all SubInventoryGroup 
        """
        sub_inventory_group_1 = jsonify(
            data=[SubInventoryGroup1.export_data(sub_inventory_group_1)
                  for sub_inventory_group_1 in session.query(SubInventoryGroup1)
                                                      .order_by(SubInventoryGroup1.code)
                                                      .all()])
        return sub_inventory_group_1

    @staticmethod
    def get_sub_inventory_group_1(sub_inventory_group_1_id):
        """
            allow obtain SubInventoryGroup for to give a sub_inventory_group_1_id
            :param sub_inventory_group_1_id identifier by SubInventoryGroup to obtain
            :return SubInventoryGroup object in JSON format
        """
        sub_inventory_group_1 = session.query(SubInventoryGroup1).get(sub_inventory_group_1_id)
        if sub_inventory_group_1 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        sub_inventory_group_1 = SubInventoryGroup1.export_data(sub_inventory_group_1)
        response = jsonify(sub_inventory_group_1)
        return response

    @staticmethod
    def post_sub_inventory_group_1(data):
        """
            Allow create a new SubInventoryGroup from data
            :param data information by new SubInventoryGroup
            :exception An error occurs when a key in data dont set
            :return SubInventoryGroup objetc in JSON format
        """
        sub_inventory_group_1 = SubInventoryGroup1()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            sub_inventory_group_1.import_data(data)

            session.add(sub_inventory_group_1)
            session.commit()
            response = jsonify({"subInventoryGroup1Id": sub_inventory_group_1.subInventoryGroup1Id})
        except KeyError as e:
            raise ValidationError("Invalid SubInventoryGroup1: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_sub_inventory_group_1(sub_inventory_group_1_id):
        """
            allow detele a SubInventoryGroup according to identifier
            :param sub_inventory_group_1_id identifier by SubInventoryGroup to delete
            :exception KeyError occurs when database integrity database tiggered
            :return:
        """
        sub_inventory_group_1 = session.query(SubInventoryGroup1).get(sub_inventory_group_1_id)
        if sub_inventory_group_1 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(sub_inventory_group_1)
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
    def put_sub_inventory_group_1(sub_inventory_group_1_id, data):
        """
             Allow update a SubInventoryGroup for to give a identifier
             :param sub_inventory_group_1_id idnetifier by SubInventoryGroup to update
             :param data
             :exception KeyError occurs when a no found or key data dont fetch
             :return a SubInventoryGroup object in JSON format
        """
        if sub_inventory_group_1_id != data["subInventoryGroup1Id"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not sub_inventory_group_1_exist(data["subInventoryGroup1Id"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        sub_inventory_group_1 = session.query(SubInventoryGroup1).get(sub_inventory_group_1_id)
        try:
            data["creationDate"] = sub_inventory_group_1.creationDate
            data["createdBy"] = sub_inventory_group_1.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            sub_inventory_group_1 = sub_inventory_group_1.import_data(data)
            session.add(sub_inventory_group_1)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid sub_inventory_group_1: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def sub_inventory_group_1_exist(sub_inventory_group_1_id):
    """
        allow validate if SubInventoryGroup exist according to identifier
        :param sub_inventory_group_1_id
        sub_inventory_group_id identifier by SubInventoryGroup to search
        :return SubInventoryGroup object found in JSON format
    """
    return session.query(SubInventoryGroup1).filter(SubInventoryGroup1.subInventoryGroup1Id == sub_inventory_group_1_id).count()
