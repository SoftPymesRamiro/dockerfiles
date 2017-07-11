from ... import Base, session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, DECIMAL
from sqlalchemy.orm import relationship


class KitLabor(Base):
    __tablename__ = 'kitlabors'

    kitLaborId = Column(Integer, primary_key=True)
    kitId = Column(ForeignKey(u'kits.kitId'), index=True)
    roleEmployeeId = Column(ForeignKey(u'roleemployees.roleEmployeeId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    quantity = Column(DECIMAL(16, 4), default=0.0)
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    kit = relationship(u'Kit')
    roleemployee = relationship(u'RoleEmployee')
    stage = relationship(u'Stage')


    def export_data(self):
        """
            allow export KitAsset data
            :return stage object in JSON format
        """
        return {
            'kitLaborId': self.kitLaborId,
            'kitId': self.kitId,
            'roleEmployeeId': self.roleEmployeeId,
            'stageId': self.stageId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'quantity': self.quantity,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'kitLaborId' in data:
            self.kitLaborId = data['kitLaborId']
        if 'kitId' in data:
            self.kitId = data['kitId']
        if 'roleEmployeeId' in data:
            self.roleEmployeeId = data['roleEmployeeId']
        if 'stageId' in data:
            self.stageId = data['stageId']
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