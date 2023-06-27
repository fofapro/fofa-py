# FOFA Pro SDK 使用说明文档
## FOFA Pro API   
<a href="https://fofa.info/api"><font face="menlo">`FOFA Pro API`</font></a> 是资产搜索引擎 <a href="https://fofa.info/">`FOFA Pro`</a> 为开发者提供的 `RESTful API` 接口, 允许开发者在自己的项目中集成 `FOFA Pro` 的功能。    


## 功能
  - Fofa搜索
  - 命令行接口

## FOFA SDK
基于 `FOFA Pro API` 编写的 `python` 版 `SDK`, 方便 `python` 开发者快速将 `FOFA Pro` 集成到自己的项目中。

## 安装
```shell
pip install fofa
```

## 用法

 显示所有支持的命令
```shell
fofa
```
### 设置fofa api key
| `Email` |用户登陆 `FOFA` 使用的 `Email`|
|---------|:-----------------:|
|`Key`| 前往 <a href="https://fofa.info/userInfo" style="color:#0000ff"><strong>`个人中心`</strong></a> 查看 `API Key`

  设置环境变量FOFA_EMAIL和FOFA_KEY

### count
统计查询的数量， 示例
```shell
fofa count domain=bing.com
382128
```

### download
从Fofa搜索，并下载数据为csv或json格式，示例:

```shell
fofa download 'domain=bing.com'
```

### host
查看一个域名或ip的host信息，示例

```shell
fofa host www.bing.com
{
    "asn": 59067,
    "category": [
        "其他企业应用"
    ],
    "consumed_fpoint": 0,
    "country_code": "CN",
    "country_name": "China",
    "domain": [
        "tuzhiji.com",
        "61.129.255.240:8080"
    ],
    "error": false,
    "host": "www.bing.com",
    "ip": "202.89.233.101",
    "org": "Microsoft Mobile Alliance Internet Services Co., Ltd",
    "port": [
        443,
        80,
        8080
    ],
    "product": [
        "Microsoft-RSA-TLS-CA",
        "Microsoft-RSA-TLS-CA-02"
    ],
    "protocol": [
        "https",
        "http"
    ],
    "required_fpoints": 0,
    "update_time": "2023-06-27 08:00:00"
}
```

### search
从Fofa搜索数据，并在命令行展示结果，可以使用--fields指定要输出的字段，示例

```shell
fofa search --fields ip,port,protocol,link,certs_expired,certs_match 'domain="bing.com" && cert.is_expired=true'
```

### stats
从Fofa获取搜索语句的聚合数据，并在命令行展示聚合结果，可以使用--fields指定要聚合的字段，示例

```shell
fofa stats --fields asn,port,country 'domain="bing.com" && cert.is_expired=true'
```


### 代码使用sdk

``` python
# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    email, key = ('test@test.com', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # 输入email和key
    client = fofa.Client(email, key)                # 将email和key传入fofa.Client类进行初始化和验证，并得到一个fofa client对象
    query_str = 'header="thinkphp" || header="think_template"'
    for page in range(1, 51):                       # 从第1页查到第50页
        fcoin = client.get_userinfo()["fofa_point"]      # 查询F点剩余数量
        if fcoin <= 249:
            break                                   # 当F币剩249个时，不再获取数据
        data = client.search(query_str, size=100, page=page, fields="ip,city")  # 查询第page页数据的ip和城市
        for ip, city in data["results"]:
            print "%s,%s" % (ip, city)              # 打印出每条数据的ip和城市

```


## 协议
`FOFA SDK` 遵循 `MIT` 协议 <a href="https://opensource.org/licenses/mit"><font face="menlo">https://opensource.org/licenses/mit
