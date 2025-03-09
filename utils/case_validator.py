#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: case_validator
@date: 2025/2/27 17:25
@desc: 
"""
import logging

logger = logging.getLogger(__name__)


class CaseValidator:
    VALIDATORS = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func):
            cls.VALIDATORS[name] = func
            return func

        return decorator

    @classmethod
    def assert_all(cls, validate: dict):
        if not validate:
            return
        for assert_type, cases in validate.items():
            logger.info(f"键：{assert_type}，值：{cases}")
            validator = cls.VALIDATORS.get(assert_type)
            logger.info(f"获取到的断言：{validator}")
            if not validator:
                raise KeyError(f"Unsupported validator: {assert_type}")
            for msg, (a, b) in cases.items():
                validator(a, b, msg)


@CaseValidator.register('equals')
def validate_equals(a, b, msg):
    logger.info(f"assert {a} == {b}, {msg}执行这段代码")
    assert a == b, msg


@CaseValidator.register('not_equals')
def validate_not_equals(a, b, msg):
    logger.info(f"assert {a} != {b}, {msg}")
    assert a != b, msg


@CaseValidator.register('contains')
def validate_contains(a, b, msg):
    logger.info(f"assert {a} in {b}, {msg}")
    assert a in b, msg


@CaseValidator.register('not_contains')
def validate_not_contains(a, b, msg):
    logger.info(f"assert {a} not in {b}, {msg}")
    assert a not in b, msg


if __name__ == '__main__':
    mock_case = {
        "validate": {
            "equals": {
                "判断相等": ["Success.", "Success."]
            },
            "not_equals": {
                "判断不相等": ["Success.", "Suc."]
            }
        }
    }

    case_validator = CaseValidator()
    print(case_validator.VALIDATORS)
    case_validator.assert_all(mock_case.get("validate"))
