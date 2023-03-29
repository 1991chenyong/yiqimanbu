# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2023/3/28
# @Email:775375798@qq.com
# @File: test.py
from pathlib import Path
import requests


url = "https://points-mall-test.henshihui.com/warehouse/query-warehouse-list"

session = requests.session()
# headers = {"token": "NWguZUdwa25wAXYGCgQNC3YgYjoWI1MPQjoZDzUCXghvKx43JEYHXQ=="}
params = {
    "page": 0,
    "pageSize": 10,
    "searchKey": "梅鸣实物商品",
    "useType": 1,
    "s_ver": 1,
    "appId": 2473,
    "t": "NWguZUdwa25wAXYGCgQNC3YgYjoWI1MPQjoZDzUCXghvKx43JEYHXQ=="
}
# res = session.get(url=url, params=params, headers=headers)
res = session.get(url=url, params=params)
print(res.text)
