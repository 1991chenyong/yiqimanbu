# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2023/3/28
# @Email:775375798@qq.com
# @File: test.py
from pathlib import Path
from common.parameters_util import read_testcase_yaml
import pytest
import allure
from common.requests_util import RequestUtil

# 当前路径
current_path = Path(__file__).parent
print(current_path)
# 找到所有的代表测试用例的yaml文件
# yaml_case_list = current_path.glob('**/*.yaml')
# for i in yaml_case_list:
#     print(i.name[:-5])

# 创建用例的方法
def create_testcase():
    def test_func(yaml_path):
        return yaml_path
    return test_func

class TestAllApi:
    pass

setattr(TestAllApi,'cy',create_testcase())
test = TestAllApi.cy
print(TestAllApi.cy("ddd"))





