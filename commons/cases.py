#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: cases.py
@date: 2024 2024/9/16 9:57
@desc: 动态生成用例
"""
from pathlib import Path
import logging

import allure
import pytest
from commons.files import YamlFile
from commons.models import CaseInfo
from commons.session import Session
from commons.exchange import Exchange
from commons import settings

logger = logging.getLogger(__name__)

session = Session(settings.base_url)

_case_path = Path(settings.case_path)

exchanger = Exchange(settings.exchanger)


@allure.epic("项目名称：answer")
class TestAPI:
    ...

    @classmethod
    def find_yaml_case(cls, case_path: Path = _case_path):
        """
        搜索和加载yaml文件
        :return:
        """
        yaml_path_list = case_path.glob("**/test_*.yaml")  # 搜索当前目录及其子目录下以test_开头yaml为后缀的文件
        for yaml_path in yaml_path_list:
            # logger.info(f"load file {yaml_path=}")

            file = YamlFile(yaml_path)  # 自动读取yaml文件
            case_info = CaseInfo(**file)  # 校验yaml格式

            # logger.info(f"case_info={case_info.to_yaml()}")  # 把case_info 转成字符串，然后记录日志

            case_func = cls.new_case(case_info)  # 从yaml格式转换为pytest格式
            print(yaml_path.stem)
            setattr(cls, f"{yaml_path.stem}", case_func)  # 把pytest格式添加到类中

    @classmethod
    def new_case(cls, case_info: CaseInfo):
        ddt_data = case_info.ddt()
        print(ddt_data)

        ddt_title = [data.title for data in ddt_data]
        logger.info(f"{ddt_title=}")
        @allure.feature(case_info.feature)
        @allure.story(case_info.story)
        @pytest.mark.parametrize("case_info", ddt_data, ids=ddt_title)
        def test_func(self, case_info: CaseInfo):
            allure.dynamic.title(case_info.title)

            logger.info(f"用例开始执行：{case_info.title}".center(80, "="))

            # 0，变量替换
            new_case_info = exchanger.replace(case_info)
            logger.info(f"1，正在注入变量...")

            # 1，发送请求
            logger.info(f"2，正在请求接口...")
            resp = session.request(**new_case_info.request)

            logger.info(f"3，正在提取变量...")
            # 2，保存变量(接口关联)
            for var_name, extract_info in new_case_info.extract.items():
                print(var_name, extract_info)
                exchanger.extract(resp, var_name, *extract_info)
            # 3，断言
            logger.info(f"4，正在断言...")
            assert_case_info = exchanger.replace(case_info)  # 为断言加载变量
            print(assert_case_info)
            assert_case_info.assert_all()  # 执行断言

            logger.info(f"用例执行结束：{case_info.title}".center(80, "="))

        return test_func


# TestAPI.find_yaml_case()
if __name__ == '__main__':
    TestAPI.find_yaml_case()
    # print(TestAPI.__dict__)
