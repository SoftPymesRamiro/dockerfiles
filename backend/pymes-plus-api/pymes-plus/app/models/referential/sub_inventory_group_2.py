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
from .sub_inventory_group_3 import SubInventoryGroup3
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class SubInventoryGroup2(Base):
    __tablename__ = "subinventorygroups2"

    subInventoryGroup2Id = Column(Integer, primary_key=True, nullable=False)
    subInventoryGroup1Id = Column(Integer, ForeignKey('subinventorygroups1.subInventoryGroup1Id'))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    commission = Column(DECIMAL(5,2), default=0.0)
    discountPercentage = Column(DECIMAL(5,2), default=0.0)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    subInventoryGroups3 = relationship("SubInventoryGroup3",
                                       primaryjoin=subInventoryGroup2Id == SubInventoryGroup3.subInventoryGroup2Id,
                                       cascade="all, delete, delete-orphan")

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to SubInventoryGroup
            :param  data
            :return SubInventoryGroup in JSON object

        """
        return {
            'subInventoryGroup2Id': data.subInventoryGroup2Id,
            'subInventoryGroup1Id': data.subInventoryGroup1Id,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'commission': data.commission,
            'discountPercentage': data.discountPercentage,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy,
            'subInventoryGroups3': [] if data.subInventoryGroups3 is None or len(data.subInventoryGroups3) == 0
            else [SubInventoryGroup3.export_data(sub3) for sub3 in data.subInventoryGroups3]
        }

    def import_data(self, data):
        """
            allow create a new  SubInventoryGroup from data element
            :param data information de new SubInventoryGroup
            :exception An erro occurrs when data not contains key needed by SubInventoryGroup
            :return SubInventoryGroup object
        """
        # try:
        if "subInventoryGroup2Id" in data:
            self.subInventoryGroup2Id = data["subInventoryGroup2Id"]

        self.name = data["name"]
        self.code = data["code"]

        self.subInventoryGroup1Id = data["subInventoryGroup1Id"]
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
            # raise ValidationError("Invalid paymentMethod: missing " + e.args[0])
        return self

    @staticmethod
    def get_sub_inventory_groups_2():
        """
            allow obtain SubInventoryGroup for to give a sub_inventory_group_2_id
            :param sub_inventory_grop_id identifier by SubInventoryGroup to obtain
            :return SubInventoryGroup object in JSON format
        """
        sub_inventory_group_2 = jsonify(
            data=[SubInventoryGroup2.export_data(sub_inventory_group_2)
                  for sub_inventory_group_2 in session.query(SubInventoryGroup2)
                                                      .order_by(SubInventoryGroup2.code)
                                                      .all()])
        return sub_inventory_group_2

    @staticmethod
    def get_sub_inventory_group_2(sub_inventory_group_2_id):
        sub_inventory_group_2 = session.query(SubInventoryGroup2).get(sub_inventory_group_2_id)
        if sub_inventory_group_2 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        sub_inventory_group_2 = SubInventoryGroup2.export_data(sub_inventory_group_2)
        response = jsonify(sub_inventory_group_2)
        return response

    @staticmethod
    def post_sub_inventory_group_2(data):
        """
            @breif allow create a new SubInventoryGroup from data
            :param data information by new SubInventoryGroup
            :exception An error occurs when a key in data dont set
            :return SubInventoryGroup objetc in JSON format
        """
        sub_inventory_group_2 = SubInventoryGroup2()

        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            sub_inventory_group_2.import_data(data)

            session.add(sub_inventory_group_2)
            session.commit()
            response = jsonify({"subInventoryGroup2Id": sub_inventory_group_2.subInventoryGroup2Id})
        except KeyError as e:
            raise ValidationError("Invalid SubInventoryGroup2: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_sub_inventory_group_2(sub_inventory_group_2_id):
        """
            allow detele a SubInventoryGroup according to identifier
            :param sub_inventory_group_2_id identifier by SubInventoryGroup to delete
            :exception KeyError occurs when database integrity database tiggered
            @retun
        """
        sub_inventory_group_2 = session.query(SubInventoryGroup2).get(sub_inventory_group_2_id)
        if sub_inventory_group_2 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(sub_inventory_group_2)
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
    def put_sub_inventory_group_2(sub_inventory_group_2_id, data):
        """
             Allow update a SubInventoryGroup for to give a identifier
             :param sub_inventory_group_2_id idnetifier by SubInventoryGroup to update
             :exception KeyError occurs when a no found or key data dont fetch
             :return a SubInventoryGroup object in JSON format
        """
        if sub_inventory_group_2_id != data["subInventoryGroup2Id"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not sub_inventory_group_2_exist(data["subInventoryGroup2Id"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        sub_inventory_group_2 = session.query(SubInventoryGroup2).get(sub_inventory_group_2_id)
        try:
            data["creationDate"] = sub_inventory_group_2.creationDate
            data["createdBy"] = sub_inventory_group_2.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            sub_inventory_group_2 = sub_inventory_group_2.import_data(data)
            session.add(sub_inventory_group_2)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid sub_inventory_group_2: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def sub_inventory_group_2_exist(sub_inventory_group_2_id):
    """
        allow validate if SubInventoryGroup exist according to identifier
        :param sub_inventory_group_2_id
        sub_inventory_group_2_id identifier by SubInventoryGroup to search
        :return SubInventoryGroup object found in JSON format
    """
    return session.query(SubInventoryGroup2).filter(SubInventoryGroup2.subInventoryGroup2Id == sub_inventory_group_2_id).count()
