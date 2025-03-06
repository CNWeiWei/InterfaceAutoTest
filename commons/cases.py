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
from commons.file_processors.yaml_processor import YamlFile
from commons.models import CaseInfo
from commons.session import Session
from commons.exchange import Exchange
from utils import data_driver

logger = logging.getLogger(__name__)

session = Session(settings.base_url)

_case_path = Path(settings.case_path)

exchanger = Exchange(settings.exchanger)


@allure.epic("项目名称：answer")
class TestAPI:

    @classmethod
    def find_yaml_case(cls, case_path: Path = _case_path):
        """
        搜索和加载yaml文件
        :return:
        """
        yaml_path_list = case_path.glob("**/test_*.yaml")  # 搜索当前目录及其子目录下以test_开头yaml为后缀的文件
        for yaml_path in yaml_path_list:
            logger.info(f"加载文件：{yaml_path}")

            file = YamlFile(yaml_path)  # 自动读取yaml文件

            case_info = CaseInfo(**file)  # 校验yaml格式

            logger.info(f"case_info={case_info.to_yaml()}")  # 把case_info 转成字符串，然后记录日志
            # case_info = {yaml_path.stem:case_info}
            # logger.info(f"case_info_dict={case_info}")
            case_func = cls.new_case(yaml_path.stem, file)  # 从yaml格式转换为pytest格式
            print(yaml_path.stem)
            setattr(cls, f"{yaml_path.stem}", case_func)  # 把pytest格式添加到类中

    @classmethod
    def new_case(cls,file_name, case_info: dict):
        case_data = data_driver.DataDriver().generate_cases(file_name,case_info)
        # ddt_data = case_info.ddt()
        keys_list = ['test_1_user[0]', 'test_1_user[1]', 'test_1_user[2]', 'test_1_user[3]']
        titles = ['查询用户信息', '查询用户信息', '查询用户信息', '查询用户信息']
        for item in case_data:
            # 遍历列表中的每个字典
            for key, value in item.items():
                print(f"key:{key}")
                keys_list.append(key)
                print(f"value:{value}")
                #     # 遍历内层字典（这里内层字典其实只有一个键值对）
                titles.append(value['title'])
        print(f"测试数据：{case_data}")
        item={'test_1_user[0]': {'feature': '特征', 'story': '事件', 'title': '查询用户信息', 'request': {'method': 'get', 'url': 'http://119.91.19.171:40065/answer/api/v1/connector/info', 'headers': {'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh_CN', 'Content-Type': 'application/json', 'Cookie': 'psession=33c6c2de-7e5d-40e2-9bbc-3c637a690c3f; lang=zh-CN; 3x-ui=MTcyNjU2NDcwOHxEWDhFQVFMX2dBQUJFQUVRQUFCMV80QUFBUVp6ZEhKcGJtY01EQUFLVEU5SFNVNWZWVk5GVWhoNExYVnBMMlJoZEdGaVlYTmxMMjF2WkdWc0xsVnpaWExfZ1FNQkFRUlZjMlZ5QWYtQ0FBRUVBUUpKWkFFRUFBRUlWWE5sY201aGJXVUJEQUFCQ0ZCaGMzTjNiM0prQVF3QUFRdE1iMmRwYmxObFkzSmxkQUVNQUFBQUdQLUNGUUVDQVFkNGRXa3lNREkwQVFkNGRXa3lNREkwQUE9PXwLOhLRIDjzvQ3oI-UF-GhkMheEENkxRJ8GkAZ79eFHvg==', 'Host': '119.91.19.171:40065', 'Origin': 'http://119.91.19.171:40065', 'Referer': 'http://119.91.19.171:40065/users/login', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'}}, 'extract': {'code': ['json', '$.code', 0], 'msg': ['json', '$.msg', 0]}, 'validate': {'equals': {'状态码等于200': [200, 'code1']}, 'not_equals': {'状态码不等于404': [404, 'code1']}, 'contains': {'包含关系': [404, 'code1']}, 'not_contains': {'不包含关系': [404, 'code1']}}, 'parametrize': [['title', 'username', 'password', 'code'], ['测试1', 'user1', 'pass1', 'code1'], ['测试2', 'user2', 'pass2', 'code2'], ['测试3', 'user3', 'pass3', 'code3'], ['测试4', 'user4', 'pass4', 'code4']]}}
        # ddt_title = [data.title for data in ddt_data]
        # logger.info(f"{ddt_title=}")
        logger.info(f"keys_list={keys_list}")
        logger.info(f"titles={titles}")
        logger.info(f"feature={case_info.get('feature')}")
        logger.info(f"story={case_info.get('story')}")
        @allure.feature(case_info.get("feature"))
        @allure.story(case_info.get("story"))
        @pytest.mark.parametrize("case_key", keys_list, ids=titles)
        def test_func(self, case_key):
            logger.info(f"case_key={case_key}")
            item.get(case_key)
            logger.info(f"========:{item}")
            logger.info(f"========:{item.get(case_key)}")
            allure.dynamic.title(case_info.get("title"))

            logger.info(f"用例开始执行：{case_info.get('title')}".center(80, "="))

            # 0，变量替换
            new_case_info = exchanger.replace(case_info)
            logger.info(f"1，正在注入变量...")
            logger.info(f"new_case_info={new_case_info}")
            # 1，发送请求
            logger.info(f"2，正在请求接口...")
            resp = session.request(**new_case_info.get("request"))

            logger.info(f"3，正在提取变量...")
            # 2，保存变量(接口关联)
            new_case_info = CaseInfo(**new_case_info)
            for var_name, extract_info in new_case_info.extract.items():
                # logger.info(f"保存变量：{var_name}{extract_info}")
                exchanger.extract(resp, var_name, *extract_info)
            # 3，断言
            logger.info(f"4，正在断言...")
            assert_case_info = exchanger.replace(case_info)  # 为断言加载变量
            # logger.info(f"替换变量后：{assert_case_info}")
            assert_case_info.assert_all()  # 执行断言

            logger.info(f"用例执行结束：{case_info.title}".center(80, "="))

        return test_func


# TestAPI.find_yaml_case()
if __name__ == '__main__':
    TestAPI.find_yaml_case()
    # print(TestAPI.__dict__)
