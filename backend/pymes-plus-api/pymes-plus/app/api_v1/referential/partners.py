# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
#
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"

from flask import request, jsonify, Response
import json
from .. import api
from ...models import Partner


@api.route('/partners/search', methods=['GET'])
def partners_search():

    """
        @api {get}  /partners/search Search Partners
        @apiName Search
        @apiGroup Referential.Partners
        @apiDescription Return all partners in a list
        @apiParam {String} search
        @apiParam {Number} simple Customer info (in success)
        @apiParam {Number} third_party_id third party identifier
        @apiParam {Number} company_id company identifier
        @apiParam {Number} page_size Quantity of customers return per page
        @apiParam {Number} page_number Pagination number
        @apiSuccessExample {json} Success
          HTTP/1.1 200 OK
            {
              "data": [{},...
                    {
                      "accountant": "MARITZA RIASCOS ALOMIA",
                      "accountantNumber": "147172T",
                      "auditor": "",
                      "auditorNumber": "",
                      "branchList": [
                        {
                          "address1": "CR 37 10 303 BODEGA 1401",
                          "address2": "",
                          "branchId": 1,
                          "city": {
                            "cityId": 864,
                            "departmentId": 24,
                            "indicative": "2",
                            "name": "YUMBO"
                          },
                          "cityId": 864,
                          "code": "001",
                          "company": {
                            "code": "001",
                            "companyId": 1,
                            "identificationDV": "6",
                            "identificationNumber": "900630008",
                            "name": "PRODUCTOS PHYSIS SAS"
                          },
                          "companyId": 1,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Fri, 17 Jun 2016 09:31:26 GMT",
                          "economicActivity": {
                            "code": "2100",
                            "economicActivityId": 118,
                            "name": "FABRICACION DE PRODUCTOS FARMACEUTICOS, SUSTANCIAS QUIMICAS MEDICINALES Y PRODUCTOS BOTANICOS DE USO FARMACEUTICO 0.30"
                          },
                          "economicActivityId": 118,
                          "email": "x7bodyperfect@gmail.com",
                          "fax": "",
                          "icaActivity1": "102-40",
                          "icaActivity2": "",
                          "icaActivity3": "",
                          "icaActivity4": "",
                          "icaActivity5": "",
                          "icaRate1": 6.60,
                          "icaRate2": 0.00,
                          "icaRate3": 0.00,
                          "icaRate4": 0.00,
                          "icaRate5": 0.00,
                          "isDeleted": 0,
                          "motionDate": "Thu, 06 Jul 2017 08:35:13 GMT",
                          "name": "ACOPI YUMBO",
                          "phone1": "6959426",
                          "phone2": "3207781009",
                          "phone3": "",
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Fri, 04 Nov 2016 17:05:22 GMT",
                          "withholdingCREEPUC": {
                            "account": "55",
                            "auxiliary1": "020",
                            "name": "SERVICIOS 1011 - 3320 0.30%",
                            "pucClass": "1",
                            "pucId": 6503,
                            "pucSubClass": "3",
                            "subAccount": "19"
                          },
                          "withholdingCREEPUCId": 6503,
                          "zipCode": ""
                        }
                      ],
                      "code": "001",
                      "companyId": 1,
                      "createdBy": "Administrador del Sistema",
                      "creationDate": "Fri, 04 Nov 2016 17:05:22 GMT",
                      "expenseLevel": "S",
                      "identificationDV": "6",
                      "identificationId": 3,
                      "identificationNumber": "900630008",
                      "identificationType": {
                        "code": "N",
                        "identificationTypeDian": "31",
                        "identificationTypeId": 3,
                        "name": "Nit"
                      },
                      "imageId": 45,
                      "isDeleted": 0,
                      "ivaType": {
                        "code": "C",
                        "ivaTypeId": 1,
                        "name": "COMUN"
                      },
                      "ivaTypeId": 1,
                      "legalAgent": "",
                      "logoConvert": "",
                      "manager": "JULIO CESAR CASA\u00d1AS MAYA",
                      "name": "PRODUCTOS PHYSIS SAS",
                      "partnerList": [
                        {
                          "address1": "CR 24 C OESTE 6 85 APTO 305",
                          "address2": "",
                          "city": {
                            "cityId": 824,
                            "departmentId": 24,
                            "indicative": "2",
                            "name": "CALI"
                          },
                          "companyId": 1,
                          "createdBy": "Administrador del Sistema",
                          "creationDate": "Fri, 04 Nov 2016 17:05:22 GMT",
                          "fax": "",
                          "isDeleted": 0,
                          "legalAgent": 0,
                          "name": " NARVAEZ RUA LUISA FERNANDA (1125998983)",
                          "participation": 100.0000,
                          "partnerId": 2,
                          "phone": "3136379209",
                          "stock": 5000,
                          "thirdParty": {
                            "alternateIdentification": "",
                            "comments": "",
                            "createdBy": "Administrador del Sistema",
                            "creationDate": "Fri, 17 Jun 2016 09:17:29 GMT",
                            "economicActivity": {
                              "code": "6810",
                              "createdBy": "CREE",
                              "creationDate": "Tue, 28 May 2013 14:39:28 GMT",
                              "economicActivityId": 379,
                              "name": "Actividades inmobiliarias realizadas con bienes propios o arrendados",
                              "percentage": 0.60,
                              "updateBy": "CREE",
                              "updateDate": "Tue, 28 May 2013 14:39:28 GMT"
                            },
                            "economicActivityId": 379,
                            "entryDate": "Fri, 17 Jun 2016 09:15:37 GMT",
                            "firstName": "LUISA FERNANDA",
                            "identificationDV": "2",
                            "identificationNumber": "1125998983",
                            "identificationType": {
                              "code": "C",
                              "createdBy": "Migracion",
                              "creationDate": "Fri, 17 Aug 2012 10:34:52 GMT",
                              "identificationTypeDian": "13",
                              "identificationTypeId": 1,
                              "isDeleted": 0,
                              "name": "Cedula de Ciudadania",
                              "updateBy": "Migracion"
                            },
                            "identificationTypeId": 1,
                            "imageId": null,
                            "isDeleted": false,
                            "isGreatTaxPayer": false,
                            "isSelfRetainer": false,
                            "isSelfRetainerICA": false,
                            "isWithholdingCREE": false,
                            "ivaTypeId": 4,
                            "lastName": "NARVAEZ",
                            "maidenName": "RUA",
                            "retirementDate": null,
                            "rut": false,
                            "secondName": "",
                            "state": "A",
                            "thirdPartyId": 59,
                            "thirdType": "N",
                            "tradeName": "",
                            "updateBy": "MARITZA RIASCOS ",
                            "updateDate": "Tue, 04 Apr 2017 16:50:57 GMT",
                            "webPage": ""
                          },
                          "thirdPartyId": 59,
                          "updateBy": "Administrador del Sistema",
                          "updateDate": "Thu, 06 Jul 2017 08:35:13 GMT",
                          "zipCode": ""
                        }
                      ],
                      "puc": {
                        "account": "20",
                        "name": "ELABORACION DE PRODUCTOS ALIMENTICIOS",
                        "pucClass": "4",
                        "pucSubClass": "1",
                        "subAccount": "14"
                      },
                      "pucId": 2328,
                      "reloadCash": 0,
                      "selfRetaining": 1,
                      "selfRetainingCREE": false,
                      "selfRetainingDate": "Fri, 02 Jun 2017 05:00:00 GMT",
                      "selfRetainingICA": true,
                      "selfRetainingRete": true,
                      "selfRetainingText": "123",
                      "serial": 0,
                      "society": {
                        "code": "F",
                        "name": "ANONIMA SIMPLIFICADA",
                        "puc": {
                          "name": "CAPITAL AUTORIZADO",
                          "percentage": 0.000,
                          "pucAccount": "310505005",
                          "pucId": 1987
                        },
                        "societyId": 2
                      },
                      "societyId": 2,
                      "taxpayer": "P",
                      "taxpayerDate": null,
                      "taxpayerText": "",
                      "updateBy": "Administrador del Sistema",
                      "updateDate": "Thu, 06 Jul 2017 08:35:12 GMT",
                      "webPage": "x7bodyperfect@gmail.com"
                    }
                ,...{}]
            }
        @apiErrorExample {json} DocumentNotFoundError The search empty result
        HTTP/1.1 200 OK
            {
                "data": []
            }
        @apiErrorExample {json} Find error
            HTTP/1.1 500 Internal Server Error
        """
    ra = request.args.get
    company_id = ra("company_id")
    simple = ra("simple")
    search = None if ra('search') == u'null' else ra('search')
    search = "" if search is None else search.strip()
    words = search.split(' ', 1) if search is not None else None
    page_size = ra("page_size")
    page_number = ra("page_number")
    third_party_id = ra("third_party_id")
    kwargs = dict(simple=simple, company_id=company_id, search=search, words=words,
                  page_size=page_size, page_number=page_number, third_party_id=third_party_id)
    response = Partner.get_bySearch(**kwargs)
    return response
