import traceback
import common.common_util as common_util
import yaml
from common.logger_util import write_log,write_error_log
import jsonpath


# 读取测试用例文件的yaml
def read_testcase_yaml(yaml_path):
    try:
        # yaml_path = str(common_util.get_path()) + yaml_path
        with open(yaml_path, encoding='utf8') as f:
            testcase_data = yaml.full_load(f.read())
            if testcase_data and isinstance(testcase_data, list):
                for testcase in testcase_data:
                    if jsonpath.jsonpath(dict(testcase), '$..parameters'):
                        testcase_list = analysis_csv(testcase)
                        return testcase_list
                    else:
                        return testcase_data
            elif testcase_data and isinstance(testcase_data, dict):
                if jsonpath.jsonpath(dict(testcase_data), '$..parameters'):
                    testcase_list = analysis_csv(testcase_data)
                    return testcase_list
                else:
                    return testcase_data
            else:
                write_error_log("从测试用例yaml文件中没有读取到数据")
    except Exception as e:
        write_error_log("读取测试用例文件失败！")

# 封装分析csv文件的方法
def analysis_csv(testcase_info):
    try:
        testcase_info_list = []
        for key, value in dict(testcase_info['parameters']).items():
            # 读取csv文件
            csv_data = common_util.read_csv_data(value)
            text_testcase_info = yaml.dump(testcase_info)
            # 所有行长度标记
            length_flag = True
            key_list = str(key).split('-')
            # 判断所有行列数是否一致
            for row in csv_data:
                if len(csv_data[0]) != len(row):
                    length_flag = False
                    write_log("csv文件长度不一致！无法正确读取数据")
                    break
            if length_flag:
                for x in range(1, len(csv_data)):
                    temp_testcase_info = text_testcase_info
                    for y in range(0, len(csv_data[x])):
                        old_value = '$csv{%s}' % csv_data[0][y]
                        if csv_data[0][y] in key_list:
                            temp_testcase_info = temp_testcase_info.replace(old_value, csv_data[x][y])
                    testcase_info_list.append(yaml.safe_load(temp_testcase_info))
        return testcase_info_list
    except:
        write_error_log("分析parameters参数化出错，异常信息： %s" % str(traceback.format_exc()))


if __name__ == "__main__":
    print(read_testcase_yaml('testcase/lms_package.yml'))