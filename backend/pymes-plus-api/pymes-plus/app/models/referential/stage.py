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
from math import ceil
from sqlalchemy import or_, and_, func


class Stage(Base):
    __tablename__ = 'stage'

    stageId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    state = Column(Integer, default=1, nullable=False)
    isDeleted = Column(Integer, default=0)
    finalStage = Column(Integer)
    code = Column(String(10))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    description = Column(String(200))

    company = relationship(u'Company')

    def export_data(self):
        """
            allow export stage data
            :return stage object in JSON format
        """
        return {
            'stageId': self.stageId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'state': bool(self.state),
            'isDeleted': self.isDeleted,
            'finalStage': self.finalStage,
            'code': self.code,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'description': self.description,
        }

    def import_data(self, data):
        """

        :param data:
        :return:
        """
        if 'stageId' in data:
            self.stageId = data['stageId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'state' in data:
            self.state = data['state']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'finalStage' in data:
            self.finalStage = data['finalStage']
        if 'code' in data:
            self.code = data['code']
        if 'comments' in data:
            self.comments = data['comments']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        if 'description' in data:
            self.description = data['description']

        return self

    @staticmethod
    def get_stages():
        """
        Allow obtain all stages
        :return: JSON object with stages array, ordered by code
        """
        countries = [Stage.export_data(stage)
                     for stage in session.query(Stage).order_by(Stage.code).all()]

        countries = jsonify(data=countries)
        return countries


    @staticmethod
    def get_stage(stage_id):
        """
        Allow obtain a stage according to identifier
        :param stage_id: stage identifier
        :return: JSON object whit stage object
        """
        stage = session.query(Stage).get(stage_id)
        if stage is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        stage = stage.export_data()
        response = jsonify(stage)
        return response

    @staticmethod
    def search_stage(**kwargs):
        """

        :param kwargs:
        :return:
        """

        by_param = kwargs.get("by_param")
        company_id = kwargs.get("company_id")

        search = kwargs.get("search")
        words = kwargs.get("words")
        code = kwargs.get("code")
        page_size = kwargs.get('page_size')
        page_number = kwargs.get('page_number')

        response = None

        if by_param:
            f = None
            if by_param == 'allNameStagesPage':
                def export_by_param(data):
                    return {
                        'stageId': data.stageId,
                        'code': data.code,
                        "name": "{} {}".format(data.code if data.code else "",
                                               data.description if data.description else ""),
                    }

            list_stages = [export_by_param(stage)
                          for stage in session.query(Stage)
                              .filter(and_(
                    Stage.companyId == company_id,
                    or_(
                        True if search == "" else None,
                        or_(*[func.CONCAT_WS('', Stage.code, Stage.description).like('%{0}%'.format(s)) for s
                              in words]),
                        or_(*[Stage.code.like('%{0}%'.format(s)) for s in words])
                    )))
                              .limit(page_size)
                              .offset((int(page_number) - 1) * int(page_size))]

            total_count = session.query(Stage) \
                .filter(and_(Stage.companyId == company_id,
                             or_(
                                 True if search == "" else None,
                                 or_(*[func.CONCAT_WS('', Stage.code, Stage.description).like('%{0}%'.format(s)) for s
                                       in words]),
                                 or_(*[Stage.code.like('%{0}%'.format(s)) for s in words])
                             ))).count()

            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listStages': list_stages,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response


        if (not code) and company_id:
            imports_founds = [Stage.export_data(import_query)
                              for import_query in session.query(Stage)
                                  .filter(and_(Stage.companyId == company_id,
                                               or_(or_(*[Stage.code.like('%{0}%'.format(s)) for s in words]),
                                                   or_(*[Stage.comments.like('%{0}%'.format(s)) for s in words])
                                                   ))).order_by(Stage.code)]

            response = jsonify(data=imports_founds)
            return response

        if code and company_id:
            imports_founds = session.query(Stage). \
                filter(Stage.code == code, Stage.companyId == company_id).first()

            if imports_founds:
                imports_founds = Stage.export_data(imports_founds)
                response = jsonify(imports_founds)

            return response

        if response is None:
            response = jsonify(data=[])

        return response


    @staticmethod
    def post_stage(data):
        """
        Allow create a stage
        :param data: information by change stage
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:
        """
        stage = Stage()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']

        if stage_exist_by_code(data['code']):
            response = jsonify({'code': 400, 'message': 'stage already exits'})
            response.status_code = 400
            return response

        stage.import_data(data)
        session.add(stage)

        try:
            session.commit()
            response = jsonify({'stageId': stage.stageId})
        except KeyError as e:
            raise ValidationError('Invalid stage: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def put_stage(stage_id, data):
        """
        Allow update an stage identifier
        :param stage_id: stage identifier to update
        :param data:  information to change stage data
        :return:
        """
        if stage_id != data['stageId']:
            response = jsonify({'error': 'bad request', 'message': 'stage not exits'})
            response.status_code = 400
            return response

        if not stage_exist(data['stageId']):
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        stage = session.query(Stage).get(stage_id)

        try:
            data['creationDate'] = stage.creationDate
            data['createdBy'] = stage.createdBy
            data['updateDate'] = datetime.now()
            data['updateBy'] = g.user['name']
            stage = stage.import_data(data)
            session.add(stage)
            session.commit()
            response = jsonify({'ok': 'ok'})
        except KeyError as e:
            session.rollback()
            raise ValidationError('Invalid stage: missing ' + e.args[0])
        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response

    @staticmethod
    def delete_stage(stage_id):
        """
        Allow delete a stage according to identifier
        :param stage_id: stage identifier to eliminate
        :return:
        """
        stage = session.query(Stage).get(stage_id)
        if stage is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(stage)
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


def stage_exist(stage_id):
    """
    Allow validate whether stage exist a for to give stage identifier
    :param stage_id: stage identifier to seek
    :return: stage object found
    """
    return session.query(Stage).filter(Stage.stageId == stage_id).count()


def stage_exist_by_code(code):
    """
    Allow validate whether stage exist a for to give stage identifier
    :param stage_id: stage identifier to seek
    :return: stage object found
    """
    return session.query(Stage).filter(Stage.code == code).count()