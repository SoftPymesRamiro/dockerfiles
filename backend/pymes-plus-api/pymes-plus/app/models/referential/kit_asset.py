from ... import Base, session
from sqlalchemy import Integer, ForeignKey, String, DateTime, DECIMAL, Column
from sqlalchemy.orm import relationship


class KitAsset(Base):
    __tablename__ = 'kitassets'

    kitAssetId = Column(Integer, primary_key=True)
    kitId = Column(ForeignKey(u'kits.kitId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    assetId = Column(ForeignKey(u'assets.assetId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    quantity = Column(DECIMAL(16, 4), default=0.0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    asset = relationship(u'Asset', foreign_keys=[assetId])
    kit = relationship(u'Kit', foreign_keys=[kitId])
    stage = relationship(u'Stage', foreign_keys=[stageId])


    def export_data(self):
        """
            allow export KitAsset data
            :return stage object in JSON format
        """
        return {
            'kitAssetId' : self.kitAssetId,
            'kitId' : self.kitId,
            'stageId' : self.stageId,
            'assetId' : self.assetId,
            'creationDate' : self.creationDate,
            'updateDate' : self.updateDate,
            'isDeleted' : self.isDeleted,
            'quantity' : self.quantity,
            'createdBy' : self.createdBy,
            'updateBy' : self.updateBy
        }


    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'kitAssetId' in data:
            self.kitAssetId = data['kitAssetId']
        if 'kitId' in data:
            self.kitId = data['kitId']
        if 'stageId' in data:
            self.stageId = data['stageId']
        if 'assetId' in data:
            self.assetId = data['assetId']
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