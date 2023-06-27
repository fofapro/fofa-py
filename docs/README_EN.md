# FOFA Pro SDK Documentation
## FOFA Pro API   
An easy-to-use wrapper for <a href="https://fofa.info/api"><font face="menlo">FOFA Pro API</font></a> written in python. Currently support both `Python 2.7` & `Python 3.7+`

FOFA is a search engine for Internet-connected devices. `FOFA PRO API` helps developers integrate FOFA Pro data easily in their own projects.

## Usage
``` python
# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    email, key = ('test@test.com', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # enter email and key
    client = fofa.Client(email, key)                # init fofa client
    query_str = 'header="thinkphp" || header="think_template"'
    for page in range(1, 51):                       # search from page 1-50
        fcoin = client.get_userinfo()["fcoin"]      # check fcoin count
        if fcoin <= 249:
            break                                   # stop request if fcoin less than 249
        data = client.search(query_str, size=100, page=page, fields="ip,city")  # query ip & city for each page
        for ip, city in data["results"]:
            print "%s,%s" % (ip, city)              # print ip & city in each result

```
#### check <a href="https://github.com/fofapro/fofa-py/wiki"><font face="menlo">wiki</font></a> for more detail

## Install
- `pip`

  - Install <a href="https://pypi.python.org/pypi/pip/"><font face="menlo">pip</font></a> before use `FOFA SDK`.

  - For more information, check:  <a href="https://pip.pypa.io/en/stable/"><font face="menlo">pip documentation</font></a> 


- FOFA SDK
    ```
    pip install fofa
    ```
    or
    
    ```
    git clone https://github.com/fofapro/fofa-py.git
    cd fofa-py   
    python setup.py install
    ```

### Email & API Key   
| `Email` |`Email` Used for `FOFA Pro` Login|
|---------|:-----------------:|
|`Key`| `API Key` in <a href="https://fofa.info/userInfo" style="color:#0000ff"><strong>`个人中心`(userinfo)</strong></a> 

## License
This software is licensed under <a href="https://opensource.org/licenses/mit"><font face="menlo">MIT License</a>

Copyright (C) 2022 Fofa, Inc.
