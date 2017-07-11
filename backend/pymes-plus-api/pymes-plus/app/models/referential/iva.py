# coding=utf-8
from datetime import datetime
from ... import Base
from flask import jsonify
from ... import session
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref


class IVA(Base):
    __tablename__ = "iva"

    ivaId = Column(Integer, primary_key=True, nullable=False)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(TINYINT)
    code = Column(String(1))
    name = Column(String(50))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    def export_data(self):
        return {
            'ivaId': self.ivaId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'code': self.code,
            'name': self.name,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def export_data_simple(self):
        return {
            'ivaId': self.ivaId,
            'code': self.code,
            'name': self.name,
        }

    @staticmethod
    def get_iva():
        list_iva = jsonify(data=[iva.export_data_simple() for iva in session.query(IVA).all()])
        return list_iva


    @staticmethod
    def get_iva_by_search(*args):
        # args = (to_items)
        to_items = args[0]
        iva = []
        if to_items:
            # /api/v1/iva/search?to_items=true
            iva = session.query(IVA).filter(IVA.code == "G").first()
            result = {
                "purchaseIVA": None if iva is None else iva.export_data_simple(),
                "saleIVA": None if iva is None else iva.export_data_simple(),
            }
            return jsonify(result)

        response = jsonify(iva=iva)
        if len(iva) == 0:
            response = jsonify({'error':'Not Found','code': 404, 'message': 'Not Found'})
            response.status_code = 404
        return response
