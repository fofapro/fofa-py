#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Erdog, Loveforkeeps, Alluka
import base64
import json
import requests
import os
import sys

from retry.api import retry_call

if __name__ == '__main__':
    # 当作为脚本直接执行时的处理方式
    from exception import FofaError
else:
    # 当作为包/模块导入时的处理方式
    from .exception import FofaError


if sys.version_info[0] > 2:
    # Python 3
    def encode_query(query_str):
        encoded_query = query_str.encode()
        encoded_query = base64.b64encode(encoded_query)
        return encoded_query.decode()
else:
    # Python 2
    def encode_query(query_str):
        encoded_query = base64.b64encode(query_str)
        return encoded_query

class Client:
    def __init__(self, email='', key='', base_url='https://fofa.info', proxies=None):
        """ 初始化Client

        :param email: The Fofa Email.
        :type email: str
        :param key: The Fofa api key.
        :type key: str
        :param proxies:  A proxies array for the requests library, e.g. {'https': 'your proxy'}
        :type proxies: dict

        """
        self.email = email
        self.key = key
        self.base_url = base_url.rstrip('/')
        self._session = requests.Session()
        if proxies:
            self._session.proxies.update(proxies)
            self._session.trust_env = False

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
        return self.__do_req( "/api/v1/info/my")

    def search(self, query_str, page=1, size=100, fields="", opts={}):
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
        param = opts
        param['qbase64'] = encode_query(query_str)
        param['page'] = page
        param['fields'] = fields
        param['size'] = size
        return self.__do_req('/api/v1/search/all', param)

    def search_stats(self, query_str, page=1, size=100, fields="", opts={}):
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
        param = opts
        param['qbase64'] = encode_query(query_str)
        param['page'] = page
        param['fields'] = fields
        param['size'] = size
        return self.__do_req('/api/v1/search/stats', param)

    def search_host(self, host, detail=False, opts={}):
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
        param = opts
        param['detail'] = detail

        u = '/api/v1/host/%s' % host
        return self.__do_req(u, param)

    def __do_req(self, path, params=None, method='get'):
        u = self.base_url + path
        data = None
        req_param = {}
        if params == None:
            req_param = {
                "email": self.email,
                "key": self.key,
            }
        else:
            req_param = params
            req_param['email'] = self.email
            req_param['key'] = self.key

        if method == 'post':
            data = params
            params = None
        res = retry_call(self._session.request, fkwargs = {
            "url": u,
            "method": method,
            "data": data,
            "params": req_param,
        }, tries = 5, delay = 1, max_delay = 60, backoff=2)
        data = res.json()
        if 'error' in data and data['error']:
            raise FofaError(data['errmsg'])
        return data


if __name__ == "__main__":
    env_dist = os.environ
    FOFA_EMAIL = env_dist.get('FOFA_EMAIL')
    FOFA_KEY = env_dist.get('FOFA_KEY')
    client = Client(FOFA_EMAIL, FOFA_KEY)
    print(json.dumps(client.get_userinfo(), ensure_ascii=False))
    print(json.dumps(client.search('app="网宿科技-公司产品"', page=1), ensure_ascii=False))
    print(json.dumps(client.search_host('78.48.50.249', detail=True), ensure_ascii=False))
    print(json.dumps(client.search_stats('domain="baidu.com"', fields='title'), ensure_ascii=False))
