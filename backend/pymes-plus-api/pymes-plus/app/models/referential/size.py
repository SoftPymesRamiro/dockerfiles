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
from ... import Base
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, VARBINARY, ForeignKey, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ... import session


class Size(Base):
    __tablename__ = 'sizes'
    sizeId = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('companies.companyId'), nullable=False)
    code = Column(String(10))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        """
            Allow export size
            :return size object in JSON format
        """
        return {
            'sizeId': self.sizeId,
            'companyId': self.companyId,
            'code': self.code,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'updateDate': self.updateDate
        }

    def import_data(self, data):
        """
            Allow create data from information
            :param data infromation by new size
            :exception  An error occurs when a key in data is not set
            :return size object in JSON format
        """
        # try:
        if "sizeId" in data:
            self.sizeId = data["sizeId"]

        self.companyId = data["companyId"]
        self.code = data["code"]

        if "createdBy" in data:
            self.createdBy = data["createdBy"]
        if "creationDate" in data:
            self.creationDate = data["creationDate"]
        if "updateBy" in data:
            self.updateBy = data["updateBy"]
        if "updateDate" in data:
            self.updateDate = data["updateDate"]
        if "isDeleted" in data:
            self.isDeleted = data["isDeleted"]
        # except KeyError as e:
        #     raise ValidationError("Invalid color: missing " + e.args[0])
        return self

    @staticmethod
    def get_sizes():
        """
            Allow obtain all sizes
            :return array of sizes objects in JSON format
        """
        size = jsonify(data=[Size.export_data(size)
                             for size in session.query(Size).order_by(Size.code).all()])
        return size

    @staticmethod
    def get_size(size_id):
        """
            Allow obtain a size for to give a identifier
            :param size_id identifier by size
            :return size object in JSON format
        """
        size = session.query(Size).get(size_id)
        if size is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        size = size.export_data()
        response = jsonify(size)
        return response

    @staticmethod
    def get_size_by_company(company_id):
        """
            get size according to company identifier
            :param company_id idnetifier by size company
            @rerutn array od size objects in JSON format
        """
        sizes = [sizes.export_data() for sizes in session.query(Size).filter(Size.companyId == company_id)]
        response = jsonify(data=sizes)
        if len(sizes) == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
        return response

    @staticmethod
    def get_size_by_search(search):
        """
            Allow seek size according to match search pattern
            :param string search pattern to size to search
            :return array with size objects in JSON format
        """
        search = "" if search is None else search.strip()
        words = search.split(' ', 1) if search is not None else None
        size = [size.export_data()
                for size in session.query(Size).filter(
                or_(
                    True if search == "" else None,
                    or_(*[Size.code.like('%{0}%'.format(s)) for s in words])
                )).order_by(Size.code)]
        response = jsonify(data=size)
        return response

    @staticmethod
    def post_size(data):
        """
            Allow create a new size
            :param data information by a new size
            :exception KeyError, a error occurs when a key in data is not set
            :return size object in JSON format
        """
        size = Size()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            size.import_data(data)

            session.add(size)
            session.commit()
            response = jsonify({"sizeId": size.sizeId})
        except KeyError as e:
            raise ValidationError("Invalid size: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_size(size_id):
        """
            Allow delete a size objects
            :param size_id identifier by size to delete
            :exception KeyError a error occurs when a key in data is not set
            :return --
        """
        size = session.query(Size).get(size_id)
        if size is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(size)
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

    @staticmethod
    def put_size(size_id, data):
        """
            Allow update a size object for to give a identifier
            :param size_id identifier by size to update
            :param data information to update
            :exception keyError a errors cocurs when a key in data is not set
            :return a size object
        """
        if size_id != data["sizeId"]:
            response = jsonify({"error": "bad request", "message": "identificador Incorrecto"})
            response.status_code = 400
            return response
        if not size_exist(data["sizeId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        size = session.query(Size).get(size_id)

        try:
            data["creationDate"] = size.creationDate
            data["createdBy"] = size.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            size = size.import_data(data)
            session.add(size)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid size: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def size_exist(size_id):
    """
        Allow seek a size accoirding to size_id
        :param size_id identifier by size
        :return a size object in JSON format
    """
    return session.query(Size).filter(Size.sizeId == size_id).count()