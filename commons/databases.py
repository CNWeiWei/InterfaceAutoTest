#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: databases
@date: 2025/2/16 20:53
@desc: 
"""
import logging
import pymysql as MySQLdb

from commons import settings

logger = logging.getLogger(__name__)


class DBServer:
    def __init__(self, host, port, user, password, database):
        self.db = MySQLdb.connect(host=host, port=port, user=user, password=password, database=database)
        self.cursor = self.db.cursor()  # 创建新的会话

    def execute_sql(self, sql):
        logger.info(f"执行sql：{sql}")
        self.cursor.execute(sql)  # 执行sql命令

        # res = self.cursor.fetchone() # 返回单行结果
        res = self.cursor.fetchall()  # 返回多行结果
        return res


db = DBServer(
    host=settings.db_host,  # ip
    port=3306,  # 端口
    user='root',  # 用户名
    password='mysql_hNahSe',  # 密码
    database='answer'  # 库名
)

if __name__ == '__main__':
    ...
    res = db.execute_sql('select username from user where id=1;')
    print(res[0])
