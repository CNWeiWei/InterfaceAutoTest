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
from dataclasses import dataclass, asdict, field
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


class YamlFile(dict):
    def __init__(self, path):
        super().__init__()  # 初始化父类 dict
        self.path = Path(path)
        self.load()  # 链式初始化加载

    def load(self):
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}  # 加载数据，空文件返回空字典
                self.clear()  # 清空当前实例
                self.update(data)  # 更新字典内容
        else:
            logger.warning(f"File {self.path} not found, initialized empty.")
        return self  # 链式调用

    def to_yaml(self) -> str:
        return yaml.safe_dump(
            dict(self),
            allow_unicode=True,
            sort_keys=False
        )


    @classmethod
    def by_yaml(cls, yaml_str):
        data = yaml.safe_load(yaml_str) or {}
        return cls({**data})  # 通过类方法创建实例

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                dict(self),  # 直接 dump 实例本身（已继承 dict）
                stream=f,
                allow_unicode=True,
                sort_keys=False
            )
        return self  # 链式调用


if __name__ == '__main__':
    from commons.models import CaseInfo

    yaml_path = r'E:\PyP\InterfaceAutoTest\TestCases\test_1_user.yaml'
    yaml_file = YamlFile(yaml_path)
    # yaml_file.load()
    case_info = CaseInfo(**yaml_file)
    yaml_file["title"] = "查询用户信息"
    yaml_file.save()
