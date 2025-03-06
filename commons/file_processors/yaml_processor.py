#!/usr/bin/env python
# coding=utf-8

"""
@author: CNWei
@Software: PyCharm
@contact: t6i888@163.com
@file: yaml_processor
@date: 2025/3/4 17:28
@desc: 
"""
import logging
from typing import Union
from dataclasses import dataclass, asdict, field
from pathlib import Path
import yaml
from commons.file_processors.base import BaseFileProcessor

logger = logging.getLogger(__name__)


class YamlFile(BaseFileProcessor, dict):
    """
    用于处理 YAML 文件的类，继承自 dict。
    提供了从文件加载、保存到文件、转换为字符串和从字符串转换的功能,
    并可以直接像字典一样访问 YAML 数据。
    """

    def __init__(self, filepath: Union[str, Path], data: Union[dict, None] = None):
        """
        初始化 YamlFile 对象。

        Args:
            filepath: YAML 文件的路径 (可以是字符串或 pathlib.Path 对象).
            data: 可选的初始数据字典。如果提供，则用该字典初始化 YamlFile。
                  如果不提供，则尝试从 filepath 加载数据。
        """
        super().__init__()  # 初始化父类 dict
        self.filepath: Path = Path(filepath)  # 确保 filepath 是 Path 对象
        if data is not None:
            self.update(data)  # 如果提供了初始数据，则更新字典
        else:
            self.load()  # 否则，尝试从文件加载

    def load(self) -> None:
        """
        从 YAML 文件加载数据并更新字典。
        如果文件不存在或加载失败，则清空字典并记录警告/错误。
        """
        self.clear()  # 清空现有数据
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded_data = yaml.safe_load(f) or {}
                    self.update(loaded_data)  # 使用加载的数据更新字典
            except yaml.YAMLError as e:
                logger.error(f"加载 YAML 文件 {self.filepath} 时出错: {e}")
                # 保持字典为空 (已在开头 clear)
        else:
            logger.warning(f"文件 {self.filepath} 不存在, 字典保持为空.")
            # 保持字典为空 (已在开头 clear)

    def to_string(self) -> str:
        """
        将字典 (自身) 转换为 YAML 格式的字符串。

        Returns:
            YAML 格式的字符串。
        """
        try:
            return yaml.safe_dump(
                dict(self),  # 使用dict转换为标准的字典
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False
            )
        except TypeError as e:
            logger.error(f"将数据转换为 YAML 字符串时出错: {e}")
            return ""

    def to_dict(self, data: str) -> None:
        """
        将 YAML 格式的字符串转换为字典，并更新当前字典的内容.

        Args:
            data: YAML 格式的字符串。
        """
        try:
            loaded_data = yaml.safe_load(data) or {}
            self.clear()
            self.update(loaded_data)  # 清空并更新
        except yaml.YAMLError as e:
            logger.error(f"将 YAML 字符串转换为字典时出错: {e}")
            self.clear()  # 出错时也清空

    def save(self, new_filepath: Union[str, Path, None] = None):
        """
        将字典数据 (自身) 保存到 YAML 文件。

        Args:
            new_filepath: 可选参数，指定新的文件路径。如果为 None，则覆盖原文件。
        """
        filepath = Path(new_filepath) if new_filepath else self.filepath

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    dict(self),  # 使用dict转换为标准的字典
                    stream=f,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False
                )
        except (TypeError, OSError) as e:
            logger.error(f"保存 YAML 文件 {filepath} 时出错: {e}")


class StringOrDict:
    @classmethod
    def to_string(cls, data: dict) -> str:
        """
        将字典 (自身) 转换为 YAML 格式的字符串。

        Returns:
            YAML 格式的字符串。
        """
        try:
            return yaml.safe_dump(
                dict(data),  # 使用dict转换为标准的字典
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False
            )
        except TypeError as e:
            logger.error(f"将数据转换为 YAML 字符串时出错: {e}")
            return ""

    @classmethod
    def to_dict(cls, data: str) -> Union[None, dict]:
        """
        将 YAML 格式的字符串转换为字典，并更新当前字典的内容.

        Args:
            data: YAML 格式的字符串。
        """
        try:
            loaded_data = yaml.safe_load(data) or {}
            return loaded_data
        except yaml.YAMLError as e:
            logger.error(f"将 YAML 字符串转换为字典时出错: {e}")


if __name__ == '__main__':
    # 示例用法
    yaml_path = r'D:\CNWei\CNW\InterfaceAutoTest\TestCases\test_1_user.yaml'  # 你的 YAML 文件路径
    yaml_file = YamlFile(yaml_path)
    print(yaml_file)
    print(type(yaml_file))

    # # 直接像字典一样访问数据
    # print("加载的数据:", yaml_file)  # 直接打印对象，就是打印字典内容
    # print("title:", yaml_file.get("title"))  # 使用 get 方法
    # if "title" in yaml_file:  # 使用 in 检查键
    #     print("原始title:", yaml_file["title"])  # 使用方括号访问
    #     yaml_file["title"] = "新的标题"  # 使用方括号修改
    #     print("修改后的title:", yaml_file["title"])
    # #
    # yaml_file["new_key"] = "new_value"  # 添加新的键值对
    #
    # # 将字典转换为 YAML 字符串
    # yaml_string = yaml_file.to_string()
    # print("\nYAML 字符串:", yaml_string)
    # #
    # # 将 YAML 字符串转换回字典 (并更新 yaml_file)
    # yaml_file.to_dict(yaml_string)
    # print("\n从字符串加载的数据:", yaml_file)
    #
    # # 保存修改后的数据 (覆盖原文件)
    # yaml_file.save()
    #
    # # 保存到新文件
    # new_yaml_path = r'D:\CNWei\CNW\InterfaceAutoTest\TestCases\test_1_user_new.yaml'
    # yaml_file.save(new_filepath=new_yaml_path)

    # 测试从字符串初始化
    # yaml_string2 = """
    # name: Test User
    # age: 30
    # """

    # yaml_file2 = YamlFile("test2.yaml", data=yaml.safe_load(yaml_string2))  # 从字符串初始化
    # print("\n从字符串初始化的 YamlFile:", yaml_file2)
    # yaml_file2.save()  # 保存到 test2.yaml
    #
    # 测试文件不存在的情形
    # non_existent_file = YamlFile("non_existent_file.yaml")
    # print("\n加载不存在的文件:", non_existent_file)  # 应该打印空字典 {}
    # non_existent_file['a'] = 1  # 可以直接添加
    # print("\n加载不存在的文件:", non_existent_file)

# if __name__ == '__main__':
#     from commons.models import CaseInfo
#
#     yaml_path = r'D:\CNWei\CNW\InterfaceAutoTest\TestCases\test_1_user.yaml'
#     yaml_file = YamlFile(yaml_path)
#     print(yaml_file.load())
#     # yaml_file.load()
#     # case_info = CaseInfo(**yaml_file)
#     # print(case_info)
#     # yaml_file["title"] = "查询用户信息"
#     # yaml_file.save()
