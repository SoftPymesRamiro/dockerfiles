# -*- coding: utf-8 -*-
#########################################################
# All rights by SoftPymes Plus
#
# Auth Module
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from ... import Base, session
from ...utils.image_converter import ImagesConverter
from sqlalchemy import String, Integer, Column, DateTime, VARBINARY, or_, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy.dialects.mysql import TINYINT
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from ...exceptions import ValidationError, InternalServerError
from jose import jwt, JWSError, ExpiredSignatureError
import os
from ..referential.image import Image
from ..referential.branch import Branch
from .rol import Rol
from .user_branch_role import UserBranchRole
from .rol_option import RolOption
from .option import Option
from flask import g, abort
from ...utils import CryptoTools


class User(Base):
    """User as a public model class.

    note::

    """
    __tablename__ = 'users'

    userId = Column(Integer, primary_key=True, nullable=False)
    firstName = Column(String(200), default=None, nullable=False)
    lastName = Column(String(200), default=None, nullable=False)
    email = Column(String(512), default=None, nullable=True)
    passwordHash = Column(String(2000), default=None, nullable=True)
    userName = Column(String(512), default=None, nullable=False)
    lastBranchId = Column(Integer, ForeignKey("branches.branchId"), index=True, nullable=True)
    lastBranch = relationship("Branch")
    joinDate = Column(DateTime, default=None, nullable=False)
    # emailConfirmed = Column(TINYINT, default=None, nullable=False)
    state = Column(TINYINT, default=None, nullable=False)
    changePasswordOnNextLogin = Column(TINYINT, default=None, nullable=False)
    processDate = Column(DateTime, default=None, nullable=True)
    adminChat = Column(TINYINT, default=0, nullable=False)
    adminPos = Column(TINYINT, default=0, nullable=False)
    adminSales = Column(TINYINT, default=1, nullable=False)
    # photo = Column(VARBINARY, default=None, nullable=True)
    name = Column(String(200), default=None, nullable=True)
    theme = Column(String(6), default=None, nullable=True)
    oldPassword = Column(String(2000), default=None, nullable=True)
    imageId = Column(Integer, ForeignKey('images.imageId'))
    image = relationship('Image')
    automaticSMS = Column(TINYINT, default=None)
    creationDate = Column(DateTime, default=datetime.now(), nullable=False)
    createdBy = Column(String(50), nullable=False)
    updateDate = Column(DateTime, default=datetime.now(), nullable=False)
    updateBy = Column(String(50), nullable=False)
    isDeleted = Column(Integer, default=0)
    userBranchRole = relationship("UserBranchRole",
                                 primaryjoin=userId == UserBranchRole.userId, cascade='delete, all, delete-orphan')


    # @validates('firstName')
    # def validate_first_name(self, key, field):
    #     if not isinstance(field, str):
    #         raise AssertionError("Invalid user: field {0}".format(key))
    #     return field

    def full_name(self):
        """
        Allow create a fullname -- first and last name by a user
        :return: fullname user str
        """
        return "{0} {1}".format(self.firstName, self.lastName)

    def set_password(self, password):
        """
        Allow set a new password hash according to input text seed
        :param password: seed to generate password
        :return: hash password
        """
        self.passwordHash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Allow validate a according to input seed and hash store by user
        :param password: seed to generate validate password
        :return: boolean status
        """
        if self.passwordHash is None:
            return False
        return check_password_hash(self.passwordHash, password)

    def change_password(self, old_password, new_password):
        """
        Allow change password
        :param old_password: old hash password
        :param new_password: new hash password
        :raise: An error occurs when a old an new passwords no match
        :return: none wheter is changed, raise otherwise
        """
        if check_password_hash(self.passwordHash, old_password):
            self.set_password(new_password)
        else:
            raise ValidationError("Las contraseñas no coiniciden")

    @staticmethod
    def find_user(username, password):
        """
        Allow find an user from username and password
        :param username: username by user to search
        :param password:  password hash by user to search
        :return: user object or None otherwise
        """
        try:
            user = session.query(User).filter(User.userName.ilike('%'+username+'%')).first()
            if user is None:
                return None
            if user.verify_password(password):
                return user
            else:
                return None
        except Exception as e:
            print(e)
            session.rollback()
            raise InternalServerError(e)

    def generate_auth_token(self, user):
        """
        Allow generate a token by un new user
        :param user: full user data
        :return: string token
        """
        payload = {
            "sub": str(user.userId),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=1),
            "name": str(user.full_name()),
            "last_branch_id": str(user.lastBranchId)
        }
        token = jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
        return token

    @staticmethod
    def verify_auth_token(token):
        """
        Allow validate a user according a yours token
        :param token: token to validate
        :raise: ValidationError an error occurs when no auth token faile
        :return: token encode or 401 unauthorized
        """
        if token is None or token == "":
            return None
        try:
            jw = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
            g.user = jw
            return jw
        except JWSError as e:
            raise ValidationError(e)
        except ExpiredSignatureError as e:
            return None
        except Exception as e:
            return None

    def export_data(self):
        """
        Allow export user data
        :return:  user object in JSON format
        """
        return {
            "id": self.userId,
            "name": self.name,
            "userName": self.userName,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "passwordHash": self.passwordHash,
            "lastBranchId": self.lastBranchId,
            "joinDate": self.joinDate,
            # "emailConfirmed": self.emailConfirmed,
            "state": bool(self.state),
            "changePasswordOnNextLogin": self.changePasswordOnNextLogin,
            "processDate": self.processDate,
            "adminChat": bool(self.adminChat),
            "adminPOS": bool(self.adminPos),
            "adminSales": bool(self.adminSales),
            "automaticSMS": bool(self.automaticSMS),
            # "photo": None if self.image is None else ImagesConverter.img_convert_to_base64(self.image.image),
            "photoId": self.imageId,
            "theme": self.theme,
            "oldPassword": self.oldPassword,
            "userBranchRoleList": [ubr.export_data() for ubr in self.userBranchRole]
        }

    def export_data_light(self):
        """
        Allow export user data short description
        :return:  user object in JSON format
        """
        return {
            "id": self.userId,
            "name": self.name,
            "userName": self.userName,
            "fullName": "{0} {1}".format(self.firstName, self.lastName),
            "firstName": self.firstName,
            "lastName": self.lastName,
            # "photo": None if self.image is None else "{0},{1}".format("data:image/*;base64",
            #                                                           ImagesConverter.img_convert_to_base64(self.image.image)),
            "state": bool(self.state)
        }

    def import_data(self, data):
        """
        Allow create un ner user from user data directly
        :param data: information by new user
        :exception: ValidationError An error occurs
        :return: user object create in JOSN format
        """
        try:
            if "id" in data:
                self.userId = data["id"]
            self.name = data["name"]
            self.userName = data["userName"]
            self.firstName = data["firstName"]
            self.lastName = data["lastName"]
            self.email = data["email"]
            self.adminPos = data["adminPOS"]
            self.adminSales = data["adminSales"]
            self.adminChat = data["adminChat"]
            if "automaticSMS" in data:
                self.automaticSMS = data["automaticSMS"]
            else:
                self.automaticSMS = 0
            self.state = data["state"]
            if "changePasswordOnNextLogin" in data:
                self.changePasswordOnNextLogin = data["changePasswordOnNextLogin"]
            if "joinDate" in data:
                    self.joinDate = datetime.now() if data["joinDate"] is None \
                        else datetime.strptime(str(data["joinDate"]), '%a, %d %b %Y %H:%M:%S %Z')
            if "email" in data:
                self.email = data["email"]
            if "passwordHash" in data:
                self.passwordHash = data["passwordHash"]
            if "lastBranchId" in data:
                self.lastBranchId = data["lastBranchId"]
            if "processDate" in data:
                self.processDate = None if data["processDate"] is None \
                    else datetime.strptime(str(data["processDate"]), '%a, %d %b %Y %H:%M:%S %Z')
            # if "photo" in data:
            #     self.photo = data["photo"]
            if "theme" in data:
                self.theme = data["theme"]
            if "oldPassword" in data:
                self.oldPassword = data["oldPassword"]
            if "imageId" in data:
                self.imageId = data["imageId"]
        except KeyError as e:
            raise ValidationError("Invalid user: missing " + e.args[0])
        return self

    @staticmethod
    def get_user(id):
        """
        Allow obtain a user for to give identifier

        :param id: user indentifier
        :return: User object
        """
        return session.query(User).filter_by(userId=id).one_or_none()

    @staticmethod
    def get_users(**kwargs):
        """
            Metodo para listar los usuarios
            Ejemplos:
            /users/ : obtiene todo los usuarios
            /users?light=1 : obtiene todos los usuarios pero no con todos los campos
            /users?can_create_anonymous_user : devulve si el usuario puede crear usuarios anonimos
            /users?search=xyz : busca por username y firstname + lastname
            :return: an array with user objects in JSON format
        """

        light = kwargs.get("light")
        can_create_anonymous_users = kwargs.get("can_create_anonymous_users")
        search = kwargs.get("search")

        if light == "1":
            users = [user.export_data_light() for user in session.query(User).order_by(User.userName).all()]
        elif can_create_anonymous_users == "1":
            if session.query(User).one_or_none() is None and g.is_authenticate is None:
                return []
            else:
                # res = jsonify()
                # res.status_code = 401
                # return {"error":}
                return None
        elif search is not None:
            text_search = "" if search is None else search.strip()
            words = text_search.split(' ', 1) if text_search is not None else None
            users = [user.export_data_light()
                     for user in session.query(User)
                         .filter(or_(True if search == "" else None,
                                     or_(*[User.userName.like('%{0}%'.format(s)) for s in words]),
                                     or_(*[User.firstName.like('%{0}%'.format(s)) for s in words]),
                                     or_(*[User.lastName.like('%{0}%'.format(s)) for s in words])
                                     )
                                 )
                     ]
            # return jsonify(userList=users)
            return users
        else:
            users = [user.export_data() for user in session.query(User).all()]
        # return jsonify(user_list=users)
        return users

    @staticmethod
    def get_my_user():
        """
        Allow obtain user active
        :return: user object in JSON format
        """
        if g.is_authenticate is None:
            return {}, 400, {}

        user = session.query(User).get(g.is_authenticate["sub"])

        # si el usuario no tiene ultima sucursal toma una de la lista que tiene asociada
        user.lastBranchId = user.userBranchRole[0].branchId if len(user.userBranchRole) > 0 else None

        # consulta la compañia de la sucursal a la que esta en el momento
        branch = session.query(Branch).filter(Branch.branchId == user.lastBranchId).first()
        last_company = {
            "name": branch.company.name if branch is not None else None,
            "companyId": branch.companyId if branch is not None else None,
            "selfRetainingRete": branch.company.selfRetainingRete if branch is not None else None,
            "selfRetainingCREE": branch.company.selfRetainingCREE if branch is not None else None,
            "selfRetainingICA": branch.company.selfRetainingICA if branch is not None else None
        }

        companies = []

        # crea lista de compañias que el usuario puede acceder
        for ubr in user.userBranchRole:
            company = session.query(Branch).filter(Branch.branchId == ubr.branchId).first()

            if len([c for c in companies if c["companyId"] == company.companyId]) == 0 and company is not None:
                branches = []
                for br in user.userBranchRole:
                    if br.branch is not None and br.branch.companyId == company.companyId:
                        branches.append({
                            "branchId": br.branch.branchId,
                            "name": br.branch.name,
                            "rolId": br.rolId
                        })

                companies.append({
                    "branchList": branches,
                    "companyId": company.companyId,
                    "expenseLevel": company.company.expenseLevel,
                    "name": company.company.name
                })

        user.processDate = datetime.now()
        user.theme = "red" if user.theme is None else str(user.theme)

        result = {
            "name": user.name,
            "userName": user.userName,
            "userId": user.userId,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "state": user.state,
            "changePasswordOnNextLogin": user.changePasswordOnNextLogin,
            "adminPos": user.adminPos,
            "adminChat": user.adminChat,
            "adminSales": user.adminSales,
            "theme": user.theme,
            "lastBranchId": user.lastBranchId,
            "processDate": user.processDate,
            "branchList": companies,
            "lastCompanyId": 0 if last_company["companyId"] is None else last_company["companyId"],
            "lasCompany": last_company,
            "lastCompanyName": "" if last_company["name"] is None else last_company["name"],
        }

        return result, 200, {}

    @staticmethod
    def get_options(user_id, branch_id):
        try:
            options = session.query(RolOption)\
                .options(joinedload(RolOption.option, innerjoin=True))\
                .join(UserBranchRole, RolOption.rolId == UserBranchRole.rolId)\
                .filter(UserBranchRole.userId == user_id, UserBranchRole.branchId == branch_id)\
                .all()
            return options
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def new_user(data):
        """
        Allow creata an new user<br/> Metodo para creacion de usaurios
        :param data: information by new user
        :exception: An error occurs when server or database no allow user.
        :return:
        """
        try:
            user = User()
            username_restricted = ("MasterPymes", "PosVentaPymes", "USUARIOINICIAL")
            user_count = session.query(User).count()

            data["changePasswordOnNextLogin"] = 1

            # carga inicial de los campos que son requeridos
            user.import_data(data)

            session.add(user)
            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

            default_role = None

            if g.is_authenticate is None:
                if user_count > 0:
                    # Si tiene más de un usuario creado en la base de datos y manda un request sin token significa que
                    # ya han creado el usuario Inicial.
                    return {}, 401, {}

                default_role = session.query(Rol).filter(Rol.name.like("%ADMINISTRADOR%")).first()

                if default_role is None:
                    session.rollback()
                    return {"message": "No existen perfiles creados en la base de datos"}, 500, {}

            # Verifica que el usuario a crear no sea un usuario con Login Reservado
            if user.userName in username_restricted:
                session.rollback()
                return {"status": 400, "error": "bad request",
                        "message": "No puedes creear el usuario {0} debido a que es un "
                                   "nombre reservado".format(user.userName)}, 400, {}

            try:

                """ Si el request tiene token, Significa que se está realizado desde la vista de Creación de usuarios
                    de lo contrario, es un primer paso desde la empresa y se está creando el primer usuario administrador de la
                    empresa. Para este usuario se requiere asignarle un perfil por defecto.
                """

                if g.is_authenticate is not None:
                    logo_converter = None if "logoConvert" not in data else data["logoConvert"]
                    image = Image()
                    if logo_converter is not None and str(logo_converter).strip() != "":
                        image_detail = ImagesConverter.img_convert(data["logoConvert"])

                        image.image = image_detail
                        image.type = "Us"
                        image.idType = user.userId
                        session.add(image)
                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise InternalServerError()

                    user.joinDate = datetime.now()
                    user.createdBy = g.user['name']
                    user.creationDate = datetime.now()
                    user.updateBy = g.user['name']
                    user.updateDate = datetime.now()
                    # user.emailConfirmed = 1
                    user.changePasswordOnNextLogin = 1
                    # user.photo = None
                    user.imageId = image.imageId

                else:
                    user.joinDate = datetime.now()
                    # user.emailConfirmed = 1
                    user.state = 1
                    user.changePasswordOnNextLogin = 1
                    user.adminChat = 0
                    user.adminPos = 0
                    user.adminSales = 1
                    # user.photo = None
                    user.createdBy = 'USUARIO INICIAL'
                    user.creationDate = datetime.now()
                    user.updateBy = 'USUARIO INICIAL'
                    user.updateDate = datetime.now()

                user.set_password(data["password"])
                # user2 = User(userName="asd", firstName="asdas", lastName="asdasd")
                # color = Color(name="asda", code="asd")
                session.add(user)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

                if g.is_authenticate is None:
                    user_branch_role = UserBranchRole()
                    user_branch_role.userId = user.userId
                    user_branch_role.rolId = default_role.rolId
                    user_branch_role.branchId = None
                    user_branch_role.createdBy = user.userName
                    user_branch_role.creationDate = datetime.now()
                    user_branch_role.updateBy = user.userName
                    user_branch_role.updateDate = datetime.now()

                    session.add(user_branch_role)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise InternalServerError(e)

                user_branch_rol_list = None if "userBranchRoleList" not in data else data["userBranchRoleList"]

                if user_branch_rol_list is not None and len(user_branch_rol_list) > 0 and g.is_authenticate is not None:
                    for ubr in data["userBranchRoleList"]:
                        if "userBranchRolId" in ubr:
                            if ubr["userBranchRolId"] > 0:
                                continue

                        new_user_branch_role = UserBranchRole()

                        new_user_branch_role.userId = user.userId
                        new_user_branch_role.rolId = ubr["rolId"]
                        new_user_branch_role.branchId = ubr["branchId"]
                        new_user_branch_role.createdBy = user.userName
                        new_user_branch_role.creationDate = datetime.now()
                        new_user_branch_role.updateBy = user.userName
                        new_user_branch_role.updateDate = datetime.now()

                        session.add(new_user_branch_role)

                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise InternalServerError(e)
                session.commit()

            except Exception as e:
                session.rollback()
                print(e)
                raise InternalServerError(e)

            return user, 201, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_user(id, data, **kwargs):
        """
            Allow update a user live user
            :param id: identifier by user
            :param data: user information
            :param kwargs: request params
            :return: status code and results
        """
        try:

            # Para cambiar contraseña del usuario
            change_password = kwargs.get('change_password')
            if change_password is not None:
                user = session.query(User).filter_by(userId=id).one_or_none()
                old_password = data.json[u'OldPassword']
                new_password = data.json[u'NewPassword']
                user.change_password(old_password, new_password)
                user.changePasswordOnNextLogin = 0
                session.add(user)
                session.commit()
                return {}, 200, {}

            # Cambia la contraseña de el usuario migrado
            change_password_old_user = kwargs.get('change_password_old_user')
            if change_password_old_user is not None:
                if g.is_authenticate is not None:
                    return {}, 401, {}
                password = data.json[u'OldPassword']
                username = data.json[u'Username']
                new_password = data.json[u'NewPassword']
                old_password_encrypt = CryptoTools.encrypt_pymes_plus(str(password), str(username).upper().ljust(8, 'F'))
                user_in_db = session.query(User).filter(User.userName.ilike('%'+username+'%'),
                                                        User.oldPassword == old_password_encrypt).first()
                if user_in_db is None:
                    raise ValidationError("Usario de migración no encontrado")

                user_in_db.set_password(new_password)

                user_in_db.changePasswordOnNextLogin = 0
                user_in_db.oldPassword = None
                session.add(user_in_db)
                session.commit()

                return {}, 200, {}

            user_data = User()
            user_data.import_data(data.json)
            user_data.userId = data.json[u'id']
            if id != user_data.userId:
                return {}, 400, {}

            user = session.query(User).filter_by(userId=id).first()

            if 'userBranchRoleList' in data.json and data.json['userBranchRoleList'] is not None \
                    and len(data.json['userBranchRoleList']) > 0:
                ubr_list = data.json['userBranchRoleList']
                for ubr in ubr_list:
                    ubr_binding = UserBranchRole()
                    ubr_binding.import_data(ubr)
                    if 'userBranchRolId' not in ubr or ubr['userBranchRolId'] <= 0:
                        user_branch_role = UserBranchRole()
                        user_branch_role.userId = user_data.userId
                        user_branch_role.rolId = ubr_binding.rolId
                        user_branch_role.branchId = ubr_binding.branchId
                        user_branch_role.createdBy = 'USUARIO INICIAL'
                        user_branch_role.creationDate = datetime.now()
                        user_branch_role.updateBy = 'USUARIO INCIAL'
                        user_branch_role.updateDate = datetime.now()
                        session.add(user_branch_role)
                    else:
                        update_branch_role = session.query(UserBranchRole).get(ubr['userBranchRolId'])
                        if update_branch_role is not None:
                            update_branch_role.rolId = ubr_binding.rolId
                            update_branch_role.branchId = ubr_binding.branchId
                            update_branch_role.updateBy = g.user['name']
                            update_branch_role.updateDate = datetime.now()
                        session.add(update_branch_role)

            password = None if 'password' not in data.json else data.json['password']

            logo_converter = None if "logoConvert" not in data.json else data.json["logoConvert"]
            image = Image()
            if logo_converter is not None and str(logo_converter).strip() != "":
                if user_data.imageId is not None:
                    image = session.query(Image).get(user_data.imageId)
                    image_detail = ImagesConverter.img_convert(data.json["logoConvert"])
                    if image_detail is not None:
                        image.image = image_detail
                        # image.type = "Us"
                        # image.idType = user.userId
                        session.add(image)
                else:
                    image_detail = ImagesConverter.img_convert(data.json["logoConvert"])
                    if image_detail is not None:
                        image.image = image_detail
                        image.type = "Us"
                        image.idType = user.userId
                        session.add(image)
                try:
                    session.flush()
                except Exception as e:
                    session.rollback()
                    raise InternalServerError(e)

            if image.imageId is not None:
                user.imageId = image.imageId

            user.userName = user_data.userName
            user.firstName = user_data.firstName
            user.lastName = user_data.lastName
            user.email = user_data.email
            user.state = user_data.state
            user.adminPos = user_data.adminPos
            user.adminChat = user_data.adminChat
            user.adminSales = user_data.adminSales

            if password is not None:
                user.set_password(password)
                user.changePasswordOnNextLogin = 1

            session.add(user)

            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise InternalServerError(e)

            return {}, 200, {}
        except KeyError as e:
            return {"error": str(e)}, 500, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_user_theme(id, data):
        """
        Allow update user's theme
        :param id: id user
        :param data: data json with name's theme
        :return: data json
        """
        try:
            # para actualizar solo el tema
            user = session.query(User).filter_by(userId=id).one_or_none()
            user.theme = data.json[u'theme']
            session.add(user)
            session.commit()
            return {}, 200, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_user_branch(id, branch_id):
        """
        Allow update last branch's user
        :param id: user id
        :param branch_id: branch id
        :return: data json
        """
        try:
            user = session.query(User).filter_by(userId=id).one_or_none()
            user.lastBranchId = branch_id
            session.add(user)
            session.commit()
            return {}, 200, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def update_user_process_date(id, process_date):
        """
        Allow update process date's user
        :param id: user id
        :param process_date: date
        :return: data json
        """
        try:
            user = session.query(User).filter_by(userId=id).one_or_none()
            user.processDate = process_date
            session.add(user)
            session.commit()
            return {}, 200, {}
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def delete_user(id):
        """
        Allow delet a user according to identifier
        :param id: identifier by user to delete
        :return: status code and result
        """
        try:
            user = session.query(User).get(id)
            if user is not None:
                session.delete(user)
                session.commit()
                return {}, 200, {}
            else:
                return {}, 404, {}
        except Exception as e:
            return {"error": str(e)}, 500, {}

    @staticmethod
    def validate_user_migrated():
        pass

