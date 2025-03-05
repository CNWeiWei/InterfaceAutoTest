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

from commons.models import CaseInfo
from commons.templates import Template
from commons.file_processors.yaml_processor import StringOrDict


class DataDriver:
    @staticmethod
    def generate_cases(file_name, case_info) -> list:

        if not case_info.get("parametrize"):
            return {file_name + "[--]": case_info}

        # cases = []
        args_names = case_info.get("parametrize")[0]
        for i, args_values in enumerate(case_info.get("parametrize")[1:]):
            # print(args_values)
            context = dict(zip(args_names, args_values))
            # print(context)
            # rendered = Template(CaseInfo(**case_info).to_yaml()).render(context)
            rendered = Template(StringOrDict.to_string(case_info)).render(context)
            # cases.append({file_name + "[" + str(i) + "]": StringOrDict.to_dict(rendered)})
            yield {file_name + "[" + str(i) + "]": StringOrDict.to_dict(rendered)}
        # return cases


if __name__ == '__main__':
    from commons.file_processors.yaml_processor import YamlFile

    file_path = Path(r"E:\PyP\InterfaceAutoTest\TestCases\test_1_user.yaml")

    file_obj = YamlFile(file_path)
    # print(file_path.stem)
    file_name = file_path.stem
    mock_case_info = {
        "case_info0": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [["title", "username", "password", "msg"], ["测试1", "user1", "pass1", "200"],
                            ["测试2", "user2", "pass2", "300"]]
        },
        "case_info1": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [1, 2, 3]
        },
        "case_info2": {
            "feature": "页面状态",
            "story": "状态",
            "title": "查询状态信息",
            "request": "",
            "extract": "",
            "validate": "",
            "parametrize": [1, 2, 3]
        }

    }

    dd = DataDriver()
    # cases = dd.generate_cases(mock_case_info.get("case_info0"))
    cases = dd.generate_cases(file_name, file_obj)
    # print(cases)
    # print(len(cases))
    keys_list = []
    titles = []
    for item in cases:
        print(item)
        # 遍历列表中的每个字典
        for key, value in item.items():
            print(f"key:{key}")
            keys_list.append(key)
            print(f"value:{value}")
        #     # 遍历内层字典（这里内层字典其实只有一个键值对）
            titles.append(value['title'])
        print(item)

    print(keys_list)
    print(titles)

    # ddt_title = [data.title for data in ddt_data]
    # logger.info(f"{ddt_title=}")
