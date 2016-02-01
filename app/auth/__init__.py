import base64
import hashlib
import random
import string

import re

import datetime
import requests
from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__)


def random_gen(length=6):
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(length))


def sms(mobile, param):
    # req_json = request.get_json(force=True)
    # if 'mobile' in req_json:
    account_id = "440831fac8bc589759c2f62b6edfe994"
    account_token = "117bd42a8294dce09921dbac0a7988db"
    app_id = "32b7884c76f94cc18e8146e9e374ac91"
    to_number = mobile
    template_id = "12445"
    match = re.search(r'^(1(3|5|7|8)[0-9]{9})$', str(to_number))
    if not match:
        return jsonify(message="wrong mobile", mobile=to_number)
        # return {'message': "wrong mobile", "mobile": to_number}
    param = str(param) + ",2"
    # well the app is not useable so let's do it normal
    # return {'message':param,'mobile':to_number}
    print param
    # return jsonify(message="success", code=param)
    signature = hashlib.md5()
    signature.update(account_id)
    signature.update(account_token)
    # loop = True
    # while loop:
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    signature.update(timestamp)
    signaturestr = signature.hexdigest().upper()
    url = "https://api.ucpaas.com/" + "2014-06-30" + "/Accounts/" + account_id + \
          "/Messages/templateSMS?sig=" + signaturestr
    body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}' \
           % (app_id, to_number, template_id, param)
    headers = {"Authorization": base64.encodestring(account_id + ":" + timestamp).strip(),
               "Accept": "application/json",
               "Content-Type": "application/json;charset=utf-8",
               "Content-Length": len(body)
               }
    r = requests.post(url, headers=headers, data=body)
    r = r.json()['resp']['respCode']
    return r
    if r == '000000':
        return jsonify(message="success", code=param)
    else:
        print "retry now"
        # return {'message': 'mobile is required'}


from . import views
