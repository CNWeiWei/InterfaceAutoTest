# interfaceAutoTest

## 简介

...

## 技术特点

...

## 环境搭建
1，安装JAVA
- 配置环境变量
```text
JAVA_HOME
java的安装路径
CLASSPATH
%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar

添加Path
%JAVA_HOME%\bin
%JAVA_HOME%\jre\bin
```

2，安装allure
- 配置环境变量
```text
添加Path
allure安装目录\bin
```


## 使用方法

### 1，创建测试项目

### 2，创建测试文件

- test_开头
- 文件以名字排序，并决定执行顺序
- 文件后缀.yaml

### 3，编写用例内容

**必填字段**

| 字段名      | 用途   | 备注               |
|----------|------|------------------|
| title    | 用例名称 |                  |
| request  | 请求参数 |                  |
| extract  | 遍历提取 | 保存在extract.yaml中 |
| validate | 接口断言 | 断言定义在CaseInfo中   |

**选填字段**

| 字段名         | 用途     | 备注 |
|-------------|--------|----|
| parametrize | 数据驱动测试 |    |
| epic        | 项目名称   |    |
| feature     | 模块名称   |    |
| story       | 功能名称   |    |

**示例**

```yaml
...

```

### 4，执行用例


