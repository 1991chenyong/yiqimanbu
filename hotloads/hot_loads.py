import yaml
import re
from debugtalk import DebugTalk
from common.common_util import read_extract_yaml

# 处理热加载数据
def replace_load(testcase_info):
    # 两个括号里的条件同时满足才能返回数据
    regx = re.compile('\$\{(.+?)\((.*?)\)}')
    fun_list = regx.findall(testcase_info)
    # [('get_user', 'name, age')]
    if fun_list:
        for fun in fun_list:
            if not len(fun[1]):
                new_data = getattr(DebugTalk(), fun[0])()
                old_data = '${' + fun[0] + '()' + '}'
                testcase_info = testcase_info.replace(old_data, new_data)
            else:
                new_data = str(getattr(DebugTalk(), fun[0])(*tuple(fun[1].split(','))))
                old_data = '${' + fun[0] + '(' + fun[1] + ')' + '}'
                testcase_info = testcase_info.replace(old_data, new_data)
    return testcase_info

# 处理关联取值
def replace_value(testcase_info):
    regx = "\{\{(.+?)\}\}"
    params_list = re.compile(regx).findall(testcase_info)
    for params in params_list:
        old_str = '{{'+params+'}}'
        new_str = read_extract_yaml(params)
        testcase_info = testcase_info.replace(old_str, str(new_str))
    return testcase_info

