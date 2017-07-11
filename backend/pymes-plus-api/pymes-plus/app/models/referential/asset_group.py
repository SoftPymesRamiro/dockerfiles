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


from ... import Base, session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from flask import jsonify, g
from datetime import datetime
from sqlalchemy import and_, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError


class AssetGroup(Base):
    __tablename__ = 'assetgroups'

    assetGroupId = Column(Integer, primary_key=True)
    branchId = Column(Integer, ForeignKey(u'branches.branchId'))
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    branch = relationship(u'Branch')


    def export_data(self):
        """
        Allow export a PUC object
        :return:  PUC object in JSON format
        """
        return {
            "assetGroupId": self.assetGroupId,
            "branchId": self.branchId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "isDeleted": self.isDeleted,
            "code": self.code,
            "name": self.name,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            # "branch": self.branch
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if "assetGroupId" in data:
            self.assetGroupId = data['assetGroupId']
        if "branchId" in data:
            self.branchId = data['branchId']
        if "creationDate" in data:
            self.creationDate = data['creationDate']
        if "updateDate" in data:
            self.updateDate = data['updateDate']
        if "isDeleted" in data:
            self.isDeleted = data['isDeleted']
        if "code" in data:
            self.code = data['code']
        if "name" in data:
            self.name = data['name']
        if "createdBy" in data:
            self.createdBy = data['createdBy']
        if "updateBy" in data:
            self.updateBy = data['updateBy']

        return self

    @staticmethod
    def search_asset_groups(**kwargs):
        """

        :return:
        """
        simple = kwargs.get("simple")
        branch_id = kwargs.get("branch_id")
        code = kwargs.get("code")
        search = kwargs.get('search')
        words = kwargs.get('words')
        response = None

        if branch_id and not simple:
            asset_groups = [asset_groups.export_data()
                                 for asset_groups in session.query(AssetGroup).filter(
                    and_(AssetGroup.branchId == branch_id,
                    or_(or_(*[AssetGroup.name.contains(word) for word in words]),
                        or_(*[AssetGroup.code.contains(word) for word in words])))
                ).order_by(AssetGroup.code)]

            response = jsonify(data=asset_groups)
            return response


        if simple:
            if branch_id and code:
                asset_group = session.query(AssetGroup).\
                    filter(and_(AssetGroup.branchId == branch_id,
                                AssetGroup.code == code)).first()

                if asset_group is None:
                    response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                    response.status_code = 404
                    return response

                asset_group = asset_group.export_data()

                return jsonify(asset_group)

            elif branch_id:
                list_asset_groups = [asset_group.export_data()
                                     for asset_group in session.query(AssetGroup).
                                         filter(AssetGroup.branchId == branch_id).all()]

                return jsonify(data=list_asset_groups)

        if response is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response


    @staticmethod
    def post_asset_group(data):
        """

        :param data:
        :return:
        """
        if asset_group_code_exist(data['code'], data['branchId']) > 0:
            response = jsonify({'error': 'Not Found', 'message': 'Asset group code ready'})
            response.status_code = 404
            return response

        new_asset_group = AssetGroup()
        try:
            data['creationDate'] = datetime.now()   #actualizo la clave fecha de creacion
            data['updateDate'] = datetime.now()     #actualizo la clave fecha de actualizacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            new_asset_group.import_data(data)
            session.add(new_asset_group)
            session.commit()
            response = jsonify({'assetGroupId': new_asset_group.assetGroupId})
        except Exception as e:
            raise ValidationError('Invalid new_asset_group: missing' + e.args[0])

        return response


    @staticmethod
    def put_asset_group(asset_group_id, data):
        """

        :param asset_group_id:
        :param data:
        :return:
        """
        update_asset_group = session.query(AssetGroup).get(asset_group_id)
        try:

            data['creationDate'] = update_asset_group.creationDate
            data['createdBy'] = update_asset_group.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']

            update_asset_group = update_asset_group.import_data(data)
            session.add(update_asset_group)
            session.commit()
            response = jsonify({'ok': 'ok'})

        except Exception as e:
            session.rollback()
            raise ValidationError('Invalid asset group: missing' + e.args[0])
        return response


    @staticmethod
    def delete_asset_group(asset_group_id):
        """

        :param asset_group_id:
        :return:
        """
        asset_group = session.query(AssetGroup).get(asset_group_id)

        if asset_group is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(asset_group)

        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except Exception as e:
            session.rollback()
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response


def asset_group_code_exist(import_code, branch_id):
    return session.query(AssetGroup)\
        .filter(and_(AssetGroup.code == import_code,
                     AssetGroup.branchId == branch_id)).count()