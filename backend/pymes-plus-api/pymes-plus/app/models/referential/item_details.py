from datetime import datetime
from ... import Base
from .image import Image
from ...utils.image_converter import ImagesConverter
from ... import session
from ...exceptions import ValidationError
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship

# images = Table('images', Base.metadata,
#                      Column('imageId', Integer, ForeignKey('images.imageId'), primary_key=True),
#                      Column('itemImageId', Integer, ForeignKey('itemdetails.imageId')))


class ItemDetail(Base):
    __tablename__ = 'itemdetails'

    itemDetailId = Column(Integer, primary_key=True, nullable=False)
    itemId = Column(Integer, ForeignKey('items.itemId'))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    enabled = Column(TINYINT, default=None)
    favorite = Column(TINYINT, default=None)
    isDeleted = Column(TINYINT, default=None)
    # image = Column(VARBINARY(length=2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    imageId = Column(Integer)

    def export_data(self):
        # img = session.query(Image).filter(Image.imageId == self.imageId).first()
        # if img is tuple or img is list:
        #     img = None if img is None else img[0].image
        # elif img is None:
        #     pass
        # else:
        #     img = img.image
        return {
            'itemDetailId': self.itemDetailId,
            'itemId': self.itemId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'enabled': self.enabled,
            'favorite': self.favorite,
            'isDeleted': self.isDeleted,
            # 'image': ImagesConverter.img_convert_to_base64(img),
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'imageId': self.imageId,
        }

    def import_data(self, data):
        self.itemId = data['itemId']
        self.creationDate = data['creationDate']
        self.updateDate = data['updateDate']
        self.enabled = data['enabled']
        self.favorite = data['favorite']
        self.isDeleted = data['isDeleted']
        # self.image = data['image']
        self.createdBy = data['createdBy']
        self.updateBy = data['updateBy']
        self.imageId = data['imageId']
