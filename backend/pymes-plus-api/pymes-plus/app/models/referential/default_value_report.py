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
from flask import jsonify
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, SMALLINT
from sqlalchemy.orm import relationship



class DefaultValueReport(Base):
    """

    """
    __tablename__ = "defaultvaluereports"

    defaultValueReportsId = Column(Integer, primary_key=True)
    documentTypeId = Column(Integer, ForeignKey("documenttypes.documentTypeId"))
    documentType = relationship("DocumentType")
    defaultValueId = Column(Integer, ForeignKey("defaultvalues.defaultValueId"))
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    selected = Column(TINYINT)
    isDeleted = Column(TINYINT)
    name = Column(String(100))
    reportName = Column(String(50))
    size = Column(String(5))
    format = Column(String(5))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    shortWord = Column(String(3))

    def export_data(self):
        """
        Allow export default value report object
        :return: default valuereport in Json format
        """
        return {
            "defaultValueReportsId": self.defaultValueReportsId,
            "documentTypeId": self.documentTypeId,
            "defaultValueId": self.defaultValueId,
            "creationDate": self.creationDate,
            "updateDate": self.updateDate,
            "selected": self.selected,
            "isDeleted": self.isDeleted,
            "name": self.name,
            "reportName": self.reportName,
            "size": self.size,
            "format": self.format,
            "createdBy": self.createdBy,
            "updateBy": self.updateBy,
            "shortWord": self.shortWord,
        }

    @staticmethod
    def export_data_format_list(data):
        """
            Allow export default value report object
            :return: default valuereport in Json format
            """
        return {
            "selected": data.selected,
            "name": data.name,
            "reportName": data.reportName,
            "format": data.format,
            "formatName": 'Predeterminado' if data.format.upper() == 'P'
            else 'Pre-Impreso' if data.format.upper() == 'F'
            else 'Media Carta' if data.format.upper() == 'M'
            else 'Tirilla' if data.format.upper() == 'T'
            else 'Media Carta Especial' if data.format.upper() == 'MV'
            else 'Diseño Especial' if data.format.upper() == 'SP' else ''
        }

    @staticmethod
    def get_default_value_report_by_search(**kwargs):
        from .default_value import DefaultValue
        short_word = kwargs.get('short_word')
        branch_id = kwargs.get('branch_id')

        default_value_id = session.query(DefaultValue.defaultValueId).filter(DefaultValue.branchId == branch_id)

        default_val_report = session.query(DefaultValueReport)\
                                    .filter(DefaultValueReport.defaultValueId == default_value_id,
                                            DefaultValueReport.shortWord == short_word).all()
        response = [DefaultValueReport.export_data_format_list(def_val_rep) for def_val_rep in default_val_report]

        if default_val_report is None:
            response = []

        return jsonify(data=response)


