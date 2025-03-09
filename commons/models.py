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
from dataclasses import dataclass, field

import yaml

from commons import settings

logger = logging.getLogger(__name__)


@dataclass
class CaseInfo:
    title: str
    request: dict
    extract: dict
    validate: dict
    parametrize: list = field(default_factory=list)
    epic: str = settings.allure_epic
    feature: str = settings.allure_feature
    story: str = settings.allure_story


if __name__ == '__main__':
    with open(r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # print(data)
    case_info = CaseInfo(**data)

