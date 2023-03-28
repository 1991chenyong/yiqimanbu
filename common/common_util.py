import csv
import yaml
import os


#获取到项目路径
def get_path():
    return os.path.realpath(__file__).split('common')[0]

# 读取配置文件的yaml
def read_config_yaml(one_node=None, two_node=None):
    file_name = str(get_path()) + 'config.yaml'
    with open(file_name, encoding='utf8') as f:
        value = yaml.full_load(f.read())
    if one_node:
        if two_node:
            return value[one_node][two_node]
        else:
            return value[one_node]
    return value

# 读取配置文件的base基础字段的key值
def read_config_keys_yaml(one_node):
    file_name = str(get_path()) + 'config.yaml'
    with open(file_name, encoding='utf8') as f:
        value = yaml.full_load(f.read())
    base_value = value[one_node]
    if isinstance(base_value, dict):
        key_list = []
        for key, value in base_value.items():
            key_list.append(key)
        return key_list

# 读取extract文件的yaml
def read_extract_yaml(node):
    file_name = str(get_path()) + 'extract.yaml'
    with open(file_name, encoding='utf8') as f:
        value = yaml.full_load(f.read())
    return value[node]

# 数据写入extract文件yaml
def write_extract_yaml(data_dict):
    file_name = str(get_path()) + 'extract.yaml'
    with open(file_name, 'a', encoding='utf8') as f:
        yaml.dump(data_dict, stream=f)
    # print('"%s"字段成功写入 extract yaml文件！' % list(data_dict.keys())[0])

#清空extract文件的yaml
def clear_extract_yaml():
    file_name = str(get_path()) + 'extract.yaml'
    with open(file_name, 'w', encoding='utf8') as f:
       f.truncate()

#读取csv文件
def read_csv_data(csv_path):
    csv_path = str(get_path()) + csv_path
    with open(csv_path, encoding='utf8') as f:
        csv_data = list(csv.reader(f))
    return csv_data


if __name__ == '__main__':
    print(read_config_yaml('login'))
    write_extract_yaml({"t": "dsfsfsfsdf"})
