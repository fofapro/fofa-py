import fofa
import time
import csv
import math

file_name = "fofa%s.csv" % int(time.time())
# 读取csv
def read_csv(file_name):
    csv_list = []
    with open(file_name, 'r', encoding='utf-8_sig') as f:
        title_names = next(csv.reader(f))
        csv_reader = csv.DictReader(f, fieldnames=title_names)
        for row in csv_reader:
            d = {}
            for k, v in row.items():
                d[k] = v
            csv_list.append(d)
    return csv_list


def csv_file_w(file_name,title_name):
    with open(file_name, mode='w', newline='', encoding='utf-8_sig') as cf:
        wf = csv.writer(cf)
        wf.writerow(title_name)

def csv_file_a(file_name,data_list):
    with open(file_name, mode='a+', newline='', encoding='utf-8_sig') as cf:
        wf = csv.writer(cf)
        wf.writerow(data_list)



if __name__ == "__main__":
    email, key = ('xxxxxxxxxxxx@xxxxxx.xxxx', 'xxxxxxxxxxxxxx')  # 输入email和key
    client = fofa.Client(email, key)
    csv_file_w(file_name, ['ip地址', '端口', '协议', '国家', '地区', '城市', '域名', '操作系统', '网站server', '网站标题', '网站链接', '产品', 'fofa最后更新时间','fofa查询语法'])
    for i in read_csv('aaa.csv'):
        query_str = f'{i["product"]}'
        print(query_str)
        data = client.search(query_str, size=10000, page=1, fields="ip,port,protocol,country_name,region,city,domain,os,server,title,link,product,lastupdatetime")
        size = data["size"]
        pages = math.ceil(size / 10000)

        for i in data["results"]:
            dateinfo = {
                'ip': i[0],
                'port': i[1],
                'protocol': i[2],
                'country_name': i[3],
                'region': i[4],
                'city': i[5],
                'domain': i[6],
                'os': i[7],
                'server': i[8],
                'title': i[9],
                'link': i[10],
                'product': i[11],
                'lastupdatetime': i[12],
                'fofa_sql': query_str
            }
            print(dateinfo)
            csv_file_a(file_name, dateinfo.values())
        if size>10000:
            pages = math.ceil(size / 10000)
            print(pages)
            for page in range(2, pages+1):
                data = client.search(query_str, size=10000, page=page, fields="ip,port,protocol,country_name,region,city,domain,os,server,title,link,product,lastupdatetime")
                for i in data["results"]:
                    dateinfo = {
                        'ip':i[0],
                        'port':i[1],
                        'protocol':i[2],
                        'country_name':i[3],
                        'region':i[4],
                        'city':i[5],
                        'domain':i[6],
                        'os':i[7],
                        'server':i[8],
                        'title':i[9],
                        'link':i[10],
                        'product':i[11],
                        'lastupdatetime':i[12],
                        'fofa_sql':query_str
                    }
                    print(dateinfo)
                    csv_file_a(file_name,dateinfo.values())



