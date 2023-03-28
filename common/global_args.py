# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2023/3/21
# @Email:775375798@qq.com
# @File: global_args.py
from pathlib import Path
from iniconfig import IniConfig
from configparser import ConfigParser


def load_tongdui8_ini():
    # 判断pytest.ini文件是否存在
    path = Path("./pytest.ini")
    new_dict = {}
    if not path.exists():
        return {}
    ini = IniConfig("./pytest.ini")
    if "tongdui8" not in ini:
        return {}
    for key,value in ini["tongdui8"].items():
        if key =='s_ver' or key == 'appid':
            value = int(value)
            new_dict[key] = value
        new_dict[key] = value
    return new_dict

def load_aiduifen_ini():
    # 判断pytest.ini文件是否存在
    path = Path("./pytest.ini")
    if not path.exists():
        return {}
    ini = IniConfig("./pytest.ini")
    if "aiduifen" not in ini:
        return {}
    return dict(ini["aiduifen"].items())

def load_ini(project):
    # 判断pytest.ini文件是否存在
    path = Path("./pytest.ini")
    if not path.exists():
        return {}
    ini = IniConfig("./pytest.ini")
    if project not in ini:
        return {}
    if project == "aiduifen":
        return dict(ini[project].items())
    else:
        new_dict = {}
        for key, value in ini["tongdui8"].items():
            if key == 's_ver' or key == 'appid':
                value = int(value)
                new_dict[key] = value
            new_dict[key] = value
        return new_dict


if __name__ == "__main__":
    print(load_ini("aiduifen"))
