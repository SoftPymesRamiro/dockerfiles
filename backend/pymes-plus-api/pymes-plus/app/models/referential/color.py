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
from sqlalchemy import String, Integer, Column, DateTime, and_, or_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from flask import jsonify, g
from ... import session
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Color(Base):
    __tablename__ = 'colors'
    colorId = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(50))
    createdBy = Column(String(50))
    creationDate = Column(DateTime, default=datetime.now())
    updateBy = Column(String(50))
    updateDate = Column(DateTime, default=datetime.now())
    isDeleted = Column(Integer, default=0)

    def export_data(self):
        """
        Return data by a color
        :return color object in JSON format
        """
        return {
            'colorId': self.colorId,
            'name': self.name,
            'code': self.code,
            'createdBy': self.createdBy,
            'creationDate': self.creationDate,
            'updateBy': self.updateBy,
            'isDeleted': self.isDeleted,
            'updateDate': self.updateDate
        }

    def import_data(self, data):
        """Allow import color from data object
            :param data informatio by a new color
            :exception KeyError an error occurs when key dont set in data
            :return create a new color from data param
        """
        try:
            if "colorId" in data:
                self.colorId = data["colorId"]
            if "name" in data:
                self.name = data["name"]
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
        except KeyError as e:
            raise ValidationError("Invalid color: missing " + e.args[0])
        return self

    @staticmethod
    def get_colors():
        """
            allow obtain all colors 
            :return an array of color objects in JSON format
        """
        color = jsonify(data=[color.export_data() for color in session.query(Color).order_by(Color.code).all()])
        return color

    @staticmethod
    def get_color(color_id):
        """
            get color for to give a identifier
            :param color_id indentifier by seek color
            :return color object in JSON format
        """
        color = session.query(Color).get(color_id)
        if color is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        color = color.export_data()
        response = jsonify(color)
        return response

    @staticmethod
    def get_color_by_search(search):
        """
            find color accoriding to name 
            :param search
            :return a color object in JSON format
        """
        search = "" if search is None else search.strip()
        words = search.split(' ', 1) if search is not None else None
        color = [color.export_data()
                for color in session.query(Color).filter(
                or_(
                    # Item.name == search,
                    # Item.code == search,
                    True if search == "" else None,
                    or_(*[Color.name.like('%{0}%'.format(s)) for s in words]),
                    or_(*[Color.code.like('%{0}%'.format(s)) for s in words])
                )).order_by(Color.name)]
        response = jsonify(data=color)
        return response

    @staticmethod
    def post_color(data):
        """
            create a new color from data param
            :param data information by create a new color
            :return a new color create in JSON format
        """
        color = Color()
        try:
            data["creationDate"] = datetime.now()
            data["updateDate"] = datetime.now()
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']
            color.import_data(data)

            session.add(color)
            session.commit()
            response = jsonify({"colorId": color.colorId})
        except KeyError as e:
            raise ValidationError("Invalid color: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_color(color_id):
        """
            allow delete a color object according to identifier
            :param color_id identifier by color
            :return
        """
        color = session.query(Color).get(color_id)
        if color is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(color)
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
    def put_color(color_id, data):
        """
            allow update values color
            :param color_id identifier by color toi update
            :param data new values by color
            :return color object  in JSON format
        """
        if color_id != data["colorId"]:
            response = jsonify({"error": "bad request", "message": "El item ya existe"})
            response.status_code = 400
            return response
        if not color_exist(data["colorId"]):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        color = session.query(Color).get(color_id)

        try:
            data["creationDate"] = color.creationDate
            data["createdBy"] = color.createdBy
            data["updateDate"] = datetime.now()
            data["updateBy"] = g.user['name']
            color = color.import_data(data)
            session.add(color)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            session.rollback()
            raise ValidationError("Invalid colors: missing " + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


def color_exist(color_id):
    """
        allow seek a color for to give identifier
        :param color_id identifier by color
        :return an color object found  in JSON format
    """
    return session.query(Color).filter(Color.colorId == color_id).count()