#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Erdog, Loveforkeeps, Alluka
import base64
import json
import requests
import os
import sys


class Client:
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.info"
        self.__search_api_url = "/api/v1/search/all"
        self.__login_api_url = "/api/v1/info/my"
        self.__stats_api_url = "/api/v1/search/stats"
        self.__host_api_url = "/api/v1/host/%s"
        self.get_userinfo()  # check email and key

    def get_userinfo(self):
        """
        get user info for current user
        :return: query result in json format
            {
                "username": "sample",
                "fofacli_ver": "4.0.3",
                "fcoin": 0,
                "error": false,
                "fofa_server": true,
                "avatar": "https://nosec.org/missing.jpg",
                "vip_level": 0,
                "is_verified": false,
                "message": "",
                "isvip": false,
                "email": "username@sample.net"
            }
        """
        api_full_url = "%s%s" % (self.base_url, self.__login_api_url)
        param = {"email": self.email, "key": self.key}
        res = self.__http_get(api_full_url, param)
        return json.loads(res)

    def search(self, query_str, page=1, size=100, fields=""):
        """
        :param query_str: search string
            example: 'ip=127.0.0.1'
            example: 'header="thinkphp" || header="think_template"'
        :param page: starting page number
        :param size: number of result fit in one page
        :param fields: query field
            example: 'ip,city'
        :return: query result in json format
            {
                "results": [
                    [
                        "111.**.241.**:8111",
                        "111.**.241.**",
                        "8111"
                    ],
                    [
                        "210.**.181.**",
                        "210.**.181.**",
                        "80"
                    ]
                ],
                "mode": "extended",
                "error": false,
                "query": "app=\"网宿科技-公司产品\"",
                "page": 1,
                "size": 2
            }
        """
        uri = self.__search_api_url
        res = self.__get_json_data(uri, query_str, page, size, fields)
        return json.loads(res)

    def search_stats(self, query_str, page=1, size=100, fields=""):
        """
        :param query_str: search string
            example: 'ip=127.0.0.1'
            example: 'header="thinkphp" || header="think_template"'
        :param page: starting page number
        :param size: number of result fit in one page
        :param fields: query field
            example: 'ip,city'
        :return: query result in json format
            {
                "distinct": {
                    "ip": 1717,
                    "title": 411
                },
                "lastupdatetime": "2022-06-17 13:00:00",
                "aggs": {
                    "title": [
                        {
                            "count": 35,
                            "name": "百度一下，你就知道"
                        },
                        {
                            "count": 25,
                            "name": "百度网盘-免费云盘丨文件共享软件丨超大容量丨存储安全"
                        },
                        {
                            "count": 16,
                            "name": "百度智能云-登录"
                        },
                        {
                            "count": 2,
                            "name": "百度翻译开放平台"
                        }
                    ],
                    "countries": []
                },
                "error": false
            }
        """
        uri = self.__stats_api_url
        res = self.__get_json_data(uri, query_str, page, size, fields)
        return json.loads(res)

    def search_host(self, host, detail=False):
        """
        :param host: required ip
        :param detail: show detail info
        :return: query result in json format
           {
                "error": false,
                "host": "78.48.50.249",
                "ip": "78.48.50.249",
                "asn": 6805,
                "org": "Telefonica Germany",
                "country_name": "Germany",
                "country_code": "DE",
                "protocol": [
                    "http",
                    "https"
                ],
                "port": [
                    80,
                    443
                ],
                "category": [
                    "CMS"
                ],
                "product": [
                    "Synology-WebStation"
                ],
                "update_time": "2022-06-11 08:00:00"
            }
        """
        uri = self.__host_api_url % host
        api_full_url = "%s%s" % (self.base_url, uri)
        param = {"email": self.email, "key": self.key, "detail": detail}
        res = self.__http_get(api_full_url, param)
        return json.loads(res)

    def __get_json_data(self, uri, query_str, page=1, size=100, fields=""):
        api_full_url = "%s%s" % (self.base_url, uri)
        if sys.version > '3':
            query_str = query_str.encode()
        query_str = base64.b64encode(query_str)
        param = {"qbase64": query_str, "email": self.email, "key": self.key, "page": page, "fields": fields,
                 "size": size}
        res = self.__http_get(api_full_url, param)
        return res

    def __http_get(self, url, param):
        try:
            resp = requests.get(url=url, params=param)
            res = resp.text
        except Exception as e:
            print(e)
            raise
        return res


if __name__ == "__main__":
    env_dist = os.environ
    FOFA_EMAIL = env_dist.get('FOFA_EMAIL')
    FOFA_KEY = env_dist.get('FOFA_KEY')
    client = Client(FOFA_EMAIL, FOFA_KEY)
    print(json.dumps(client.get_userinfo(), ensure_ascii=False))
    print(json.dumps(client.search('app="网宿科技-公司产品"', page=1), ensure_ascii=False))
    print(json.dumps(client.search_host('78.48.50.249', detail=True), ensure_ascii=False))
    print(json.dumps(client.search_stats('domain="baidu.com"', fields='title'), ensure_ascii=False))