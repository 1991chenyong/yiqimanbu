import re
import time
import random
from common.common_util import read_config_yaml


class DebugTalk(object):

    def read_config(self, section, option=None):
        return read_config_yaml(section, option)

    def get_random_number(self):
        return random.randint(20190616000001, 20190616999999)

    def get_token_data(self):
        return [
            {"appid": "wx07df0de943e4669f", "grant_type": "client_credential", "secret": "970cad5163a8954fc4d8423a8a15ced0", "eq_str": "access_token"},
            {"appid": "", "grant_type": "client_credential", "secret": "client_credential", "eq_str": "errcode"},
            {"appid": "2222", "grant_type": "client_credential", "secret": "970cad5163a8954fc4d8423a8a15ced0", "eq_str": "errcode"}
        ]

    # 获取时间
    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def get_addone_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+1))

    def get_addtwo_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+2))

    def get_addthree_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+3))

    def get_reduceone_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-1))

    def get_reducetwo_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-2))

    def get_reducethree_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-3))

    def get_reducefour_second(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-4))

    def get_add_month(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+2592000))


if __name__ == "__main__":
    test = "endTime: ${get_add_month()}"
    regx = re.compile(r'\$\{(.+?)\((.*?)\)}')
    fun_list = regx.findall(test)
    print("fun_list=", fun_list)
    print(DebugTalk().get_current_time())
    print(DebugTalk().get_add_month())

