# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2023/2/27
# @Email:775375798@qq.com
# @File: assert_util.py
import json
import jsonpath
import logging


logger = logging.getLogger(__name__)


def result_validate(yq_result, real_result):
    """
    :param yq_result: 预期结果
    :param real_result: 实际结果
    :param status_code: 状态码
    :return: 返回断言成功与否的标记
    """
    logger.info("预期结果：%s" % yq_result)
    logger.info("实际结果：%s" % real_result.text)
    for key, value in yq_result.items():
        if key == "status_code":
            status_code_assert(value, real_result.status_code)
        elif key == "equals":
            equals_assert(real_result.json(), value)
        elif key == "contains":
            contans_assert(real_result, value)
        elif key == "database":
            pass
        else:
            raise_assert_error("不支持的断言方式！")


def status_code_assert(yq_code, sj_code):
    if yq_code != sj_code:
        raise_assert_error("status_code断言错误！预期结果："+str(yq_code)+",实际结果: "+str(sj_code))


def equals_assert(real_result, value):
    for assert_key, assert_value in value.items():
        data = jsonpath.jsonpath(real_result, '$..%s' % assert_key)[0]
        if not data or data != assert_value:
            raise_assert_error(f"equal断言失败！{assert_key}字段值不为{assert_value}!".format(assert_key, assert_value))


def contans_assert(real_result, value):
    if value not in json.dumps(real_result.text):
        raise_assert_error("contains断言失败！%s不存在"%value)


def raise_assert_error(msg):
    logger.info(msg)
    logger.info("---------------测试用例结束---------------\n")
    raise AssertionError(msg)


# 数据库断言
def database_assert():
    pass