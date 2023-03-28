# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/5/18
# @Email:775375798@qq.com
# @File: conftest.py

from common.common_util import read_config_yaml
import requests
import pytest
import json
import common.common_util as commonutil
import yaml
import os
from common.common_util import write_extract_yaml
from configparser import ConfigParser
import datetime
import random


#ConfigParser自带的optionxfrom()方法中含有lower()函数将字符串强制输出为小写
#所以声明一个自己的解析类，继承原有ConfigParser并重写optionxfrom()方法
class MyParser(ConfigParser):
    def optionxform(self,optionstr):
        return optionstr

conf = MyParser()

# 进行清空extract文件操作
@pytest.fixture(scope="session", autouse=True)
def clean_extract():
    commonutil.clear_extract_yaml()

#登录前置，获取登录信息
@pytest.fixture(scope="session", autouse=True)
def program_login():
    session = requests.session()
    base_data = read_config_yaml('base')
    user_data = {
        "userName": base_data["userName"],
        "password": base_data["password"]
    }
    code = {"code": base_data["code"]}
    # 输入用户名和密码
    session.request(method='post', url='http://admin-test.idouzi.com/amount/login', data=user_data)
    # 输入默认验证码
    res2 = session.request(method='post', url='http://admin-test.idouzi.com/amount/verify-code', data=code)
    # 将提取到的token写入extract文件
    t = json.loads(res2.content)["return_msg"]
    print("t====", t)
    commonutil.write_extract_yaml({"t": t})
    # 将获取到的t值写入配置文件
    write_ini("aiduifen", "t", t)

@pytest.fixture(scope="session", autouse=True)
def tongdui8_login():
    session = requests.session()
    base_url = read_config_yaml("tongdui8_base", "base_url")
    url = base_url+"/supplier/account/login-with-account?s_ver=1"
    user_data = {
        "mobile": read_config_yaml("tongdui8_base", "mobile"),
        "password": read_config_yaml("tongdui8_base", "password")
    }
    res = session.request(method='post', url=url, data=user_data).json()
    # 将获取到的ticket和appid写入临时文件
    ticket = res["return_msg"]["ticket"]
    appId = res["return_msg"]["lastVisitAppId"]["appId"]
    # 将获取到的ticket值写入配置文件
    write_ini("tongdui8", "t", ticket)
    write_ini("tongdui8", "appId", appId)
    write_extract_yaml({"ticket": ticket, "appId": int(appId)})

@pytest.fixture(scope="session", autouse=True)
def set_username():
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute= datetime.datetime.now().minute
    second = datetime.datetime.now().second
    list_date = [day, hour, minute, second]
    date = ''.join(str(i) for i in list_date)
    name =random_name()
    write_extract_yaml({"name": name})

def write_ini(sections, options, value):
    config = MyParser()
    config.read("./pytest.ini", encoding="utf‐8")
    config.set(section=sections, option=options, value=value)
    with open("./pytest.ini", "w+") as file:
        config.write(file)

def random_name():
    # 删减部分，比较大众化姓氏
    firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平" \
                "黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉" \
                "龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓公晋楚闫"
    # 百家姓中双姓氏
    firstName2 = "万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫"
    # 女孩名字
    girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
    # 男孩名字
    boy = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
    # 名
    name = '中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝'
    # 10%的机遇生成双数姓氏
    if random.choice(range(100)) > 10:
        num = random.choice(range(len(firstName)))
        firstName_name = firstName[num]
    else:
        i = random.choice([i for i in range(len(firstName2)) if i % 2 == 0])
        firstName_name = firstName2[i:i + 2]

    sex = random.choice(range(2))
    name_1 = ""
    # 生成并返回一个名字
    if sex > 0:
        girl_name = girl[random.choice(range(len(girl)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + girl_name
    else:
        boy_name = boy[random.choice(range(len(boy)))]
        if random.choice(range(2)) > 0:
            name_1 = name[random.choice(range(len(name)))]
        return firstName_name + name_1 + boy_name

if __name__ == '__main__':
    filename = os.path.join(commonutil.get_rootpath(), 'config.yaml')
    with open(file=filename, mode='w', encoding='utf-8') as f:
        yaml.dump(data={"test": "cy"}, stream=f)




