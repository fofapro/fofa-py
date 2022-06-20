# -*- coding: utf-8 -*-
import fofa

if __name__ == "__main__":
    email, key = ('test@test.com', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # 输入email和key
    client = fofa.Client(email, key)                # 将email和key传入fofa.Client类进行初始化和验证，并得到一个fofa client对象
    query_str = 'header="thinkphp" || header="think_template"'
    for page in range(1, 51):                       # 从第1页查到第50页
        fcoin = client.get_userinfo()["fcoin"]      # 查询F币剩余数量
        if fcoin <= 249:
            break                                   # 当F币剩249个时，不再获取数据
        data = client.search(query_str, size=100, page=page, fields="ip,city")  # 查询第page页数据的ip和城市
        for ip, city in data["results"]:
            print("%s,%s" % (ip, city))              # 打印出每条数据的ip和城市
