from ... import Base, session
from sqlalchemy import Integer, Column, ForeignKey, DateTime, String, DECIMAL
from sqlalchemy.orm import relationship
from ...exceptions import InternalServerError


class KitItem(Base):
    __tablename__ = 'kititems'

    kitItemId = Column(Integer, primary_key=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    kitId = Column(ForeignKey(u'kits.kitId'), index=True)
    pieceId = Column(ForeignKey(u'pieces.pieceId'), index=True)
    articleId = Column(ForeignKey(u'items.itemId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    quantity = Column(DECIMAL(18, 5), default=0.0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    item = relationship(u'Item', foreign_keys=[articleId])
    kit = relationship(u'Kit', foreign_keys=[kitId])
    piece = relationship(u'Piece', foreign_keys=[pieceId])
    stage = relationship(u'Stage', foreign_keys=[stageId])

    def export_data(self):
        """

        :return:
        """
        return {
            'kitItemId': self.kitItemId,
            'stageId': self.stageId,
            'kitId': self.kitId,
            'pieceId': self.pieceId,
            'articleId': self.articleId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'quantity': self.quantity,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }

    def export_data_item(self):
        return {
            'kitId': self.kitId,
            'kitItemId': self.kitItemId,
            'itemId': self.articleId,
            'stageId': self.stageId,
            'code': self.item.code if self.item else None,
            'name': self.item.name if self.item else None,
            'measurementUnitCode': self.item.measurementUnit.code
            if self.item else None,
            'measurementUnitId': self.item.measurementUnitId,
            'quantity': self.quantity
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'kitItemId' in data:
            self.kitItemId = data['kitItemId']
        if 'stageId' in data:
            self.stageId = data['stageId']
        if 'kitId' in data:
            self.kitId = data['kitId']
        if 'pieceId' in data:
            self.pieceId = data['pieceId']
        if 'articleId' in data:
            self.articleId = data['articleId']
        if 'ItemId' in data:
            self.articleId = data['ItemId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'quantity' in data:
            self.quantity = data['quantity']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

    @staticmethod
    def get_kit_item_by_id(kit_id):
        """
        Allow get item's kit
        :param kit_id: kit id
        :return: kit item list object
        """
        try:
            kit_item = session.query(KitItem).filter(KitItem.kitId == kit_id).all()
            return kit_item
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)
