from datetime import datetime
from ... import Base
from ...exceptions import ValidationError
from sqlalchemy import String, Integer, Column
from sqlalchemy.dialects.mysql import MEDIUMBLOB, CHAR, LONGBLOB
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Image(Base):
    """
    """
    __tablename__ = 'images'

    imageId = Column(Integer, primary_key=True, nullable=False)
    image = Column(LONGBLOB)
    type = Column(String(2))
    # idType = Column(CHAR(36))

    def export_data(self):
        """
        """
        return {
            'imageId': self.imageId,
            'image': self.image,
            'type': self.type,
            # 'idType': self.idType,
        }

    def import_data(self, data):
        """
        """
        self.imageId = data['imageId'],
        self.image = data['image'],
        self.type = data['type'],
        # self.idType = data['idType'],



