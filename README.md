# FOFA Python SDK Documentation

An easy-to-use wrapper for <a href="https://fofa.info/api"><font face="menlo">FOFA API</font></a> written in python. Currently support `Python 3.7+`

FOFA is a search engine for Internet-connected devices. `FOFA API` helps developers integrate FOFA data easily in their own projects.

## Documentaion
- <a href="./docs/README_EN.md"> Documentation </a>
- <a href="./docs/README_CN.md"> 中文文档 </a>
- [Api Documentation](https://fofapro.github.io/fofa-py/index.html)

## Usage   
``` python
# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    client = fofa.Client(key)               
    query_str = 'header="thinkphp" || header="think_template"'                           
    data = client.search(query_str, size=100, page=1, fields="ip,city") 
    for ip, city in data["results"]:
        print("%s,%s" % (ip, city))          
```
## License
This software is licensed under <a href="https://opensource.org/licenses/mit"><font face="menlo">MIT License</a>

Copyright (C) 2023 Fofa, Inc.
