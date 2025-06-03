#!/usr/bin/env python
# coding=utf-8

"""
@author: chen wei
@Software: PyCharm
@contact: t6i888@163.com
@file: models.py
@date: 2024 2024/9/15 21:14
@desc: 声明yaml用例格式
"""
import logging
from typing import Union, Optional
from dataclasses import dataclass, field

import yaml

from commons import settings

logger = logging.getLogger(__name__)


@dataclass
class RequestModel:
    method: str
    url: str
    headers: Optional[dict] = None
    # body: Optional[Union[dict, str]] = None
    params: Optional[Union[dict, str]] = None


@dataclass
class TestCaseModel:
    title: str
    request: RequestModel
    extract: dict
    validate: dict
    parametrize: list = field(default_factory=list)
    epic: str = field(default_factory=lambda: settings.allure_epic)
    feature: str = field(default_factory=lambda: settings.allure_feature)
    story: str = field(default_factory=lambda: settings.allure_story)

    def __post_init__(self):
        # 必填字段非空校验
        if self.title is None:
            raise ValueError("Title cannot be empty")

            # 校验RequestModel
        if isinstance(self.request, dict):
            try:
                self.request = RequestModel(**self.request)  # RequestModel 的 __post_init__ 会被调用
            except (TypeError, ValueError) as e:
                raise ValueError(f"解析 'request' 字段失败: {e} (数据: {self.request})") from e
        elif not isinstance(self.request, RequestModel):  # 如果不是 dict 也不是 RequestModel
            raise TypeError(
                f"字段 'request' 必须是字典 (将在内部转换为 RequestModel) 或 RequestModel 实例, "
                f"得到的是 {type(self.request).__name__}"
            )


if __name__ == '__main__':
    with open(r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # print(data)
    case_info = TestCaseModel(**data)
