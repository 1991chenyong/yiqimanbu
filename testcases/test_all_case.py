# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2023/3/13
# @Email:775375798@qq.com
# @File: test_all_case.py
from pathlib import Path
from common.parameters_util import read_testcase_yaml
import pytest
import allure
from common.requests_util import RequestUtil

# 当前路径
current_path = Path(__file__).parent
# 找到所有的代表测试用例的yaml文件
yaml_case_list = current_path.glob('**/*.yaml')

# 创建用例的方法
allure.epic("一起漫部项目后台接口")
def create_testcase(yaml_path):
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml(yaml_path))
    def test_func(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)
    return test_func

class TestAllApi:
    pass

# 循环所有的yaml用例的文件名
for yaml_path in yaml_case_list:
    yaml_name = yaml_path.name[:-5]
    # 表示再类中增加一个名字为yaml_name的测试用例
    setattr(TestAllApi,yaml_name,create_testcase(yaml_path))

if __name__ == "__main__":
    pass

