# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 22:05:13 2019

@author: Overcomer
"""

import requests as req
import os
from bs4 import BeautifulSoup as beautisp
from bs4 import NavigableString
import pymongo as pygo
#import pandas


file_name = "oil_price.html"

if os.path.isfile(file_name):
    with open(file_name, "r", encoding="utf8") as f:
        soup = beautisp(f, "lxml")
        field_name = soup.tbody.tr

        # 將欄位放入field變數裡
        field = list()

        for items in field_name:
            # 判斷是否有此屬性，參考：https://blog.csdn.net/xun527/article/details/88059666
            if hasattr(field_name.br, "decompose"):
                # 消除<br> tag
                field_name.br.decompose()
                if not isinstance(items, NavigableString):
                    # 除去\n和空白，並加入清單中
                    field.append(items.getText().replace("\n",'').replace(" ", '').replace("0.5", "5x10-1").replace("\r", ''))

        # 取得欄位和欄位值
        field_value = soup.tbody.find_all("tr")
        # print(field_value)
        print("<tr> count: %d" % len(field_value))
        # field_value = <class 'bs4.element.ResultSet'>
        # print(type(field_value))

        # 除去第一筆<tr>，第一個<tr></tr>是欄位
        field_value.pop(0)

        # 初始化oil_list_dict variable變數，儲存抓取的資料
        oil_list_dict = list()

        for item in field_value[0:]:
            data_dict = dict()
            # <tr><td>value</td>
            tag_td = item.find_all("td")

            # MongoDB data insert
            mongo_client = pygo.MongoClient("mongodb://127.0.0.1:27017")
            mongo_db = mongo_client["Oil"]
            mongo_coll = mongo_db["Price"]

            # 讀出所有的欄位值
            for num, field_items in enumerate(field):
                data_dict[field_items] = tag_td[num].getText().replace(",", '')
#                print(data_dict[field_items], end=" ")
#            print()
            # 將單筆資料放入清單
            oil_list_dict.append(data_dict)

        # 一次插入所有資料
        mongo_insert_many = mongo_coll.insert_many(oil_list_dict)
        print(mongo_insert_many)
else:
    url = "https://web.cpc.com.tw/division/mb/oil-more4.aspx"
    oil_web_respone = req.get(url)
    oil_web_respone.encoding = "utf8"

#    with open("oil_price.html", "w", encoding="utf8") as oil_price:
#        oil_price.write(oil_web_respone.text)

    soup = beautisp(oil_web_respone.text, "lxml")
    # print(soup.prettify())
    field_name = soup.tbody.tr
    # 將欄位放入field變數裡
    field = list()

    for items in field_name:
        # 判斷是否有此屬性，參考：https://blog.csdn.net/xun527/article/details/88059666
        if hasattr(field_name.br, "decompose"):
            # 消除<br> tag
            field_name.br.decompose()
            if not isinstance(items, NavigableString):
                # 除去\n和空白，並加入清單中
                field.append(items.getText().replace("\n",'').replace(" ", '').replace("0.5", "5x10-1").replace("\r", ''))

    # 取得欄位和欄位值
    field_value = soup.tbody.find_all("tr")
    # print(field_value)
    print("<tr> count: %d" % len(field_value))
    # field_value = <class 'bs4.element.ResultSet'>
    # print(type(field_value))

    # 除去第一筆<tr>，第一個<tr></tr>是欄位
    field_value.pop(0)

    # 初始化oil_list_dict variable變數，儲存抓取的資料
    oil_list_dict = list()

    for item in field_value[0:]:
        data_dict = dict()
        # <tr><td>value</td>
        tag_td = item.find_all("td")

        # MongoDB data insert
        mongo_client = pygo.MongoClient("mongodb://127.0.0.1:27017")
        mongo_db = mongo_client["Oil"]
        mongo_coll = mongo_db["Price"]

        # 讀出所有的欄位值
        for num, field_items in enumerate(field):
            data_dict[field_items] = tag_td[num].getText().replace(",", '')
#                print(data_dict[field_items], end=" ")
#            print()
        # 將單筆資料放入清單
        oil_list_dict.append(data_dict)

    # 一次插入所有資料
    mongo_insert_many = mongo_coll.insert_many(oil_list_dict)
    print(mongo_insert_many)