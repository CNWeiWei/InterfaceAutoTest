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

from commons import settings
from commons.file_processors.file_handle import FileHandle
from commons.models import CaseInfo
from commons.session import Session
from commons.exchange import Exchange
from utils import data_driver, case_validator

logger = logging.getLogger(__name__)

session = Session(settings.base_url)

cases_dir = Path(settings.cases_dir)

exchanger = Exchange(settings.exchanger)


class TestAPI:

    @classmethod
    def find_test_cases(cls, case_dir: Path = cases_dir):
        """
        搜索和加载yaml文件
        :return:
        """
        case_path_list = case_dir.glob("**/test_*.yaml")  # 搜索当前目录及其子目录下以test_开头yaml为后缀的文件
        for case_path in case_path_list:
            logger.info(f"加载文件：{case_path}")

            file = FileHandle(case_path)  # 自动读取yaml文件
            try:
                CaseInfo(**file)  # 校验用例格式
                logger.info(f"case_info：{FileHandle.to_string(file)}")  # 把case_info 转成字符串，然后记录日志
                case_func = cls.new_case(case_path.stem, file)  # 转换为pytest格式
                # print(case_path.stem)
                setattr(cls, f"{case_path.stem}", case_func)  # 把pytest格式添加到类中
            except Exception as e:
                logger.error(e)

    @classmethod
    def new_case(cls, file_name, case_info: dict):
        test_case = data_driver.DataDriver().generate_cases(file_name, case_info)

        keys_list = list(test_case.keys())
        logger.info(f"keys_list：{keys_list}")

        values_list = list(test_case.values())
        logger.info(f"测试用例列表：{values_list}")

        driver_title = [i.get("title") for i in values_list]
        logger.info(f"driver_title={driver_title}")

        epic = case_info["epic"] if case_info["epic"] else settings.allure_epic
        logger.info(f"epic：{epic}")

        feature = case_info["feature"] if case_info["feature"] else settings.allure_feature
        logger.info(f"feature：{feature}")

        story = case_info["story"] if case_info["story"] else settings.allure_story
        logger.info(f"story：{story}")

        @allure.epic(epic)
        @allure.feature(feature)
        @allure.story(story)
        @pytest.mark.parametrize("case_key", keys_list, ids=driver_title)
        def test_func(self, case_key):
            logger.info(f"case_key：{case_key}")

            test_case_mapping = test_case.get(case_key)
            logger.info(f"测试用例：{test_case_mapping}")

            allure.dynamic.title(test_case_mapping.get("title"))

            logger.info(f"用例开始执行：{test_case_mapping.get('title')}".center(80, "="))

            # 0，变量替换
            new_case_info = exchanger.replace(test_case_mapping)
            logger.info(f"1，正在注入变量...")
            logger.info(f"new_case_info：{new_case_info}")
            # 1，发送请求
            logger.info(f"2，正在请求接口...")
            resp = session.request(**new_case_info.get("request"))

            logger.info(f"3，正在提取变量...")
            # 2，保存变量(接口关联)
            for var_name, extract_info in new_case_info.get("extract").items():
                logger.info(f"保存变量：{var_name}{extract_info}")
                exchanger.extract(resp, var_name, *extract_info)
            # 3，断言
            logger.info(f"4，正在断言...")
            assert_case_info = exchanger.replace(test_case_mapping)  # 为断言加载变量
            logger.info(f"替换变量后：{assert_case_info}")
            # assert_case_info.assert_all()  # 执行断言
            _validator = case_validator.CaseValidator()
            _validator.assert_all(assert_case_info.get("validate"))

            logger.info(f"用例执行结束：{test_case_mapping.get('title')}".center(80, "="))

        return test_func


# TestAPI.find_yaml_case()
if __name__ == '__main__':
    TestAPI.find_test_cases()
    # print(TestAPI.__dict__)
