#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: header_transition.py
@date: 2024 2024/9/17 17:34
@desc: 
"""
import re

headerStr = '''
Accept-Encoding: gzip, deflate
Accept-Language: zh_CN
Content-Type: application/json
Cookie: psession=33c6c2de-7e5d-40e2-9bbc-3c637a690c3f; lang=zh-CN; 3x-ui=MTcyNjU2NDcwOHxEWDhFQVFMX2dBQUJFQUVRQUFCMV80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWhoNExYVnBMMlJoZEdGaVlYTmxMMjF2WkdWc0xsVnpaWExfZ1FNQkFRUlZjMlZ5QWYtQ0FBRUVBUUpKWkFFRUFBRUlWWE5sY201aGJXVUJEQUFCQ0ZCaGMzTjNiM0prQVF3QUFRdE1iMmRwYmxObFkzSmxkQUVNQUFBQUdQLUNGUUVDQVFkNGRXa3lNREkwQVFkNGRXa3lNREkwQUE9PXwLOhLRIDjzvQ3oI-UF-GhkMheEENkxRJ8GkAZ79eFHvg==
Host: 119.91.19.171:40065
Origin: http://119.91.19.171:40065
Referer: http://119.91.19.171:40065/users/login
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0
'''
ret = ""
for i in headerStr:
    if i == '\n':
        i = "',\n"
    ret += i

ret = re.sub(": ", ": '", ret)
print(ret[3: -3])
