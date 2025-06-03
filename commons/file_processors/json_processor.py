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
from typing import Union, Any
from pathlib import Path
import json
from commons.file_processors.base_processor import BaseFileProcessor

logger = logging.getLogger(__name__)


class JsonProcessor(BaseFileProcessor):
    """
    用于处理 JSON 文件的类。
    提供了从文件加载 JSON 数据为字典，以及将字典保存为 JSON 文件的功能。
    """

    def __init__(self, filepath: Union[str, Path], **kwargs):
        """
        初始化 JsonFile 对象。

        Args:
            filepath: YAML 文件的路径 (可以是字符串或 pathlib.Path 对象).
        """
        super().__init__(filepath, **kwargs)
        # self.filepath: Path = Path(filepath)  # 确保 filepath 是 Path 对象

    def load(self) -> dict[str, Any]:
        """
        从 Json 文件加载数据。
        :return:
        """
        if not self.filepath.exists():
            logger.warning(f"文件 {self.filepath} 不存在.")
            raise FileNotFoundError(f"文件 {self.filepath} 不存在.")
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)
                if not isinstance(loaded_data, dict):  # 确保加载的是字典
                    logger.error(f"YAML文件 {self.filepath} 的根节点不是一个字典/映射.")
                    raise ValueError(f"YAML文件 {self.filepath} 的根节点不是一个字典/映射.")
            return loaded_data
        except json.JSONDecodeError as e:
            logger.error(f"加载 YAML 文件 {self.filepath} 时出错: {e}")
            raise e

    def save(self, data: dict, new_filepath: Union[str, Path, None] = None) -> None:
        """
        将字典数据保存到 json 文件。

        Args:
            :param data:
            :param new_filepath: 可选参数，指定新的文件路径。如果为 None，则覆盖原文件。
        """
        filepath = Path(new_filepath) if new_filepath else self.filepath
        filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,  # 允许非ASCII字符
                    sort_keys=False  # 不排序键
                )
            logger.info(f"数据已成功保存到 {filepath}")
        except (TypeError, OSError, json.JSONDecodeError) as e:
            logger.error(f"保存 JSON 文件 {filepath} 时出错: {e}")
            raise e


if __name__ == '__main__':
    # 示例用法
    json_path = r'E:\PyP\InterfaceAutoTest\TestCases\test_1_user.json'  # 你的 JSON 文件路径
    json_file = JsonProcessor(json_path)
    print(json_file.load())
    print(type(json_file))
    # json_file.save()
