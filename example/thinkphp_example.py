# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    config = open('../CONFIG').read()
    email, key = config.split("\n")
    client = fofa.Client(email, key)
    query_str = 'header="thinkphp" || header="think_template"'
    for page in range(1,51):
        # fcoin = client.get_userinfo()["fcoin"]
        # if fcoin <= 249:
        #     break
        data = client.get_data(query_str,size=100,page=page,fields="ip,city")
        for ip,city in data["results"]:
            print "%s,%s"%(ip,city)