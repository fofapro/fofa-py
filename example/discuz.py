# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    config = open('../CONFIG').read()
    email, key = config.split("\n")
    client = fofa.Client(email, key)
    data = client.get_data('''host="fofa.so"''',fields="ip,city")
    for ip,city in data["results"]:
        print "%s,%s"%(ip,city)