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
from flask import jsonify,g
from ... import session
from sqlalchemy import String, Integer, Column, DateTime, DECIMAL, ForeignKey,and_, or_
from sqlalchemy.dialects.mysql import TINYINT, VARBINARY
from sqlalchemy.orm import relationship, backref
from sqlalchemy.exc import IntegrityError as sqlIntegrityError
from ...exceptions import ValidationError, InternalServerError, IntegrityError
from .dian_form_concept import DianFormConcept
from .dian_concept import DianConcept
from math import ceil

class DianForm(Base):
    __tablename__ = 'dianforms'

    dianFormId = Column(Integer, primary_key=True)
    companyId = Column(ForeignKey(u'companies.companyId'), index=True)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    isDeleted = Column(Integer)
    code = Column(String(4))
    name = Column(String(200))
    version = Column(String(2))
    createdBy = Column(String(50))
    updateBy = Column(String(50))

    company = relationship(u'Company', foreign_keys=[companyId])
    dianConcepts = relationship('DianConcept', lazy='dynamic')

    def export_data(self):
        """
        Allow obtain dian_form data in session
        :return: an dian_form object in Json format
        """
        return {
            'dianFormId': self.dianFormId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'code': self.code,
            'name': self.name,
            'version': self.version,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'dianConcepts': None if self.dianConcepts is None else[
                DianConcept.export_data(dian_concept) for dian_concept in self.dianConcepts
            ],
        }

    def export_data_light(self):
        """
        Allow obtain dian_form data in session
        :return: an dian_form object in Json format
        """
        return {
            'dianFormId': self.dianFormId,
            'companyId': self.companyId,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'isDeleted': self.isDeleted,
            'code': self.code,
            'name': self.name,
            'version': self.version,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy
        }

    def import_data(self, data):
        """
        Allow create dian_form fro data information
        :param data: information of dian_form
        :raise: KeyError
        :exception: An error occurs when a key in data is not set
        :return:  dian_form object
        """
        if 'dianFormId' in data:
            self.dianFormId = data['dianFormId']
        if 'companyId' in data:
            self.companyId = data['companyId']
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'code' in data:
            self.code = data['code']
        if 'name' in data:
            self.name = data['name']
        if 'version' in data:
            self.version = data['version']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']

        return self


    @staticmethod
    def get_dian_forms():
        dian_form = [DianForm.export_data_light(dian_form)
                                   for dian_form in session.query(DianForm)
                         .order_by(DianForm.code).all()]

        dian_form = jsonify(data=dian_form)
        return dian_form

    @staticmethod
    def get_dian_form(dian_form_id):
        dian_form = session.query(DianForm).get(dian_form_id)
        if dian_form is None:
            response = jsonify({'error': "Not Found", 'message': 'Not Found'})
            response.status_code = 404
            return response

        dian_form = DianForm.export_data(dian_form)
        response = jsonify(dian_form)
        return response


    @staticmethod
    def search_dian_forms(**kwargs):
        """

        :param kwargs:
        :return:
        """
        by_param = kwargs.get("by_param")
        simple = kwargs.get("simple")
        search = kwargs.get("search")
        words = kwargs.get("words")
        code = kwargs.get("code")
        company_id = kwargs.get("company_id")

        paginate = kwargs.get("paginate")
        page_size = kwargs.get("page_size")
        page_number = kwargs.get("page_number")

        if by_param:
            f = None

        if simple and code and company_id:
            form_found = session.query(DianForm). \
                filter(and_(DianForm.code == code,
                            DianForm.companyId == company_id)).first()

            if form_found:
                form_found = DianForm.export_data(form_found)
                response = jsonify(form_found)
                return response

        if company_id and not paginate:
            text_search = "" if search is None else str(search).strip()
            words = text_search.split(' ', 1) if text_search is not None else None

            list_dianform = [DianForm.export_data(dian_form)
                   for dian_form in session.query(DianForm).filter(and_(DianForm.companyId == company_id,
                                    or_(or_(*[DianForm.code.contains('%{0}%'.format(s)) for s in words]),
                                        or_(*[DianForm.name.contains('%{0}%'.format(s)) for s in words])
                                        ))).all()]

            response = jsonify(data=list_dianform)
            return response

        if paginate:
            list_forms = [form.export_data_light()
                          for form in session.query(DianForm)
                              .filter(and_(DianForm.companyId == company_id,
                    or_(
                        True if search == "" else None,
                        or_(*[DianForm.name.like('%{0}%'.format(s)) for s in words]),
                        or_(*[DianForm.code.like('%{0}%'.format(s)) for s in words])
                    )))
                              .limit(page_size)
                              .offset((int(page_number) - 1) * int(page_size))
                          ]
            total_count = session.query(DianForm) \
                .filter(and_(DianForm.companyId == company_id,
                             or_(
                                 True if search == "" else None,
                                 or_(*[DianForm.name.like('%{0}%'.format(s)) for s in words]),
                                 or_(*[DianForm.code.like('%{0}%'.format(s)) for s in words])
                             ))).count()
            total_pages = int(ceil(total_count / float(page_size)))
            response = jsonify({
                'listForms': list_forms,
                'totalCount': total_count,
                'totalPages': total_pages
            })
            return response


    @staticmethod
    def post_dian_form(data):
        """

        :param data:
        :return:
        """
        code_exist = session.query(DianForm)\
            .filter(DianForm.code == data["code"]).count()

        if code_exist > 0:
            response = jsonify({'error': 'bad request',
                                'message': 'El formulario ya existe'})
            response.status_code = 400
            return response

        dian_form = DianForm()

        data['creationDate'] = datetime.now()
        data['updateDate'] = datetime.now()
        data['createdBy'] = g.user['name']
        data['updateBy'] = g.user['name']
        dian_form.import_data(data)
        session.add(dian_form)

        try:
            session.flush()
        except:
            session.rollback()
            raise

        for concept in data['dianConcepts']:
            dian_concept = DianConcept()

            concept['dianFormId'] = dian_form.dianFormId
            concept['creationDate'] = datetime.now()
            concept['updateDate'] = datetime.now()
            concept['createdBy'] = g.user['name']
            concept['updateBy'] = g.user['name']

            dian_concept.import_data(concept)
            session.add(dian_concept)
            try:
                session.flush()
            except:
                session.rollback()
                raise

            for form_concept in concept['dianformconcepts']:
                dian_form_concept = DianFormConcept()

                form_concept['dianConceptId'] = dian_concept.dianConceptId
                form_concept['creationDate'] = datetime.now()
                form_concept['updateDate'] = datetime.now()
                form_concept['createdBy'] = g.user['name']
                form_concept['updateBy'] = g.user['name']

                dian_form_concept.import_data(form_concept)
                session.add(dian_form_concept)
                try:
                    session.flush()
                except:
                    session.rollback()
                    raise

        try:
            session.add(dian_form)
            session.commit()
            response = jsonify({'dianFormId': dian_form.dianFormId})

        except KeyError as e:
            raise ValidationError('Invalid dianForm: missing' + e.args[0])
        return response

    @staticmethod
    def put_dian_form(dian_form_id, data):
        """

        :param dian_form_id:
        :param data:
        :return:
        """
        if dian_form_id != data["dianFormId"]:
            response = jsonify({"error": "bad request", "message": 'Bad Request'})
            response.status_code = 400
            return response

        code_exist = session.query(DianForm)\
            .filter(DianForm.code == data["code"]).count()

        if code_exist == 0:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        dian_form = session.query(DianForm).get(dian_form_id)
        if dian_form is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        concept = session.query(DianConcept.dianConceptId)\
            .filter(DianConcept.dianFormId == dian_form_id).subquery()

        form_concept = session.query(DianFormConcept)\
            .filter(DianFormConcept.dianConceptId.in_(concept)).delete(synchronize_session='fetch')

        rule = session.query(DianConcept) \
            .filter(DianConcept.dianFormId == dian_form_id).delete()

        try:
            session.flush()
        except:
            session.rollback()
            raise


        for concept in data['dianConcepts']:
            dian_concept = DianConcept()

            concept['dianFormId'] = dian_form.dianFormId
            concept['creationDate'] = datetime.now()
            concept['updateDate'] = datetime.now()
            concept['createdBy'] = g.user['name']
            concept['updateBy'] = g.user['name']

            dian_concept.import_data(concept)
            session.add(dian_concept)
            try:
                session.flush()
            except:
                session.rollback()
                raise

            for form_concept in concept['dianformconcepts']:
                dian_form_concept = DianFormConcept()

                form_concept['dianConceptId'] = dian_concept.dianConceptId
                form_concept['creationDate'] = datetime.now()
                form_concept['updateDate'] = datetime.now()
                form_concept['createdBy'] = g.user['name']
                form_concept['updateBy'] = g.user['name']

                dian_form_concept.import_data(form_concept)
                session.add(dian_form_concept)
                try:
                    session.flush()
                except:
                    session.rollback()
                    raise

        try:
            session.add(dian_form)
            dian_form = session.query(DianForm).get(dian_form_id)

            data['updateDate'] = datetime.now()
            data['creationDate'] = dian_form.creationDate
            data["updateBy"] = g.user['name']

            dian_form.import_data(data)
            session.add(dian_form)
            session.commit()
            response = jsonify({"ok": "ok"})
        except KeyError as e:
            raise ValidationError('Invalid list_dian_form: missing' + e.args[0])
        return response

    @staticmethod
    def delete_dian_form(dian_form_id):
        """

        :param dian_form_id:
        :return:
        """
        dian_form = session.query(DianForm).get(dian_form_id)
        if dian_form is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        concept = session.query(DianConcept.dianConceptId) \
            .filter(DianConcept.dianFormId == dian_form_id).subquery()

        form_concept = session.query(DianFormConcept) \
            .filter(DianFormConcept.dianConceptId.in_(concept)).delete(synchronize_session='fetch')

        rule = session.query(DianConcept) \
            .filter(DianConcept.dianFormId == dian_form_id).delete()

        try:
            session.flush()
            session.delete(dian_form)
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