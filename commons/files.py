#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: files.py
@date: 2024 2024/9/15 21:28
@desc: 读取和保存yaml文件
"""
import logging

import yaml
from commons.models import CaseInfo

logger = logging.getLogger(__name__)

class YamlFile(dict):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.load()

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)  # 字典
        if data:
            self.update(data)  # 把两个字段的内容合并

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                dict(self),
                stream=f,
                allow_unicode=True,  # allow_unicode：使用unicode编码正常显示中文
                sort_keys=False)  # sort_keys：保持原有排序


if __name__ == '__main__':
    yaml_path = r'E:\PyP\InterfaceAutoTest\TestCases\test_1_user.yaml'
    yaml_file = YamlFile(yaml_path)
    # yaml_file.load()
    case_info = CaseInfo(**yaml_file)
    yaml_file["title"] = "查询用户信息"
    yaml_file.save()
