# FOFA Pro SDK 使用说明文档
## FOFA Pro API   
<a href="https://fofa.so/api"><font face="menlo">`FOFA Pro API`</font></a> 是资产搜索引擎 <a href="https://fofa.so/">`FOFA Pro`</a> 为开发者提供的 `RESTful API` 接口, 允许开发者在自己的项目中集成 `FOFA Pro` 的功能。    


## FOFA SDK
基于 `FOFA Pro API` 编写的 `python` 版 `SDK`, 方便 `python` 开发者快速将 `FOFA Pro` 集成到自己的项目中。


## 环境
### 开发环境
``` 
windows7 + Python 2.7.10 + pycharm 2016.2.3
```
### 测试环境
``` 
Ubuntu 16.04 LTS x64 +  Python 2.7.12
```
### 使用环境
`Python 2.x`   

## 获取
### `pip`
安装 `FOFA SDK` 之前，请先确认已经安装 <a href="https://pypi.python.org/pypi/pip/"><font face="menlo">pip</font></a>.   

`点击`  <a href="https://pip.pypa.io/en/stable/"><font face="menlo">pip documentation</font></a> `了解详细的说明`      


### FOFA SDK

<strong>安装</strong>  
```
pip install fofa
```
or

```
git clone https://github.com/fofapro/fofa-py.git
cd fofa-py   
python setup.py install
```

## 依赖
### Library
目前全部采用的是python内置包，可直接安装使用。
### Email & API Key   
| `Email` |用户登陆 `FOFA Pro` 使用的 `Email`|
|---------|:-----------------:|
|`Key`| 前往 <a href="https://fofa.so/my/users/info" style="color:#0000ff"><strong>`个人中心`</strong></a> 查看 `API Key` 


## Example   
``` python
# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    email, key = ('test@test.com','xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') #输入email和key
    client = fofa.Client(email, key)                                  #将email和key传入fofa.Client类进行初始化和验证，并得到一个fofa client对象
    query_str = 'header="thinkphp" || header="think_template"'
    for page in range(1,51):                                          #从第1页查到第50页
        fcoin = client.get_userinfo()["fcoin"]                        #查询F币剩余数量
        if fcoin <= 249:
            break                                                     #当F币剩249个时，不再获取数据
        data = client.get_data(query_str,page=page,fields="ip,city")  #查询第page页数据的ip和城市
        for ip,city in data["results"]:
            print "%s,%s"%(ip,city)                                   #打印出每条数据的ip和城市
```
####具体使用文档见<a href="https://github.com/fofapro/fofa-py/wiki"><font face="menlo">wiki</font></a>

## 协议
`FOFA SDK` 遵循 `MIT` 协议 <a href="https://opensource.org/licenses/mit"><font face="menlo">https://opensource.org/licenses/mit</font></a>