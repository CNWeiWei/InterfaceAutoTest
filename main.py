import os
import shutil
import datetime
import pytest

from commons.cases import TestAPI

TestAPI.find_yaml_case()  # 加载yaml文件

if __name__ == '__main__':
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # 1，启动框架（生成临时文件）
    # -x表示有一个用例失败后面将不执行;-v表示展示用例名称;-c,配置文件所在目录：指定pytest.ini路径;--alluredir=temp。指定数据生成目录
    pytest.main([__file__, "-x", "-v","--alluredir=temp"])
    # 2，生成HTML报告
    os.system('allure generate temp -o report --clean')  # java程序只能借助操作系统执行

    # 3，备份日志
    shutil.copy2("logs/pytest.log", f"logs/pytest_{now}.log")
