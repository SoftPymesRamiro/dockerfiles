#!/usr/bin/env python
# -*- coding: utf-8 -*
#########################################################
# TEST Referential
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from flask import Flask
import unittest
import json
from copy import *
import time
import logging


from app import create_app
from app.api_v1 import api

"""
This module shows various methods and function by allow
handled Customer
"""
class CustomerTest(unittest.TestCase):
    """
    This Class is a Test Case for Customer API class
    """
    def setUp(self):
        """
        Allow construct a environment by all cases and functions
        """
        self.userdata = dict(username='administrador',
            password='Admin*2') # valid data by access to SoftPymes plus

        app = Flask(__name__) # aplication Flask
        self.app = create_app(app)  # pymes-plus-api
        self.test_client = self.app.test_client(self) # test client
        self.test_client.testing = False # allow create the environmet by test

        # Obtain token by user data and access in all enviroment test cases
        self.response = self.test_client.post('/oauth/token',
                    data=json.dumps(self.userdata),
                        content_type='application/json')
        # User token
        self.token = json.loads( self.response.data.decode("utf-8") )['token']
        # request header by access to several test in api
        self.headers = {"Authorization": "bearer {token}".format(token=self.token)}

    ################################ REQUEST FUNCTIONS ##################################
    def request_get(self,data,path="/"):
        """Sent get request to #/api/v1/customers# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.get('/api/v1/customers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_post(self,data,path="/"):
        """Sent post request to #/api/v1/customers# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.post('/api/v1/customers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_put(self,data,path="/"):
        """Sent put request to #/api/v1/customers# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.put('/api/v1/customers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    def request_delete(self,data,path="/"):
        """Sent delete request to #/api/v1/customers# with customer data values

        :param data: user data, username and password
        :type data: json object, default none
        :param path: specific path
        :type path: str
        :return: request response in dict format
        """
        return self.test_client.delete('/api/v1/customers'+path,
                data=json.dumps(data),
                content_type='application/json',headers=self.headers)  # envio el request

    ######################################################################################

    def test_search_customers(self):
        """
        This function test get all customers
        ** First validate that contains the data key and content
        """
        response = self.request_get("","/search?simple=1&search='CLL 42'")
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertTrue("totalPages" in response.json)
        self.assertTrue("listThirdParty" in response.json)
        self.assertTrue("totalCount" in response.json)

        self.assertEqual(0,response.json["totalPages"])
        self.assertEqual([], response.json["listThirdParty"])
        self.assertEqual(0,response.json["totalCount"])

        response = self.request_get("","/search?simple=1&search=YEFFE")
        response.json = json.loads( response.data.decode("utf-8") )
        # print(response.json)

        response = self.request_get("","/search?thirdPartyId=1&company_id=14")
        response.json = json.loads( response.data.decode("utf-8") )
        # print(response.json)


    def test_post_put_delete_business_agent(self):
        """
        This function test get a brand according to identifier
         ** First test is correct identifier
         ** Second test is incorrect identifier and validate data
        """
        data = {
          "billAddress1": "CLN1WQEWQE12132",
          "billAddress2": None,
          "billCity": {
            "department": {
              "code": "23",
              "country": {
                "countryId": 2,
                "indicative": "57"
              },
              "name": "CÓRDOBA",
              "departmentId": 10
            },
            "code": "678",
            "cityId": 61,
            "indicative": "4",
            "name": "SAN CARLOS - CÓRDOBA - COLOMBIA"
          },
          "billCityId": 61,
          "billCitySimple": {
            "department": {
              "code": "23",
              "country": {
                "countryId": 2,
                "indicative": "57"
              },
              "name": "CÓRDOBA",
              "departmentId": 10
            },
            "code": "678",
            "cityId": 61,
            "indicative": "4",
            "name": "SAN CARLOS - CÓRDOBA - COLOMBIA"
          },
          "billZipCode": None,
          "branch": "11",
          "branchId": 14,
          "businessAgentId": 6,
          "cellPhone": None,
          "changeIsMain": [],
          "companyId": 1,
          "contactList": [
            {
              "extension3": None,
              "name": "AAAAA",
              "extension1": "22",
              "businessAgentId": None,
              "extension2": None,
              "isDeleted": None,
              "phone3": None,
              "payrollEntityId": None,
              "updateDate": "Wed, 10 Aug 2016 08:32:07 GMT",
              "otherThirdId": None,
              "email1": "",
              "updateBy": "JAPeTo",
              "providerId": None,
              "createdBy": "JAPeTo",
              "email2": None,
              "lastName": "AAAAA",
              "isMain": None,
              "roleEmployee": None,
              "employeeId": None,
              "phone1": "2313213213",
              "financialEntityId": None,
              "fax": None,
              "phone2": "23123123213123213213",
              "creationDate": "Fri, 05 Aug 2016 17:19:49 GMT"
            }
          ],
          "creditCapacity": 12000,
          "employeeId": "",
          "fax": None,
          "isDeleted": None,
          "isMain": False,
          "name": "CLN1",
          "paymentTerm": {
            "code": "02",
            "name": "Credito"
          },
          "paymentTermId": 2,
          "phone": "231424234234",
          "priceList": None,
          "shipAddress1": None,
          "shipAddress2": None,
          "shipCity": None,
          "shipCityId": None,
          "shipCitySimple": None,
          "shipTo": None,
          "shipZipCode": None,
          "state": "A",
          "subZone1": None,
          "subZone1Id": None,
          "subZone2": None,
          "subZone2Id": None,
          "subZone3Id": None,
          "subZones3": None,
          "thirdPartyId": 2296,
          "updateBy": "JAPeTo",
          "updateDate": "Wed, 10 Aug 2016 08:32:07 GMT",
          "zone": None,
          "zoneId": None
        }
        # envio la peticion al sevidor
        response = self.request_post(data)
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))

        self.assertIn("customerId", response.json)
        self.customerId = response.json['customerId']

        data_copy = copy(data)
        data_copy['customerId'] = self.customerId
        data_copy["name"] = "CLNUPDATE"
        data_copy["shipZipCode"] = None
        data_copy["creditCapacity"]= 12000

        # envio la peticion al sevidor
        response = self.request_put(data_copy)

        self.assertEqual('405 METHOD NOT ALLOWED', response.status,
                         '405 METHOD NOT ALLOWED is correct response')

        # envio la peticion al sevidor
        response = self.request_put(data_copy, "/"+str(self.customerId))
        # convierto a json object
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('ok', response.json)

        #*******************************
        response = self.request_get("", "/"+str(self.customerId))
        response.json = json.loads( response.data.decode("utf-8") )

        self.assertIn("contactList", response.json)
        self.assertIsNone(response.json["contactList"][0]['businessAgentId'])
        self.assertIsNone(response.json["contactList"][0]['otherThirdId'])
        self.assertIsNone(response.json["contactList"][0]['payrollEntityId'])
        self.assertIsNone(response.json["contactList"][0]['employeeId'])
        self.assertEqual(self.customerId, response.json["contactList"][0]['customerId'])

        self.assertEqual(data_copy['customerId'], response.json['customerId'] )
        self.assertEqual(data_copy["name"], response.json["name"] )
        self.assertEqual(data_copy["shipZipCode"], response.json["shipZipCode"] )
        self.assertEqual(data_copy["creditCapacity"], response.json["creditCapacity"])

        response = self.request_delete(data_copy,"/"+str(self.customerId))
        response.json = json.loads(response.data.decode("utf-8"))
        self.assertIn('ok', response.json)
