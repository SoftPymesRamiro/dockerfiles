from ... import Base, session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, DECIMAL
from sqlalchemy.orm import relationship


class KitStage(Base):
    __tablename__ = 'kitstage'

    kitStageId = Column(Integer, primary_key=True)
    kitId = Column(ForeignKey(u'kits.kitId'), index=True)
    stageId = Column(ForeignKey(u'stage.stageId'), index=True)
    comments = Column(String(2000))

    kit = relationship(u'Kit')
    stage = relationship(u'Stage')

    def export_data(self):
        """

        :return:
        """
        return {
            "comments": self.comments,
            "kitId": self.kitId,
            "kitStageId": self.kitStageId,
            "stageId": self.stageId,
            "stage": self.stage,
            "kit": self.kit,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'kitStageId' in data:
            self.kitStageId = data['kitStageId']
        if 'kitId' in data:
            self.kitId = data['kitId']
        if 'stageId' in data:
            self.stageId = data['stageId']
        if 'comments' in data:
            self.comments = data['comments']
