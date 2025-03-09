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
from pathlib import Path
import json
from commons.file_processors.base import BaseFileProcessor

logger = logging.getLogger(__name__)


class JsonProcessor(BaseFileProcessor, dict):
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
                    loaded_data = json.load(f) or {}
                    self.update(loaded_data)  # 使用加载的数据更新字典
            except json.JSONDecodeError as e:
                logger.error(f"加载 YAML 文件 {self.filepath} 时出错: {e}")
                # 保持字典为空 (已在开头 clear)
        else:
            logger.warning(f"文件 {self.filepath} 不存在, 字典保持为空.")
            # 保持字典为空 (已在开头 clear)

    @staticmethod
    def to_string(data: dict) -> str:
        """
        将字典 (自身) 转换为 YAML 格式的字符串。

        Returns:
            YAML 格式的字符串。
        """
        try:
            return json.dumps(
                dict(data),  # 使用dict转换为标准的字典
                ensure_ascii=False,  # 允许非ASCII字符
                # indent=4,  # 美化输出，缩进4个空格
                sort_keys=False  # 不排序键
            )
        except TypeError as e:
            logger.error(f"将数据转换为 JSON 字符串时出错: {e}")
            return ""

    @staticmethod
    def to_dict(data: str) -> None:
        """
        将 YAML 格式的字符串转换为字典，并更新当前字典的内容.

        Args:
            data: YAML 格式的字符串。
        """
        try:
            loaded_data = json.loads(data) or {}
            return loaded_data
        except json.JSONDecodeError as e:
            logger.error(f"将 JSON 字符串转换为字典时出错: {e}")

    def save(self, new_filepath: Union[str, Path, None] = None):
        """
        将字典数据 (自身) 保存到 YAML 文件。

        Args:
            new_filepath: 可选参数，指定新的文件路径。如果为 None，则覆盖原文件。
        """
        filepath = Path(new_filepath) if new_filepath else self.filepath

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    dict(self),  # 使用dict转换为标准的字典
                    f,
                    ensure_ascii=False,  # 允许非ASCII字符
                    indent=4,  # 美化输出，缩进4个空格
                    sort_keys=False  # 不排序键
                )
        except (TypeError, OSError) as e:
            logger.error(f"保存 JSON 文件 {filepath} 时出错: {e}")


if __name__ == '__main__':
    # 示例用法
    json_path = r'E:\PyP\InterfaceAutoTest\TestCases\test_1_user.json'  # 你的 JSON 文件路径
    json_file = JsonProcessor(json_path)
    print(json_file)
    print(type(json_file))
    json_string = JsonProcessor.to_string(json_file)
    JsonProcessor.to_dict(json_string)
    print(json_string)
    json_file.save()
