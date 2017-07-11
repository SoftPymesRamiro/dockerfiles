# coding=utf-8
#########################################################
# All rights by SoftPymes Plus
# Referential module
#
# Date: 22-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from datetime import datetime
from flask import jsonify, g
from ... import Base
from .department import Department
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, and_, or_
from sqlalchemy.dialects.mysql import TINYINT, DECIMAL
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from sqlalchemy.orm import relationship, backref
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError

class Piece(Base):
    __tablename__ = 'pieces'

    pieceId = Column(Integer, primary_key=True)
    measurementUnitId = Column(ForeignKey(u'measurementunits.measurementUnitId'), index=True)
    inventoryPUCId = Column(ForeignKey(u'puc.pucId'), index=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer, default=0)
    state = Column(Integer, default=1)
    code = Column(String(50))
    name = Column(String(100))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    comments = Column(String(2000))

    company = relationship(u'Company')
    puc = relationship(u'PUC')
    measurementUnit = relationship(u'MeasurementUnit')


    def export_data(self):
        """
            allow export stage data
            :return stage object in JSON format
        """
        return {
            'pieceId':self.pieceId,
            'measurementUnitId':self.measurementUnitId,
            'inventoryPUCId':self.inventoryPUCId,
            'companyId':self.companyId,
            'creationDate':self.creationDate,
            'updateDate':self.updateDate,
            'isDeleted':self.isDeleted,
            'state':bool(self.state),
            'code':self.code,
            'name':self.name,
            'createdBy':self.createdBy,
            'updateBy':self.updateBy,
            'comments':self.comments
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'pieceId' in data:
            self.pieceId = data['pieceId']
        if 'measurementUnitId' in data:
            self.measurementUnitId = data['measurementUnitId']
        if 'inventoryPUCId' in data:
            self.inventoryPUCId = data['inventoryPUCId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'state' in data:
            self.state = data['state']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'comments' in data:
            self.comments = data['comments']

        return self

    @staticmethod
    def get_pieces():
        """
        Allow obtain all pieces
        :return: JSON object with pieces array, ordered by code
        """
        pieces = [Piece.export_data(piece)
                     for piece in session.query(Piece).order_by(Piece.code).all()]

        pieces = jsonify(data=pieces)
        return pieces


    @staticmethod
    def get_piece(piece_id):
        """
        Allow obtain a piece according to identifier
        :param piece_id: piece identifier
        :return: JSON object whit piece object
        """
        piece = session.query(Piece).get(piece_id)
        if piece is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        piece = piece.export_data()
        response = jsonify(piece)
        return response

    @staticmethod
    def search_piece(**kwargs):
        """

        :param kwargs:
        :return:
        """

        by_param = kwargs.get("by_param")
        company_id = kwargs.get("company_id")

        search = kwargs.get("search")
        words = kwargs.get("words")
        code = kwargs.get("code")
        response = None

        if (not code) and  company_id:
            imports_founds = [Piece.export_data(import_query)
                              for import_query in session.query(Piece)
                                  .filter(and_(Piece.companyId == company_id,
                                            or_(or_(*[Piece.code.like('%{0}%'.format(s)) for s in words]),
                                              or_(*[Piece.name.like('%{0}%'.format(s)) for s in words])
                                              ))).order_by(Piece.code)]

            response = jsonify(data=imports_founds)
            return response

        if code and company_id:
            imports_founds = session.query(Piece).\
                filter(Piece.code == code, Piece.companyId == company_id).first()

            if imports_founds:
                imports_founds = Piece.export_data(imports_founds)
                response = jsonify(imports_founds)

            return response

        if response is None:
            response = jsonify(data=[])

        return response

    @staticmethod
    def post_piece(data):
        """
        Allow create a piece
        :param data: information by change piece
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:
        """
        piece = Piece()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        if piece_exist_by_code(data['code']):
            response = jsonify({'code': 400, 'message': 'piece code already exits'})
            response.status_code = 400
            return response

        piece.import_data(data)
        session.add(piece)

        try:
            session.commit()
            response = jsonify({'pieceId': piece.pieceId})
        except KeyError as e:
            raise ValidationError('Invalid piece: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def put_piece(piece_id, data):
        """
        Allow update an piece identifier
        :param piece_id: piece identifier to update
        :param data:  information to change piece data
        :return:
        """
        if piece_id != data['pieceId']:
            response = jsonify({'error': 'bad request', 'message': 'piece not exits'})
            response.status_code = 400
            return response

        if not piece_exist(data['pieceId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        piece = session.query(Piece).get(piece_id)

        try:
            data['creationDate'] = piece.creationDate
            data['createdBy'] = piece.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            piece = piece.import_data(data)
            session.add(piece)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid piece: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response



    @staticmethod
    def delete_piece(piece_id):
        """
        Allow delete a piece according to identifier
        :param piece_id: piece identifier to eliminate
        :return:
        """
        piece = session.query(Piece).get(piece_id)
        if piece is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(piece)
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


def piece_exist(piece_id):
    """
    Allow validate whether piece exist a for to give piece identifier
    :param piece_id: piece identifier to seek
    :return: piece object found
    """
    return session.query(Piece).filter(Piece.pieceId == piece_id).count()


def piece_exist_by_code(code):
    """
    Allow validate whether piece exist a for to give piece identifier
    :param piece_id: piece identifier to seek
    :return: piece object found
    """
    return session.query(Piece).filter(Piece.code == code).count()