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
import os
from dotenv import load_dotenv

load_dotenv()

root_path = (Path(__file__)).resolve().parents[1]

base_url = os.getenv("BASE_URL")
cases_dir = rf"{root_path}\TestCases\answer"
exchanger = rf"{root_path}\extract.yaml"
id_path = rf"{root_path}\id.yaml"

db_host = os.getenv("DB_HOST") # ip
db_port = os.getenv("DB_PORT")  # 端口
db_user = os.getenv("DB_USER")  # 用户名
db_password = os.getenv("DB_PASSWORD")  # 密码
db_database = os.getenv("DB_DATABASE")  # 库名

allure_epic: str = "项目名称：answer"
allure_feature: str = "默认特征（feature）"
allure_story: str = "默认事件（story）"

rsa_public = ""
rsa_private = ""


if __name__ == '__main__':
    print(root_path)
    print(base_url,db_host,db_port,db_user,db_password,db_database)