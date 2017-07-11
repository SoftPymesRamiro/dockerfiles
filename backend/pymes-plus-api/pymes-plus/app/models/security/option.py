# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from datetime import datetime
from ... import Base, session
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from ...exceptions import ValidationError, InternalServerError
from flask import g
from .rol import Rol


class Option(Base):
    """
    Option as a public model class.
    """
    __tablename__ = 'options'

    optionId = Column(Integer, primary_key=True)
    parent = Column(ForeignKey(u'options.optionId'), index=True)
    creationDate = Column(DateTime, default=datetime.now())
    updateDate = Column(DateTime, default=datetime.now())
    branchRequired = Column(Integer)
    isDeleted = Column(Integer, default=0)
    name = Column(String(100))
    code = Column(String(200))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    # url = Column(String(200))
    type = Column(Integer)

    parentObj = relationship(u'Option', remote_side=[optionId])

    def __init__(self):
        self.options_from_role = []

    def export_data(self):
        """
        Allow export option object to json
        :return: json object
        """
        return {
            'optionId': self.optionId,
            'parent': self.parent,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'branchRequired': self.branchRequired,
            'isDeleted': self.isDeleted,
            'name': self.name,
            'code': self.code,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            'type': self.type,
        }

    def export_data_simple(self):
        """
        Allow export option object to json simple
        :return: json object
        """
        return {
            'optionId': self.optionId,
            'parent': self.parent,
            'name': self.name,
            'code': self.code,
            'type': self.type,
        }

    def all_role_option_on_tree(self):
        """
        Allow build a clean tree's options
        :return: list options
        """
        try:
            options = session.query(Option).all()

            for opt in options:
                i = OptionSimple(opt.optionId, opt.name, opt.code, opt.parent, False, False, False, False, None, [])
                self.options_from_role.append(i)
            list_option_simple_parent = [i for i in self.options_from_role if i.parent is None]
            list_option_simple_parent = Option.order_parent_list(list_option_simple_parent)

            i = 0
            while i < len(list_option_simple_parent):
                item = list_option_simple_parent[i]
                item.childs = self.fill(item.option_id)

                if item.childs is None or (item.childs is not None and len(item.childs) == 0):
                    list_option_simple_parent.remove(item)
                    i -= 1
                i += 1
            return list_option_simple_parent
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    def fill(self, parent_option_id):
        if parent_option_id is None:
            return None

        return_list = [x for x in self.options_from_role if x.parent == parent_option_id]

        if return_list is not None and len(return_list) > 0:
            for j in return_list:
                j.childs = self.fill(j.option_id)
        return return_list

    @staticmethod
    def order_parent_list(list_option_simple_parent):
        """
        Allow return the tree parent of options
        :param list_option_simple_parent: list parent's options
        :return: sorted list options
        """
        # switch = {
        #     'ESTRUCTURACIÓN': lambda: 1,
        #     'PARAMETRIZACIÓN': lambda: 2,
        #     'TABLAS': lambda: 3,
        #     'CONTABILIDAD': lambda: 4,
        #     'NÓMINA': lambda: 5,
        #     'PRODUCCION': lambda: 6,
        #     'POS': lambda: 7,
        #     'OTROS PROCESOS': lambda: 8,
        #     'INFORMES': lambda: 9,
        #     'CONSULTAS': lambda: 10,
        #     'AYUDA': lambda: 11
        # }
        switch = {
            'Estructuración': lambda: 1,
            'Compras': lambda: 2,
            'Ventas': lambda: 3,
            'Inventario': lambda: 4,
            'Tesorería': lambda: 5,
            'Otras Contabilizaciones': lambda: 6,
            'Nómina': lambda: 7,
            'Producción': lambda: 8,
            'POS': lambda: 9,
            'Informes': lambda: 10,
            'Ayuda': lambda: 11
        }
        for i in list_option_simple_parent:
            try:
                i.order = switch[i.name]()
            except KeyError as e:
                raise ValidationError(e)
        return sorted(list_option_simple_parent, key=lambda x: x.order)

    # @staticmethod

    def get_options_by_rol_id(self, rol_id):
        try:
            from .rol_option import RolOption
            rol_option_list = session.query(RolOption)\
                .options(joinedload(RolOption.option))\
                .filter(RolOption.rolId == rol_id).all()
            self.options_from_role = []
            for rol_o in rol_option_list:
                i = OptionSimple(rol_o.option.optionId,
                                 rol_o.option.name,
                                 rol_o.option.code,
                                 rol_o.option.parent,
                                 rol_o.c,
                                 rol_o.r,
                                 rol_o.u,
                                 rol_o.d,
                                 None,
                                 [])
                self.options_from_role.append(i)
            list_option_simple_parent = [x for x in self.options_from_role if x.parent is None]
            list_option_simple_parent = Option.order_parent_list(list_option_simple_parent)

            i = 0
            while i < len(list_option_simple_parent):
                item = list_option_simple_parent[i]
                item.childs = self.fill(item.option_id)

                if item.childs is None or (item.childs is not None and len(item.childs) == 0):
                    list_option_simple_parent.remove(item)
                    i -= 1
                i += 1
            return list_option_simple_parent

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def save_profile(data):
        """
        Allow save profile
        :param data: data object with options
        :return: message
        """
        try:
            from .rol_option import RolOption
            rol = Rol()
            profile = data['ProfileOptions']
            rol.name = data['name']
            rol.createdBy = g.user['name']
            rol.creationDate = datetime.now()
            rol.updateBy = g.user['name']
            rol.updateDate = datetime.now()

            session.add(rol)
            session.flush()

            for item in profile:
                ro = RolOption()
                ro.import_data(item)
                ro.rolId = rol.rolId
                ro.createdBy = g.user['name']
                ro.creationDate = datetime.now()
                ro.updateBy = g.user['name']
                ro.updateDate = datetime.now()
                session.add(ro)

            session.flush()
            session.commit()
            return {'data': 'Perfil Creado Correctamente'}
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def update_profile(profile_id, data):
        """
        Allow update a profile
        :param profile_id: profile id
        :param data: profile data object
        :return: Response string
        """
        try:
            from .rol_option import RolOption
            rol = session.query(Rol).filter(Rol.rolId == profile_id).first()
            if rol is None:
                raise ValidationError('Objeto no encontrado')
            rol.import_data(data)
            rol.updateBy = g.user['name']
            rol.updateDate = datetime.now()

            session.add(rol)
            session.flush()

            rol_options_to_delete = session.query(RolOption).filter(RolOption.rolId == rol.rolId).all()
            [session.delete(i) for i in rol_options_to_delete]
            session.flush()

            for item in data['ProfileOptions']:
                ro = RolOption()
                ro.import_data(item)
                ro.rolId = rol.rolId
                ro.createdBy = g.user['name']
                ro.creationDate = datetime.now()
                ro.updateBy = g.user['name']
                ro.updateDate = datetime.now()
                session.add(ro)

            session.flush()
            session.commit()

            return {'data': 'Perfil Actualizado Correctamente'}

        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    @staticmethod
    def delete_profile(profile_id):
        """
        Allow delete profile
        :param profile_id: profile id
        :return: Response string
        """
        try:
            from .rol_option import RolOption
            from .rol import Rol
            from .user_branch_role import UserBranchRole
            rol = session.query(Rol).get(profile_id)
            if rol is None:
                raise ValidationError('Objeto no encontrado')

            rol_options_to_delete = session.query(RolOption).filter(RolOption.rolId == rol.rolId).all()
            [session.delete(i) for i in rol_options_to_delete]

            rol_user = session.query(UserBranchRole).filter(UserBranchRole.rolId == rol.rolId).first()
            if rol_user is not None:
                raise ValidationError('El perfil no se puede eliminar porque está siendo usado por un usuario')

            session.delete(rol)
            session.commit()

            return {'data': 'Perfil Eliminado Correctamente'}
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)


class OptionSimple(object):
    """
    Binding class to option class
    """
    def __init__(self, option_id, name, code, parent, c, r, u, d, order, childs):
        self.option_id = option_id
        self.name = name
        self.code = code
        self.parent = parent
        self.c = c
        self.r = r
        self.u = u
        self.d = d
        self.order = order
        self.childs = childs

    def export_data(self):
        """
        Allow export to json the class
        :return: dict object
        """
        return {
            'optionId': self.option_id,
            'name': self.name,
            'code': self.code,
            'parent': self.parent,
            'c': bool(self.c),
            'r': bool(self.r),
            'u': bool(self.u),
            'd': bool(self.d),
            'order': self.order,
            'childs': [z.export_data() for z in self.childs],
        }




