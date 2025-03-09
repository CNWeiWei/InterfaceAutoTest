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
from pathlib import Path

from commons.templates import Template
from commons.file_processors.file_handle import FileHandle


class DataDriver:
    @staticmethod
    def generate_cases(file_name, case_info) -> dict:

        if not case_info.get("parametrize"):
            return {file_name + "[--]": case_info}

        cases = {}
        args_names = case_info.get("parametrize")[0]
        for i, args_values in enumerate(case_info.get("parametrize")[1:]):
            # print(args_values)
            context = dict(zip(args_names, args_values))
            # print(context)
            rendered = Template(FileHandle.to_string(case_info)).render(context)
            cases.update({file_name + "[" + str(i) + "]": FileHandle.to_dict(rendered)})

        return cases


if __name__ == '__main__':

    file_path = Path(r"E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml")

    file_obj = FileHandle(file_path)
    print(file_path.stem)
    file_name_ = file_path.stem
    # mock_case_info = {
    #     "case_info0": {
    #         "feature": "页面状态",
    #         "story": "状态",
    #         "title": "查询状态信息",
    #         "request": "",
    #         "extract": "",
    #         "validate": "",
    #         "parametrize": [["title", "username", "password", "msg"], ["测试1", "user1", "pass1", "200"],
    #                         ["测试2", "user2", "pass2", "300"]]
    #     },
    #     "case_info1": {
    #         "feature": "页面状态",
    #         "story": "状态",
    #         "title": "查询状态信息",
    #         "request": "",
    #         "extract": "",
    #         "validate": "",
    #         "parametrize": [1, 2, 3]
    #     },
    #     "case_info2": {
    #         "feature": "页面状态",
    #         "story": "状态",
    #         "title": "查询状态信息",
    #         "request": "",
    #         "extract": "",
    #         "validate": "",
    #         "parametrize": [1, 2, 3]
    #     }
    #
    # }

    dd = DataDriver()
    # cases = dd.generate_cases(mock_case_info.get("case_info0"))
    cases_ = dd.generate_cases(file_name_, file_obj)
    print(cases_)
    case_keys = list(cases_.keys())
    case_values = cases_.values()

    print(case_keys)
    print(case_values)
    aa = [i.get("title") for i in case_values]
    print(aa)
    # print(list(case_values)[0]["feature"])
    print(file_obj["feature"])
    # print(list(case_values)[0]["story"])
    print(file_obj["story"])

