# coding=utf-8
from datetime import datetime
from flask import jsonify,g
from ... import Base
from ... import session
from .sub_zones_1 import SubZone1
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from sqlalchemy import or_, and_, func

from .item import Item
from .kit_stage import KitStage
from .kit_item import KitItem
from .kit_labor import KitLabor
from .kit_asset import KitAsset


class Kit(Base):

    __tablename__ = 'kits'

    kitId = Column(Integer, primary_key=True)
    itemId = Column(ForeignKey(u'items.itemId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer, default=0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    item = relationship(u'Item', foreign_keys=[itemId])

    kitStages = relationship('KitStage', lazy='dynamic')
    kitItems = relationship(u'KitItem', lazy='dynamic')
    kitAsset = relationship(u'KitAsset', lazy='dynamic')
    kitLabor = relationship(u'KitLabor', lazy='dynamic')

    def export_data(self):
        """

        :return:
        """
        def export_stage(data):
            return {
                'kitStageId': data.kitStageId,
                'kitId': data.kitId,
                'stageId': data.stageId,
                'comments': data.comments,
                'code': data.stage.code,
                "name": "{} {}".format(data.stage.code if data.stage.code else "",
                                       data.stage.description if data.stage.description else ""),

                'kitItems': None if data.kit.kitItems is None else[
                    {
                        'kitId': kit_item.kitId,
                        'kitItemId': kit_item.kitItemId,
                        'itemId': kit_item.articleId,
                        'stageId': kit_item.stageId,
                        'code': kit_item.item.code if kit_item.item else None,
                        'name': kit_item.item.name if kit_item.item else None,
                        'measurementUnitCode': kit_item.item.measurementUnit.code
                        if kit_item.item else None,
                        'quantity': kit_item.quantity

                     } for kit_item in list(filter(lambda x: x.stageId == data.stageId , data.kit.kitItems))
                ],
                'kitAssets': None if data.kit.kitAsset is None else[
                    {
                        'kitId': kit_asset.kitId,
                        'kitAssetId': kit_asset.kitAssetId,
                        'assetId': kit_asset.assetId,
                        'stageId': kit_asset.stageId,
                        'code': kit_asset.asset.code if kit_asset.asset else None,
                        'name': kit_asset.asset.name if kit_asset.asset else None,
                        'quantity': kit_asset.quantity

                    } for kit_asset in list(filter(lambda x: x.stageId == data.stageId, data.kit.kitAsset))
                ],
                'kitLabors': None if data.kit.kitLabor is None else[
                    {
                        'kitId': kit_labor.kitId,
                        'kitLaborId': kit_labor.kitLaborId,
                        'stageId': kit_labor.stageId,
                        'roleEmployeeId': kit_labor.roleEmployeeId,
                        'code': kit_labor.roleemployee.code if kit_labor.roleemployee else None,
                        'name': kit_labor.roleemployee.name if kit_labor.roleemployee else None,
                        'quantity': kit_labor.quantity

                    } for kit_labor in list(filter(lambda x: x.stageId == data.stageId , data.kit.kitLabor))
                ],
            }

        return {
            'kitId': self.kitId,
            'itemId': self.itemId,
            "kitStages": None if self.kitStages is None else[
                export_stage(data) for data in self.kitStages
            ],
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'kitId' in data:
            self.kitId = data['kitId']
        if 'itemId' in data:
            self.itemId = data['itemId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self


    @staticmethod
    def get_kits():
        """
        :return all kits ordered by code in JSON object
        """
        kits = jsonify(data=[Kit.export_data(kits) for kits in session.query(Kit).order_by(Kit.creationDate).all()])
        return kits

    @staticmethod
    def get_kit_byid(kit_id):
        """
            Allow obtain a kit according to kit_id
            :param item_id identifier by asset
            :return asset in JSON object
        """
        kit_found = session.query(Kit)\
            .filter(Kit.kitId == kit_id).first()

        if kit_found is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        kit_found = kit_found.export_data()
        response = jsonify(kit_found)
        return response

    @staticmethod
    def get_kit_byitemid(item_id):
        """
            Allow obtain a kit according to item_id
            :param item_id identifier by asset
            :return asset in JSON object
        """
        kit_found = session.query(Kit)\
            .join(KitStage, KitStage.kitId==Kit.kitId)\
            .join(KitAsset, KitStage.stageId==KitAsset.stageId)\
            .join(KitItem, KitItem.stageId==KitStage.stageId)\
            .join(KitLabor, KitLabor.stageId==KitStage.stageId)\
            .filter(Kit.itemId == item_id).first()

        if kit_found is None:
            kit_found = session.query(Kit) \
                .join(KitStage, KitStage.kitId == Kit.kitId) \
                .filter(Kit.itemId == item_id).first()

            if kit_found is None:
                kit_found = session.query(Kit) \
                    .filter(Kit.itemId == item_id).first()

                if kit_found is None:
                    response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                    response.status_code = 404
                    return response

        kit_found = kit_found.export_data()
        response = jsonify(kit_found)
        return response

    @staticmethod
    def export_item(data):
        """
        :return all kit with item data
        """
        return {
            "itemId": data.item.itemId,
            "nameItem": '{} {}'.format(data.item.code if data.item.code else "",
                                       data.item.name if data.item.name else ""),
            "companyId":data.item.companyId,
            "code":data.item.code,
            "name":data.item.name,
            "kitId": data.kitId
        }


    @staticmethod
    def search_kits(**kwargs):
        """

        :return:
        """
        simple = kwargs.get("simple")
        company_id = kwargs.get("company_id")
        code = kwargs.get("code")
        search = kwargs.get('search')
        words = kwargs.get('words')
        response = None

        kits = [Kit.export_item(kit)
                  for kit in session.query(Kit)
            .join(Item, Item.itemId==Kit.itemId)
            .filter(Item.companyId == company_id, Item.itemId==Kit.itemId,
                     or_(True if search == "" else None,
                         or_(*[Item.name.contains(word) for word in words]),
                         or_(*[Item.code.contains(word) for word in words])
                         )
            ).order_by(Item.code)]


        response = jsonify(data=kits)
        return response

    @staticmethod
    def post_kit(data):
        """

        :param data:
        :return:
        """
        kit = Kit()

        data["creationDate"] = datetime.now()
        data["updateDate"] = datetime.now()
        data["createdBy"] = g.user['name']
        data['isDeleted'] = 0
        data["updateBy"] = g.user['name']

        kit.import_data(data)
        session.add(kit)
        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        for kit_stage in data['kitStages']:
            kitstage = KitStage()
            kit_stage['kitId'] = kit.kitId
            kit_stage['comments'] = kit_stage["comments"]
            kit_stage['isDeleted'] = 0
            kit_stage['stageId'] = kit_stage['stageId']

            for to_change in kit_stage['kitAssets']:

                kitAsset = KitAsset()

                to_change['kitId'] = kit.kitId
                to_change['creationDate'] = datetime.now()
                to_change['updateDate'] = datetime.now()
                to_change['createdBy'] = g.user['name']
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitAsset.import_data(to_change)
                session.add(kitAsset)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            for to_change in kit_stage['kitItems']:
                kitItem = KitItem()

                to_change['kitId'] = kit.kitId
                to_change['creationDate'] = datetime.now()
                to_change['updateDate'] = datetime.now()
                to_change['createdBy'] = g.user['name']
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitItem.import_data(to_change)
                session.add(kitItem)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            for to_change in kit_stage['kitLabors']:
                kitLabor = KitLabor()

                to_change['kitId'] = kit.kitId
                to_change['creationDate'] = datetime.now()
                to_change['updateDate'] = datetime.now()
                to_change['createdBy'] = g.user['name']
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitLabor.import_data(to_change)
                session.add(kitLabor)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            kitstage.import_data(kit_stage)
            session.add(kitstage)
            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

        try:
            session.commit()
            response = jsonify({'kitId': kit.kitId})
        except KeyError as e:
            raise ValidationError('Invalid consecutive: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def put_kit(kit_id,data):
        """

        :param data:
        :return:
        """
        if kit_id != data['kitId']:
            response = jsonify({'error': 'bad request', 'message': 'Bad Request'})
            response.status_code = 400
            return response

        kit = session.query(Kit).get(kit_id)
        if kit is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        kit_assets = session.query(KitAsset)\
            .filter(KitAsset.kitId == kit_id).delete()
        kit_items = session.query(KitItem)\
            .filter(KitItem.kitId == kit_id).delete()
        kit_labors = session.query(KitLabor)\
            .filter(KitLabor.kitId == kit_id).delete()
        kit_stage = session.query(KitStage)\
            .filter(KitStage.kitId == kit_id).delete()

        try:
            session.flush()
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)

        for kit_stage in data['kitStages']:
            kitstage = KitStage()
            kit_stage['kitId'] = kit_id
            kit_stage['comments'] = kit_stage["comments"]
            kit_stage['isDeleted'] = 0
            kit_stage['stageId'] = kit_stage['stageId']

            for to_change in kit_stage['kitAssets']:

                kitAsset = KitAsset()

                to_change['kitId'] = kit_id
                to_change['updateDate'] = datetime.now()
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitAsset.import_data(to_change)
                session.add(kitAsset)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            for to_change in kit_stage['kitItems']:
                kitItem = KitItem()

                to_change['kitId'] = kit_id
                to_change['updateDate'] = datetime.now()
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitItem.import_data(to_change)
                session.add(kitItem)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            for to_change in kit_stage['kitLabors']:
                kitLabor = KitLabor()

                to_change['kitId'] = kit_id
                to_change['updateDate'] = datetime.now()
                to_change['isDeleted'] = 0
                to_change['updateBy'] = g.user['name']

                to_change['stageId'] = kit_stage['stageId']
                to_change['isDelete'] = False

                kitLabor.import_data(to_change)
                session.add(kitLabor)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            kitstage.import_data(kit_stage)
            session.add(kitstage)
            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

        try:
            session.commit()
            kit = session.query(Kit).get(kit_id)

            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']

            kit = kit.import_data(data)
            session.add(kit)
            session.commit()

            response = jsonify({"ok": "ok"})
        except KeyError as e:
            raise ValidationError('Invalid consecutive: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def delete_kit(kit_id):
        kit_found = session.query(Kit).get(kit_id)

        if kit_found is None:
            response = jsonify({'code': 404, 'message': 'Not Found'})
            response.status_code = 404
            return response

        kit_assets = session.query(KitAsset)\
            .filter(KitAsset.kitId == kit_id).delete()
        kit_items = session.query(KitItem)\
            .filter(KitItem.kitId == kit_id).delete()
        kit_labors = session.query(KitLabor)\
            .filter(KitLabor.kitId == kit_id).delete()
        kit_stage = session.query(KitStage)\
            .filter(KitStage.kitId == kit_id).delete()

        session.flush()

        session.delete(kit_found)
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