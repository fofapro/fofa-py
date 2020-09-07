#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Erdog
import base64
import json
import requests
import os
import sys

# Python版本识别
if sys.version > '3':
    PY3 = True
else:
    PY3 = False


class Client:
    def __init__(self, email, key, debug=False):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.debug = debug
        self.get_userinfo()  # check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url, self.login_api_url)
        param = {"email": self.email, "key": self.key}
        if self.debug:
            print(api_full_url, param)
        res = self.__http_get(api_full_url, param)
        return json.loads(res)

    def get_data(self, query_str, page=1, fields="", size=100):
        res = self.get_json_data(query_str, page, fields)
        return json.loads(res)

    def get_json_data(self, query_str, page=1, fields="", size=100):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        if PY3:
            query_str = query_str.encode()
        query_str = base64.b64encode(query_str)
        param = {"qbase64": query_str, "email": self.email, "key": self.key, "page": page, "fields": fields, "size": size}
        res = self.__http_get(api_full_url, param)
        return res

    def __http_get(self, url, param):
        try:
            resp = requests.get(url=url, params=param)
            res = resp.text
            if self.debug:
                print(res)
        except Exception as e:
            print(e)
            raise
        return res


if __name__ == "__main__":
    env_dist = os.environ
    FOFA_EMAIL = env_dist.get('FOFA_EMAIL')
    FOFA_KEY = env_dist.get('FOFA_KEY')
    client = Client(FOFA_EMAIL, FOFA_KEY, debug=True)
    client.get_data('app="网宿"', page=1)
