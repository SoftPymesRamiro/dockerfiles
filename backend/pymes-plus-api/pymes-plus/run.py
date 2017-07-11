#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# TEST
# To execute this test run python auth_test.py on 
# the Terminal. 
# Reading the defined test you'll see that we should
# expect
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from app import create_app

app = Flask(__name__)
app = create_app(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
