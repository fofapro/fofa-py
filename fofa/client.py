# -*- coding: utf-8 -*-
import base64
import json
import urllib
import urllib2


class Client:
    def __init__(self,email,key):
        self.email = email
        self.key = key
        self.base_url = "https://fofa.so"
        self.search_api_url = "/api/v1/search/all"

    def get_data(self,query_str,page=1,fields=""):
        res = self.get_json_data(query_str,page,fields)
        return json.loads(res)

    def get_json_data(self,query_str,page=1,fields=""):
        api_full_url = "%s%s" % (self.base_url,self.search_api_url)
        data = {"qbase64":base64.b64encode(query_str),"email":self.email,"key":self.key,"page":page,"fields":fields}
        data = urllib.urlencode(data)
        url = "%s?%s" % (api_full_url,data)
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req).read()
            if "errmsg" in res:
                raise RuntimeError(res)
        except urllib2.HTTPError,e:
            print "errmsg："+e.read(),
            raise e
        return res
