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
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from flask import jsonify, g


class SubInventoryGroup3(Base):
    __tablename__ = "subinventorygroups3"

    subInventoryGroup3Id = Column(Integer, primary_key=True, nullable=False)
    subInventoryGroup2Id = Column(Integer, ForeignKey('subinventorygroups2.subInventoryGroup2Id'))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    commission = Column(DECIMAL(5,2), default=0.0)
    discountPercentage = Column(DECIMAL(5,2), default=0.0)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    @staticmethod
    def export_data(data):
        """
            allow obtain data according to SubInventoryGroup
            :param data
            :return SubInventoryGroup in JSON object

        """
        return {
            'subInventoryGroup3Id': data.subInventoryGroup3Id,
            'subInventoryGroup2Id': data.subInventoryGroup2Id,
            'creationDate': data.creationDate,
            'updateDate': data.updateDate,
            'isDeleted': data.isDeleted,
            'commission': data.commission,
            'discountPercentage': data.discountPercentage,
            'code': data.code,
            'name': data.name,
            'createdBy': data.createdBy,
            'updateBy': data.updateBy
        }

    def import_data(self, data):
        """
            allow create a new  SubInventoryGroup from data element
            :paramdata information de new SubInventoryGroup
            :exception An erro occurrs when data not contains key needed by SubInventoryGroup
            :return SubInventoryGroup object
        """
        # try:
        if "subInventoryGroup3Id" in data:
            self.subInventoryGroup3Id = data["subInventoryGroup3Id"]

        self.name = data["name"]
        self.code = data["code"]

        self.subInventoryGroup2Id = data["subInventoryGroup2Id"]
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
    def get_sub_inventory_groups_3():
        """
            :return all SubInventoryGroup 
        """
        sub_inventory_group_3 = jsonify(
            data=[SubInventoryGroup3.export_data(sub_inventory_group_3)
                  for sub_inventory_group_3 in session.query(SubInventoryGroup3)
                                                      .order_by(SubInventoryGroup3.code)
                                                      .all()])
        return sub_inventory_group_3

    @staticmethod
    def get_sub_inventory_group_3(sub_inventory_group_3_id):
        """
            allow obtain SubInventoryGroup for to give a sub_inventory_group_3_id
            :paramsub_inventory_grop_id identifier by SubInventoryGroup to obtain
            :return SubInventoryGroup object in JSON format
        """
        sub_inventory_group_3 = session.query(SubInventoryGroup3).get(sub_inventory_group_3_id)
        if sub_inventory_group_3 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        sub_inventory_group_3 = SubInventoryGroup3.export_data(sub_inventory_group_3)
        response = jsonify(sub_inventory_group_3)
        return response

    @staticmethod
    def post_sub_inventory_group_3(data):
        """
            @breif allow create a new SubInventoryGroup from data
            :paramdata information by new SubInventoryGroup
            :exception An error occurs when a key in data dont set
            :return SubInventoryGroup objetc in JSON format
        """
        sub_inventory_group_3 = SubInventoryGroup3()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            # TODO: Colocar el nombre de autenticacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            sub_inventory_group_3.import_data(data)

            session.add(sub_inventory_group_3)
            session.commit()
            response = jsonify({"subInventoryGroup3Id": sub_inventory_group_3.subInventoryGroup3Id})
        except KeyError as e:
            raise ValidationError("Invalid SubInventoryGroup3: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_sub_inventory_group_3(sub_inventory_group_3_id):
        """
            allow detele a SubInventoryGroup according to identifier
            :paramsub_inventory_group_3_id identifier by SubInventoryGroup to delete
            :exception KeyError occurs when database integrity database tiggered
            @retun
        """
        sub_inventory_group_3 = session.query(SubInventoryGroup3).get(sub_inventory_group_3_id)
        if sub_inventory_group_3 is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        session.delete(sub_inventory_group_3)
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
    def put_sub_inventory_group_3(sub_inventory_group_3_id, data):
        """
             Allow update a SubInventoryGroup for to give a identifier
             :paramsub_inventory_group_3_id idnetifier by SubInventoryGroup to update
             :exception KeyError occurs when a no found or key data dont fetch
             :return a SubInventoryGroup object in JSON format
        """
        if sub_inventory_group_3_id != data["subInventoryGroup3Id"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response
        if not sub_inventory_group_3_exist(data["subInventoryGroup3Id"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        sub_inventory_group_3 = session.query(SubInventoryGroup3).get(sub_inventory_group_3_id)
        try:
            data["creationDate"] = sub_inventory_group_3.creationDate
            data["createdBy"] = sub_inventory_group_3.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            sub_inventory_group_3 = sub_inventory_group_3.import_data(data)
            session.add(sub_inventory_group_3)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid sub_inventory_group_3: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def sub_inventory_group_3_exist(sub_inventory_group_3_id):
    """
        allow validate if SubInventoryGroup exist according to identifier
        :paramsub_inventory_group_3_id
        sub_inventory_group_3_id identifier by SubInventoryGroup to search
        :return SubInventoryGroup object found in JSON format
    """
    return session.query(SubInventoryGroup3).\
        filter(SubInventoryGroup3.subInventoryGroup3Id == sub_inventory_group_3_id).count()