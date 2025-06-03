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
import yaml
from commons.file_processors.base_processor import BaseFileProcessor

logger = logging.getLogger(__name__)


class YamlProcessor(BaseFileProcessor):
    """
    用于处理 YAML 文件的类，继承自 dict。
    提供了从文件加载、保存到文件、转换为字符串和从字符串转换的功能,
    并可以直接像字典一样访问 YAML 数据。
    """

    def __init__(self, filepath: Union[str, Path], **kwargs):
        """
        初始化 YamlFile 对象。

        Args:            filepath: YAML 文件的路径 (可以是字符串或 pathlib.Path 对象).
            data: 可选的初始数据字典。如果提供，则用该字典初始化 YamlFile。
                  如果不提供，则尝试从 filepath 加载数据。
        """
        super().__init__(filepath, **kwargs)
        # self.filepath: Path = Path(filepath)  # 确保 filepath 是 Path 对象

    def load(self) -> dict:
        """
        从 YAML 文件加载数据
        :return:
        """
        if not self.filepath.exists():
            logger.warning(f"文件 {self.filepath} 不存在.")
            raise FileNotFoundError(f"文件 {self.filepath} 不存在.")

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                loaded_data = yaml.safe_load(f)
                if not isinstance(loaded_data, dict):  # 确保加载的是字典
                    logger.error(f"YAML文件 {self.filepath} 的根节点不是一个字典/映射.")
                    raise ValueError(f"YAML文件 {self.filepath} 的根节点不是一个字典/映射.")
            return loaded_data

        except yaml.YAMLError as e:
            logger.error(f"加载 YAML 文件 {self.filepath} 时出错: {e}")
            raise e

    def save(self, data: dict, new_filepath: Union[str, Path, None] = None) -> None:
        """
        将字典数据保存到 YAML 文件。
        :param data:
        :param new_filepath: 可选参数，指定新的文件路径。如果为 None，则覆盖原文件。

        """
        filepath = Path(new_filepath) if new_filepath else self.filepath

        # 确保目标目录存在
        filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    data,
                    stream=f,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False
                )
            logger.info(f"数据已成功保存到 {filepath}")
        except (TypeError, OSError, yaml.YAMLError) as e:
            logger.error(f"保存 YAML 文件 {filepath} 时出错: {e}")
            raise e





if __name__ == '__main__':
    # 示例用法
    yaml_path = r'E:\PyP\InterfaceAutoTest\TestCases\answer\test_1_status.yaml'  # 你的 YAML 文件路径
    yaml_file = YamlProcessor(yaml_path)
    print(yaml_file.load())
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

