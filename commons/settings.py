#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: settings
@date: 2025/2/23 21:34
@desc: 
"""
from pathlib import Path

root_path = (Path(__file__)).resolve().parents[1]

base_url = 'http://127.0.0.1:40065'
case_path = rf"{root_path}\TestCases\answer"
exchanger = rf"{root_path}\extract.yaml"
id_path = rf"{root_path}\id.yaml"

db_host = '127.0.0.1'  # ip
db_port = 3306  # 端口
db_user = 'root'  # 用户名
db_password = 'password'  # 密码
db_database = 'answer'  # 库名

allure_epic: str = "项目名称：answer"
allure_feature: str = "默认特征（feature）"
allure_story: str = "默认事件（story）"

rsa_public = ""
rsa_private = ""


if __name__ == '__main__':
    print(root_path)