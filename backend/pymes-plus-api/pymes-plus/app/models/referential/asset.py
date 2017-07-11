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
from ... import Base, session
from sqlalchemy import Column, Integer, ForeignKey, DateTime, DECIMAL, String, SmallInteger
from sqlalchemy.orm import relationship
from .image import Image
from ...utils.image_converter import ImagesConverter
from flask import jsonify, g
from sqlalchemy import or_, and_
from ...exceptions import ValidationError, IntegrityError, InternalServerError
from ...utils import converters
from sqlalchemy.exc import IntegrityError as sqlIntegrityError


class Asset(Base):
    """
        Datatable class
    """
    __tablename__ = 'assets'

    assetId = Column(Integer, primary_key=True)
    sectionId = Column(ForeignKey(u'sections.sectionId'), index=True)
    costCenterId = Column(ForeignKey(u'costcenters.costCenterId'), index=True)
    branchId = Column(ForeignKey(u'branches.branchId'), index=True)
    pucId = Column(ForeignKey(u'puc.pucId'), index=True)
    divisionId = Column(ForeignKey(u'divisions.divisionId'), index=True)
    assetGroupId = Column(ForeignKey(u'assetgroups.assetGroupId'), index=True)
    dependencyId = Column(ForeignKey(u'dependencies.dependencyId'), index=True)
    cityId = Column(ForeignKey(u'cities.cityId'), index=True)
    purchaseDate = Column(DateTime)
    dateNotarialDocument = Column(DateTime)
    creationDate = Column(DateTime)
    updateDate = Column(DateTime)
    rentable = Column(Integer)
    isDeleted = Column(Integer)
    percentageSaving = Column(DECIMAL(5, 2), default=0.0)
    landArea = Column(DECIMAL(12, 2), default=0.0)
    builtArea = Column(DECIMAL(12, 2), default=0.0)
    costHour = Column(DECIMAL(14, 2), default=0.0)
    netValueNIIF = Column(DECIMAL(18, 4), default=0.0)
    percentageResidual = Column(DECIMAL(5, 2), default=0.0)
    # Photo = Column(VARBINARY(2000))
    code = Column(String(50))
    typeAsset = Column(String(1))
    name = Column(String(100))
    address = Column(String(50))
    notarialDocument = Column(String(20))
    notary = Column(String(3))
    comments = Column(String(2000))
    createdBy = Column(String(50))
    updateBy = Column(String(50))
    # responsible = Column(String(2000))
    propertyNumber = Column(String(30))
    engineSerial = Column(String(20))
    chassisSerial = Column(String(20))
    line = Column(String(50))
    plate = Column(String(8))
    state = Column(String(1))
    depreciationYear = Column(SmallInteger)
    depreciationMonth = Column(SmallInteger)
    model = Column(SmallInteger)
    depreciationYearNIIF = Column(SmallInteger)
    depreciationMonthNIIF = Column(SmallInteger)
    imageId = Column(ForeignKey(u'images.imageId'), index=True)

    assetGroup = relationship(u'AssetGroup')
    branch = relationship(u'Branch')
    city = relationship(u'City')
    costCenter = relationship(u'CostCenter')
    dependency = relationship(u'Dependency')
    division = relationship(u'Division')
    puc = relationship(u'PUC')
    section = relationship(u'Section')

    image = relationship("Image",
                         primaryjoin=imageId == Image.imageId,
                         cascade="all, delete, delete-orphan", single_parent=True)

    def export_data(self):
        """
        :return all asset data
        """
        img = session.query(Image).filter(Image.imageId == self.imageId).first()
        if img is tuple or img is list:
            img = None if img is None else img[0].image
        elif img is None:
            pass
        else:
            img = img.image

        return {
            'assetId': self.assetId,
            'sectionId': self.sectionId,
            'costCenterId': self.costCenterId,
            'branchId': self.branchId,
            'pucId': self.pucId,
            "puc": None if self.pucId is None or self.puc is None else{
                "pucId": self.puc.pucId,
                "account": '{0}{1}{2}{3}{4}'.format(self.puc.pucClass,
                                                    self.puc.pucSubClass,
                                                    self.puc.account,
                                                    self.puc.subAccount,
                                                    self.puc.auxiliary1),
                "name": self.puc.name,
            },
            'divisionId': self.divisionId,
            'assetGroupId': self.assetGroupId,
            'dependencyId': self.dependencyId,
            'cityId': self.cityId,
            'city': None if self.cityId is None or self.city is None else{
                'cityId': self.city.cityId,
                'code': self.city.code,
                'name': '{0}{1}{2}'.format(
                    self.city.name,
                    '' if self.city.department is None
                    else ' - {0}'.format(self.city.department.name),
                    '' if self.city.department is None and self.city.department.country is None
                    else ' - {0}'.format(self.city.department.country.name)),
                'indicative': self.city.indicative,
                'department': None if self.city.department is None else {
                    'departmentId': self.city.department.departmentId,
                    'code': self.city.department.code,
                    'name': self.city.department.name,
                    'country': None if self.city.department.country is None else {
                        'countryId': self.city.department.country.countryId,
                        'indicative': self.city.department.country.indicative,
                    }
                }

            },
            'purchaseDate': self.purchaseDate,
            'dateNotarialDocument': self.dateNotarialDocument,
            'creationDate': self.creationDate,
            'updateDate': self.updateDate,
            'rentable': bool(self.rentable),
            'isDeleted': self.isDeleted,
            'percentageSaving': self.percentageSaving,
            'landArea': self.landArea,
            'builtArea': self.builtArea,
            'costHour': self.costHour,
            'netValueNIIF': self.netValueNIIF,
            'percentageResidual': self.percentageResidual,
            'code': self.code,
            'typeAsset': self.typeAsset,
            'name': self.name,
            'address': self.address,
            'notarialDocument': self.notarialDocument,
            'notary': self.notary,
            'comments': self.comments,
            'createdBy': self.createdBy,
            'updateBy': self.updateBy,
            # 'responsible': self.responsible,
            'propertyNumber': self.propertyNumber,
            'engineSerial': self.engineSerial,
            'chassisSerial': self.chassisSerial,
            'logoConvert': ImagesConverter.img_convert_to_base64(img),
            'line': self.line,
            'plate': self.plate,
            'state': self.state,
            'depreciationYear': self.depreciationYear,
            'depreciationMonth': self.depreciationMonth,
            'model': self.model,
            'depreciationYearNIIF': self.depreciationYearNIIF,
            'depreciationMonthNIIF': self.depreciationMonthNIIF,
            'imageId': self.imageId,
        }


    def import_data(self, data):
        """
            Import business agents data from

            :param data
            :exception: ValidationError
            :return status import
        """
        if 'assetId' in data:
            self.assetId = data['assetId']
        if 'sectionId' in data:
            self.sectionId = data['sectionId']
        if 'costCenterId' in data:
            self.costCenterId = data['costCenterId']
        if 'branchId' in data:
            self.branchId = data['branchId']
        if 'pucId' in data:
            self.pucId = data['pucId']
        if 'divisionId' in data:
            self.divisionId = data['divisionId']
        if 'assetGroupId' in data:
            self.assetGroupId = data['assetGroupId']
        if 'dependencyId' in data:
            self.dependencyId = data['dependencyId']
        if 'cityId' in data:
            self.cityId = data['cityId']
        if 'purchaseDate' in data:
            self.purchaseDate = converters.convert_string_to_date(data['purchaseDate'])
        if 'dateNotarialDocument' in data:
            self.dateNotarialDocument = converters.convert_string_to_date(data['dateNotarialDocument'])
        if 'creationDate' in data:
            self.creationDate = data['creationDate']
        if 'updateDate' in data:
            self.updateDate = data['updateDate']
        if 'rentable' in data:
            self.rentable = data['rentable']
        if 'isDeleted' in data:
            self.isDeleted = data['isDeleted']
        if 'percentageSaving' in data:
            self.percentageSaving = data['percentageSaving']
        if 'landArea' in data:
            self.landArea = data['landArea']
        if 'builtArea' in data:
            self.builtArea = data['builtArea']
        if 'costHour' in data:
            self.costHour = data['costHour']
        if 'netValueNIIF' in data:
            self.netValueNIIF = data['netValueNIIF']
        if 'percentageResidual' in data:
            self.percentageResidual = data['percentageResidual']
        if 'code' in data:
            self.code = data['code']
        if 'typeAsset' in data:
            self.typeAsset = data['typeAsset']
        if 'name' in data:
            self.name = data['name']
        if 'address' in data:
            self.address = data['address']
        if 'notarialDocument' in data:
            self.notarialDocument = data['notarialDocument']
        if 'notary' in data:
            self.notary = data['notary']
        if 'comments' in data:
            self.comments = data['comments']
        if 'createdBy' in data:
            self.createdBy = data['createdBy']
        if 'updateBy' in data:
            self.updateBy = data['updateBy']
        # if 'responsible' in data:
        #     self.responsible = data['responsible']
        if 'propertyNumber' in data:
            self.propertyNumber = data['propertyNumber']
        if 'engineSerial' in data:
            self.engineSerial = data['engineSerial']
        if 'chassisSerial' in data:
            self.chassisSerial = data['chassisSerial']
        if 'line' in data:
            self.line = data['line']
        if 'plate' in data:
            self.plate = data['plate']
        if 'state' in data:
            self.state = data['state']
        if 'depreciationYear' in data:
            self.depreciationYear = data['depreciationYear']
        if 'depreciationMonth' in data:
            self.depreciationMonth = data['depreciationMonth']
        if 'model' in data:
            self.model = data['model']
        if 'depreciationYearNIIF' in data:
            self.depreciationYearNIIF = data['depreciationYearNIIF']
        if 'depreciationMonthNIIF' in data:
            self.depreciationMonthNIIF = data['depreciationMonthNIIF']
        if 'imageId' in data:
            self.imageId = data['imageId']

        # if 'imageAsset' in data:
        #     self.imageAsset = data['imageAsset']

        return self


    def export_simple(self):
        return {
            'assetId': self.assetId,
            'code': self.code,
            'typeAsset': self.typeAsset,
            'name': self.name,
            'branchId': self.branchId,
        }

    def save(self):
        """
        Allow save a document detail in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.createdBy = g.user['name']
            self.creationDate = datetime.now()
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    def update(self):
        """
        Allow save a document detail in database
        :exception: An error occurs when save not performance
        :return: None
        """
        try:
            self.updateBy = g.user['name']
            self.updateDate = datetime.now()

            session.add(self)
            session.flush()
        except Exception as e:
            session.rollback()
            print(e)
            raise InternalServerError(e)

    @staticmethod
    def get_asset(asset_id):
        """
            Allow obtain a asset according to asset_id
            :param asset_id identifier by asset
            :return asset in JSON object
        """
        asset_found = session.query(Asset).get(asset_id)
        if asset_found is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response

        asset_found = asset_found.export_data()
        response = jsonify(asset_found)
        return response


    @staticmethod
    def search_assets(**kwargs):
        """

        :return:
        """
        simple = kwargs.get("simple")
        branch_id = kwargs.get("branch_id")
        by_param = kwargs.get("by_param")
        code = kwargs.get("code")
        search = kwargs.get('search')
        words = kwargs.get('words')
        response = None

        if by_param:
            f = None
            if by_param == 'getAssetKitCode':
                wrd = list(words[0])
                direct = False
                if len(wrd) >= 3:
                    if wrd[-1] == '*' and wrd[-2] == '*':
                        direct = True

                f = (Asset.branchId == branch_id,
                     Asset.typeAsset == "M",
                     or_(*[Asset.code.contains(word) for word in words]))
                if len(words) == 1 and direct:
                    f = (Asset.branchId == branch_id,
                         Asset.typeAsset == "M",
                         Asset.code == words[0][:-2])

                list_asset = [asset.export_simple()
                                  for asset in session.query(Asset)
                                      .filter(*f)]

                response = jsonify(data=list_asset)
                return response

            if by_param == 'getAssetKitName':
                wrd = list(words[0])
                direct = False
                if len(wrd) >= 3:
                    if wrd[-1] == '*' and wrd[-2] == '*':
                        direct = True

                f = (Asset.branchId == branch_id,
                     Asset.typeAsset == "M",
                     or_(*[Asset.name.contains(word) for word in words]))
                if len(words) == 1 and direct:
                    f = (Asset.branchId == branch_id,
                         Asset.typeAsset == "M",
                         Asset.name == words[0][:-2])

                list_asset = [asset.export_simple()
                                  for asset in session.query(Asset)
                                      .filter(*f)]

                response = jsonify(data=list_asset)
                return response

        if branch_id and not simple:
            assets = [assets.export_data()
                            for assets in session.query(Asset).filter(
                    and_(Asset.branchId == branch_id,
                    or_(or_(*[Asset.name.contains(word) for word in words]),
                        or_(*[Asset.code.contains(word) for word in words])))
                ).order_by(Asset.code)]

            response = jsonify(data=assets)
            return response

        if simple and branch_id and not code:
            asset = session.query(Asset). \
                filter(Asset.branchId == branch_id).first()

            if asset is None:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404
                return response

            asset = asset.export_data()

            return jsonify(asset)

        elif simple and branch_id and code:
            asset = session.query(Asset). \
                filter(and_(
                    Asset.branchId == branch_id,
                    Asset.code == code
            )).first()

            if asset is None:
                response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
                response.status_code = 404
                return response

            asset = asset.export_data()

            return jsonify(asset)

        if response is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response


    @staticmethod
    def post_asset(data):
        """

        :param data:
        :return:
        """
        if asset_code_exist(data['code'], data['branchId']) > 0:
            response = jsonify({'error': 'Not Found', 'message': 'Asset code ready'})
            response.status_code = 404
            return response

        asset = Asset()
        try:
            data['creationDate'] = datetime.now()  # actualizo la clave fecha de creacion
            data['updateDate'] = datetime.now()  # actualizo la clave fecha de actualizacion
            data["createdBy"] = g.user['name']
            data["updateBy"] = g.user['name']

            asset.import_data(data)
            session.add(asset)
            try:
                session.flush()
            except Exception as e:
                session.rollback()
                raise InternalServerError(e)

            logos_converter = None if "imageAsset" not in data else data["imageAsset"]
            if not logos_converter is None:
                logo_convert = None if 'logoConvert' not in logos_converter else logos_converter['logoConvert']
                if logo_convert and not logo_convert == "":
                    detail_i = ImagesConverter.img_convert(logo_convert)
                    image = Image()
                    image.image = detail_i
                    image.type = "Em"
                    image.idType = asset.assetId
                    session.add(image)

                    try:
                        session.flush()
                    except Exception as e:
                        session.rollback()
                        raise InternalServerError(e)

                    asset.imageId = image.imageId


            session.commit()
            response = jsonify({'assetId': asset.assetId})

        except KeyError as e:
            raise ValidationError('Invalid asset: missing' + e.args[0])

        return response


    @staticmethod
    def put_asset(asset_id, data):
        """

        :param asset_id:
        :param data:
        :return:
        """

        update_asset = session.query(Asset).get(asset_id)

        try:

            data['creationDate'] = update_asset.creationDate
            data['createdBy'] = update_asset.createdBy
            data['updateDate'] = datetime.now()
            data["updateBy"] = g.user['name']

            update_asset = update_asset.import_data(data)
            session.add(update_asset)

            logos_converter = None if "imageAsset" not in data else data["imageAsset"]
            if not logos_converter is None:
                logo_convert = None if 'logoConvert' not in logos_converter else logos_converter['logoConvert']
                if logo_convert and not logo_convert == "":
                        detail_i = ImagesConverter.img_convert(logo_convert)
                        image = Image()
                        image.image = detail_i
                        image.type = "As"
                        image.idType = update_asset.assetId
                        session.add(image)

                        try:
                            session.flush()
                        except Exception as e:
                            session.rollback()
                            raise InternalServerError(e)

                        update_asset.imageId = image.imageId

            session.commit()
            response = jsonify({'ok': 'ok'})

        except Exception as e:
            session.rollback()
            raise InternalServerError(e)
        return response


    @staticmethod
    def delete_asset(asset_id):
        """

        :param asset_id:
        :return:
        """
        asset = session.query(Asset).get(asset_id)
        if asset is None:
            response = jsonify({'error': 'Not Found', 'message': 'Not Found'})
            response.status_code = 404
            return response
        session.delete(asset)
        try:
            session.commit()
            response = jsonify({'message': 'Eliminado correctamente'})
            response.status_code = 200
            return response
        except sqlIntegrityError as e:
            session.rollback()
            raise IntegrityError(e)
        except Exception as e:
            response = jsonify({'error': str(e)})
            response.status_code = 500
            return response


def asset_code_exist(import_code, branch_id):
    return session.query(Asset)\
        .filter(and_(Asset.code == import_code,
                     Asset.branchId == branch_id)).count()