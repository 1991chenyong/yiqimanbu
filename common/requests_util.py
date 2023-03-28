import traceback
import json
from io import StringIO
import requests
import yaml
import common.common_util as common_util
import jsonpath
import re
from common.global_args import load_ini
from common.logger_util import write_log, write_error_log
from common.assert_util import result_validate
from hotloads.hot_loads import replace_load, replace_value
import logging


#获得日志对象
logger = logging.getLogger(__name__)

class RequestUtil(object):

    sessions =requests.session()

    def __init__(self):
        # 初始化一个基础路径
        self.base_url = common_util.read_config_yaml('base', 'base_url')

    # 封装提取变量(json提取器,正则表达式提取器)
    def analysic_extract(self, casetest_info, res):
        if jsonpath.jsonpath(casetest_info, '$..extract'):
            # print("************%s" % casetest_info['extract'])
            for key, value in dict(casetest_info['extract']).items():
                if '(.+?)' in value or '(.*?)' in value:
                    logger.info("进入正则提取判断")
                    zz_value = re.findall(value, res.text)
                    if zz_value:
                        if len(zz_value) == 1:
                            # 提取到一个值
                            common_util.write_extract_yaml({key: zz_value[0]})
                            # write_log("--------------提取到的值是：%s" % zz_value[0])
                        else:
                            #提取到多个值
                            common_util.write_extract_yaml({key: zz_value})
                            # write_log("--------------提取到的多个值是：%s"%str(zz_value))
                        logger.info("--------------------%s提取成功--------------------\n\n" % key)
                    else:
                        # write_error_log("提取%s失败"%key)
                        write_error_log("提取%s失败"%key)
                elif key == value:
                    logger.info("进入json提取判断")
                    json_result = res.json()
                    temp_data = jsonpath.jsonpath(json_result, '$..%s' % value)
                    if temp_data:
                        data_dict = {key: temp_data[0]}
                        common_util.write_extract_yaml(data_dict)
                        logger.info("--------------------%s提取成功--------------------\n\n" % key)
                # 此判断适用于提取的键值在返回的数据中存在且返回的数据为json
                elif value:
                    json_result = res.json()
                    logger.info("进入通过key值提取数据场景")
                    temp_data = jsonpath.jsonpath(json_result, '$..%s' % value)
                    if temp_data:
                        data_dict = {key: temp_data[0]}
                        common_util.write_extract_yaml(data_dict)
                        logger.info("--------------------%s提取成功--------------------\n\n" % key)
                else:
                    write_error_log("暂不支持该提取方式")

    # 封装的分析yaml测试用例文件的方法
    def analysis_yaml(self, testcase_info):
        """
        :param casetest_info: yaml测试用例数据
        :return: 无
        """
        # 判断：name,request,validate关键字是否存在
        testcase_info = dict(testcase_info)
        keys = testcase_info.keys()
        #if 'name' in keys and 'request' in keys and 'validate' in keys:
        if set(keys).issuperset({"name", "request", "validate","project"}):
            request_data = testcase_info["request"]
            request_keys = request_data.keys()
            # if 'url' in request_keys and 'method' in request_keys:
            if set(request_keys).issuperset({"url", "method"}):
                testcase_str = yaml.dump(testcase_info)  # 将字典格式转化为字符串
                testcase_str = replace_load(testcase_str)  # 热加载处理
                testcase_str = replace_value(testcase_str)  # 参数请求替换
                testcase_info = yaml.safe_load(StringIO(testcase_str))  # 将字符串转化为字典
                request_data = testcase_info["request"]     #进行替换操作后，重新赋值
                if set(request_keys).issuperset({"params"}):
                    request_data["params"].update(load_ini(testcase_info["project"]))
                else:
                    request_data["params"] = {}
                    request_data["params"].update(load_ini(testcase_info["project"]))
                if set(request_keys).issuperset({'files'}):
                    for key, value in request_data["files"].items():
                        request_data["files"][key] = open(value, 'rb')
                # 收集日志
                logger.info("------------------------接口请求开始-------------------------")
                logger.info("接口名称：%s" % testcase_info['name'])
                for key, value in testcase_info['request'].items():
                    logger.info("用例%s参数: %s" % (key, value))
                res = self.send_request(**request_data)
                logger.info("接口返回数据：%s" % res.text)
                # 断言返回结果
                if testcase_info["validate"]:
                    yq_result = testcase_info['validate']
                    result_validate(yq_result=yq_result, real_result=res)
                    # 提取变量
                    self.analysic_extract(testcase_info, res)
                    logger.info("------------------------接口请求结束-------------------------")
                    return res.json()
            else:
                write_error_log("request必须包含二级关键字：url、method!")
        else:
            write_error_log("测试用例一级关键字不符合规则")

    def send_request(self, **kwargs):
        # print("kwargs====", kwargs)
        res = RequestUtil.sessions.request(**kwargs)
        return res

if __name__ == "__main__":
    url = "http://miniprogram-aiduifen-test.tongdui8.com/superAdmin/user-manage/give-adfun"
    params = {"t": "LUZfZGpmOVp0MglUDxN2A0AXGxcsKE4DFT87UidWTG4AKAk2JVF9Cg=="}
    data = {
        "uid": 143,
        "amount": 1,
        "reason": "test"
    }
    res = requests.post(url=url,params=params,data=data)
    print(res.json())
