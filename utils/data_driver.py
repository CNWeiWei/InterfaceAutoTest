#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: data_driver
@date: 2025/3/3 10:56
@desc: 
"""

from commons.models import CaseInfo
from commons.templates import Template


class DataDriver:
    @staticmethod
    def generate_cases(case_info) -> list:
        if not case_info.get("parametrize"):
            return [case_info]

        cases = []
        args_names = case_info.get("parametrize")[0]
        for args_values in case_info.get("parametrize")[1:]:
            print(args_values)
            context = dict(zip(args_names, args_values))
            print(context)
            rendered = Template(CaseInfo(**case_info).to_yaml()).render(context)
            cases.append({args_names[0]:CaseInfo(**case_info).by_yaml(rendered)})
        return cases


if __name__ == '__main__':
    mock_case_info = {
        "case_info0": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [[ "title","username","password","msg" ] ,[ "测试1","user1","pass1","200" ] ,[ "测试2","user2","pass2","300" ]]
        },
        "case_info1": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [1,2,3]
        },
        "case_info2": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [1,2,3]
        }

    }

    dd = DataDriver()
    cases = dd.generate_cases(mock_case_info.get("case_info0"))
    print(cases)