# FOFA Pro SDK Documentation

An easy-to-use wrapper for <a href="https://fofa.info/api"><font face="menlo">FOFA Pro API</font></a> written in python. Currently support both `Python 2.7` & `Python 3.7+`

FOFA is a search engine for Internet-connected devices. `FOFA PRO API` helps developers integrate FOFA Pro data easily in their own projects.

## Documentaion
- <a href="./docs/README_EN.md"> Documentation </a>
- <a href="./docs/README_CN.md"> 中文文档 </a>

## Usage   
``` python
# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    email, key = ('test@test.com', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  
    client = fofa.Client(email, key)               
    query_str = 'header="thinkphp" || header="think_template"'                           
    data = client.search(query_str, size=100, page=1, fields="ip,city") 
    for ip, city in data["results"]:
        print("%s,%s" % (ip, city))          
```
## License
This software is licensed under <a href="https://opensource.org/licenses/mit"><font face="menlo">MIT License</a>

Copyright (C) 2023 Fofa, Inc.
