#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: exchange.py
@date: 2024 2024/9/18 21:58
@desc: 
"""
import copy
import json
import logging
import re

import allure

from commons.templates import Template
import jsonpath

from commons.files import YamlFile
from commons.models import CaseInfo

logger = logging.getLogger(__name__)


class Exchange:
    def __init__(self, path):
        self.file = YamlFile(path)

    @allure.step("提取变量")
    def extract(self, resp, var_name, attr, expr: str, index):

        resp = copy.deepcopy(resp)

        try:
            # resp中json是方法不是属性，需要手动更改为属性
            resp.json = resp.json()
        except json.decoder.JSONDecodeError:
            resp.json = {"msg": "is not json data"}

        data = getattr(resp, attr)
        if expr.startswith("/"):  # xpath
            res = None
        elif expr.startswith("$"):  # jsonpath
            data = dict(data)
            res = jsonpath.jsonpath(data, expr)
        else:  # 正则
            res = re.findall(expr, str(data))
            # print(res)
        if res:  # 如果有数据
            value = res[index]
        else:  # 如果没有数据
            value = "not data"

        logger.debug(f"{var_name} = {value}")  # 记录变量名和变量值

        self.file[var_name] = value  # 保存变量
        self.file.save()  # 持久化存储到文件

    @allure.step("替换变量")
    def replace(self, case_info: CaseInfo):
        logger.info(case_info)
        # 1，将case_info转换为字符串
        case_info_str = case_info.to_yaml()
        print(f"{case_info_str=}")
        # 2，替换字符串
        case_info_str = Template(case_info_str).render(self.file)
        print(f"{case_info_str=}")
        # 3，将字符串转换成case_info
        new_case_info = case_info.by_yaml(case_info_str)
        return new_case_info


if __name__ == '__main__':
    class MockResponse:
        text = '{"name":"张三","age":"18","data":[3,4,5],"aaa":null}'

        def json(self):
            return json.loads(self.text)


    mock_resp = MockResponse()

    # print(mock_resp.text)
    # print(mock_resp.json())
    exchanger = Exchange(r"D:\CNWei\CNW\InterfaceAutoTest\extract.yaml")
    exchanger.extract(mock_resp, "name", "json", '$.name', 0)
    exchanger.extract(mock_resp, "age", "json", '$.age', 0)
    exchanger.extract(mock_resp, "data", "json", '$.data', 0)
    exchanger.extract(mock_resp, "aaa", "json", '$.aaa', 0)
    mock_case_info = CaseInfo(
        title="单元测试",
        request={
            "data":
                {"name": "${name}", "age": "${str(age)}", "time": "${add(1,2)}"}
        },
        extract={},
        validate={}
    )
    new_mock_case_info = exchanger.replace(mock_case_info)
    print(new_mock_case_info)
