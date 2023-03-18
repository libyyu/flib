# -*- coding: utf-8 -*-
'''
生成Jenkins菜单
'''
import argparse
import sys, os

table_template = """
    <table width="100%" class="parameters">
        <tbody>
        {rows}
        </tbody>
    </table>
"""
__channel_gens = {}
__channel_names = {}
__channel_name2s = {}
__channel_common_options = []

def make_input(param, desc, default="", input_type="text", class_style="setting-input"):
    return """
            <tr>
                <td class="setting-leftspace">&nbsp;</td>
                <td class="setting-name">{param}</td>
                <td class="setting-main">
                    <input name="value" type="{input_type}" class="{class_style}" value="{default}">
                </td>
            </tr>
            <tr>
                <td colspan="2"></td>
                <td class="setting-description">{desc}</td>
            </tr>
    """.format(**locals())

def make_select(param, options, desc):
    options_ = ""
    for option in options:
        options_ += """<option value="{param}" {selected}>{name}</option>""".format(param=option["key"], name=option["value"], selected=option["selected"])


    return """
            <tr>
                <td class="setting-leftspace">&nbsp;</td>
                <td class="setting-name">{param}</td>
                <td class="setting-main">
                    <select name="value">
                        {options}
                    </select>
                </td>
            </tr>
            <tr>
                <td colspan="2"></td>
                <td class="setting-description">{desc}</td>
            </tr>
    """.format(param=param, options=options_, desc=desc)

class Option:
    """
    渠道参数选项
    """
    def __init__(self, optionname, desc, input_type = "text", class_style = "setting-input", default=""):
        self.option = optionname
        self.desc = desc
        self.input_type = input_type
        self.class_style = class_style
        self.default_value = default

    def __str__(self):
        return make_input(self.option, self.desc, input_type=self.input_type, class_style=self.class_style,
                          default=self.default_value)

class InputOption(Option):
    """
    输入选项
    """
    def __init__(self, optionname, desc, input_type = "text", class_style = "setting-input", default=""):
        Option.__init__(self,optionname, desc, input_type, class_style, default)

    def __str__(self):
        return make_input(self.option, self.desc, input_type=self.input_type, class_style=self.class_style,
                          default=self.default_value)

class SelectOption(Option):
    """
    下拉选择
    """
    def __init__(self, optionname, desc, input_type = "text", class_style = "setting-input", default="", selects = []):
        Option.__init__(self,optionname, desc, input_type, class_style, default)
        self.selects = selects

    def __str__(self):
        select_options = []
        for select in self.selects:
            option_item = {}
            option_item["key"] = select#key
            option_item["value"] = select#value
            if self.default_value == select:
                option_item["selected"] = """selected = "selected" """
            else:
                option_item["selected"] = ""
            select_options.append(option_item)

        return make_select(self.option, select_options, self.desc)

def zulong_option():
    """
    生成祖龙渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appid"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("wx_payId", "wx_payId"))
    options.append(InputOption("isDebug", "wx_payId", input_type="checkbox", class_style="  "))
    options.append(InputOption("server_oauth_url", "server_oauth_url"))
    options.append(InputOption("server_back_url", "server_back_url"))
    options.append(InputOption("aliyun_httpdns_url", "aliyun_httpdns_url"))
    options.append(InputOption("http_agreement_url", "http_agreement_url"))
    options.append(InputOption("server_host_url", "server_host_url"))
    options.append(InputOption("server_host_back_url", "server_host_back_url"))
    options.append(InputOption("talking_data_appid", "talking_data_appid"))
    options.append(InputOption("talking_data_channelid", "talking_data_channelid"))
    options.append(InputOption("qq_appId", "qq_appId"))
    options.append(InputOption("weibo_appId", "weibo_appId"))
    return options

def uc_option():
    """
    生成uc渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("uc_gameId", "uc_gameId"))
    options.append(InputOption("uc_cpId", "uc_cpId"))
    return options

def a360_option():
    """
    生成360渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("appSecret", "appSecret"))
    options.append(InputOption("appGaodeKey", "appGaodeKey", default="none"))
    options.append(InputOption("appWXAppId", "appWXAppId", default="none"))
    return options

def baidu_option():
    """
    生成baidu渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    return options

def coolpad_option():
    """
    生成coolpad渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("appPayKey", "appPayKey"))
    return options

def huawei_option():
    """
    生成huawei渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("appPayRsaPrivate", "appPayRsaPrivate"))
    options.append(InputOption("appPayRsaPublic", "appPayRsaPublic"))
    options.append(InputOption("appFloatPrivate", "appFloatPrivate"))
    return options

def iqiyi_option():
    """
    生成iqiyi渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    return options

def amigo_option():
    """
    生成金立渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    return options

def lenovo_option():
    """
    生成lenovo渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    return options

def leshi_option():
    """
    生成leshi渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    return options

def mz_option():
    """
    生成魅族渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    return options

def oppo_option():
    """
    生成oppo渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("appSecret", "appSecret"))
    return options

def quick_option():
    """
    生成quick渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    return options

def tt_option():
    """
    生成tt渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    options.append(InputOption("appKey", "appKey"))
    options.append(InputOption("isDebug", "isDebug", input_type="checkbox", class_style="  "))
    return options

def vivo_option():
    """
    生成vivo渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("appId", "appId"))
    return options

def xiaomi_option():
    """
    生成xiaomi渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("mi_appId", "mi_appId"))
    options.append(InputOption("mi_appKey", "mi_appKey"))
    return options

def tencent_option():
    """
    生成应用宝渠道配置参数信息
    :return: list
    """
    options = []
    options.append(InputOption("pkg_name", "渠道包名"))
    options.append(InputOption("qqAppId", "qqAppId"))
    options.append(InputOption("wxAppId", "wxAppId"))
    options.append(InputOption("offerId", "offerId"))
    options.append(InputOption("isDebug", "isDebug", input_type="checkbox", class_style="  "))
    return options

def common_option():
    """
    通用参数配置，所有渠道都用到
    :return:
    """
    options = []
    options.append(InputOption("build_target", "安卓编译版本"))
    selects = ["1.0", "2.0", "3.0_debug"]
    options.append(SelectOption("version", "SDK版本号", default="1.0", selects = selects))
    return options

def insert_common():
    """
    注册通用配置
    :return:
    """
    for option in common_option():
        __channel_common_options.append(option)

def insert_channel(channel, showname, func):
    """
    注册渠道Jenkins选项菜单，
    :param channel: 渠道英文名
    :param showname: 渠道显示名，可以是中文
    :param func: 处理函数
    :return:
    """
    __channel_names[channel] = showname
    __channel_name2s[showname] = channel
    __channel_gens[channel] = func()

def register_channel():
    """
    注册所有渠道生成参数
    :return:
    """
    insert_channel("zulong_release", "祖龙正式", zulong_option)
    insert_channel("zulong_test", "祖龙测试", zulong_option)
    insert_channel("tencent_release", "腾讯正式", tencent_option)
    insert_channel("tencent_testenv", "腾讯测试", tencent_option)
    insert_channel("uc", "uc", uc_option)
    insert_channel("baidu", "百度多酷", baidu_option)
    insert_channel("xiaomi", "小米", xiaomi_option)
    insert_channel("lenovo", "联想", lenovo_option)
    insert_channel("vivo", "vivo", vivo_option)
    insert_channel("oppo", "oppo", oppo_option)
    insert_channel("mz", "魅族", mz_option)
    insert_channel("a360", "360", a360_option)
    insert_channel("huawei", "华为", huawei_option)
    insert_channel("amigo", "金立", amigo_option)
    insert_channel("coolpad", "酷派", coolpad_option)
    insert_channel("leshi", "乐视", leshi_option)
    #insert_channel("ireader", "掌阅", ireader_option)
    insert_channel("iqiyi", "爱奇艺", iqiyi_option)
    insert_channel("quick", "Quick", quick_option)
    insert_channel("tt", "TT语音", tt_option)

    #注册通用参数
    insert_common()
# 预先注册
register_channel()

def gen_channel_param(channel):
    """
    生成渠道对应的命令行参数信息
    :param channel:
    :return:
    """
    if __channel_gens.has_key(channel):
        options = __channel_gens[channel]
    elif __channel_name2s.has_key(channel) and __channel_gens.has_key(__channel_name2s[channel]):
        options = __channel_gens[__channel_name2s[channel]]
    else:
        raise Exception("渠道{}未注册".format(channel))
    ret = []
    for option in options:
        ret.append("-" + option.option)
    return tuple(ret)

def gen_common_param():
    """
    生成通用配置对应的命令行参数信息
    :return:
    """
    ret = []
    for option in __channel_common_options:
        ret.append("-" + option.option)
    return tuple(ret)

def get_channel_info(channel):
    """
    返回渠道英文名，中文名称
    :param channel:
    :return:
    """
    if __channel_names.has_key(channel):
        return (channel, __channel_names[channel])
    elif __channel_name2s.has_key(channel):
        return (__channel_name2s[channel], channel)
    else:
        raise Exception("渠道{}未注册".format(channel))


def gen_jenkins_option(options):
    """
    生成渠道在Jenkins里面的参数配置
    :param channel:渠道名称
    :return:
    """
    rows = ""
    for option in options:
        rows += str(option)
    return rows

def gen_channel_option(channel):
    """
    生成渠道在Jenkins里面的参数配置
    :param channel:渠道名称
    :return:
    """
    if __channel_gens.has_key(channel):
        options = __channel_gens[channel]
    elif __channel_name2s.has_key(channel) and __channel_gens.has_key(__channel_name2s[channel]):
        options = __channel_gens[__channel_name2s[channel]]
    else:
        return None
    return gen_jenkins_option(options)

def gen_common_option():
    """
    生成渠道通用配置
    :return:
    """
    return gen_jenkins_option(__channel_common_options)

#默认参数设置
def get_default_value(channel_name, param_type, key):
    pass

def get_file_list(_dir, recursion = True):
    """
    列举目录下所有的文件
    :param recursion:是否递归文件夹
    :return:
    """
    def __enum__(src, callback):
        for f in os.listdir(src):
            sourceF = os.path.join(src, f)
            if os.path.isdir(sourceF):
                if recursion:
                    __enum__(sourceF, callback)
            else:
                callback(sourceF)
    ret = []
    __enum__(_dir, lambda p: ret.append(p))
    return ret


def get_folder_list(_dir, recursion = True):
    """
    列举目录下所有的目录
    :param recursion:是否递归文件夹
    :return:
    """
    def __enum__(src, callback):
        for f in os.listdir(src):
            sourceF = os.path.join(src, f)
            if os.path.isdir(sourceF):
                callback(sourceF)
                if recursion:
                    __enum__(sourceF, callback)
    ret = []
    __enum__(_dir, lambda p: ret.append(p))
    return ret

def gen_jenkinss_version_option(_path):
    """
    获取所有版本信息
    :param _path:
    :return:
    """
    if _path[:7] == "http://":
        from py_script.FUtil import FUtil
        versions = FUtil.check_output("svn list {svn_url}".format(svn_url=_path), logout=False)
    else:
        versions = get_folder_list(_path, recursion=False)
    result = ""
    for v in versions:
        result += "\n" + v.strip("\n").replace("\n", "")
    return result


def test():
    #print get_file_list("""F:\Seven\uniclient_py_zl\cache\seven\channels""", recursion = True)
    gen_jenkinss_version_option("http://10.236.192.18/svn/seven_client/branches/lidengfeng/uniclient_py/channels")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", help="需要的渠道", required=True, type=str)
    parser.add_argument("--path", help="搜索路径", type=str)
    parser.add_argument("--paramtype", help="生成的参数类型", required=True, type=str)
    args = parser.parse_args()


    if args.paramtype == "channel":
        channel = args.channel
        rows = gen_channel_option(channel)
        if not rows:
            rows = """渠道 <font color="red">{channel}</font> 不支持，未定义渠道。""".format(channel=channel)
        print table_template.format(rows=rows)


    if args.paramtype == "common":
        rows = gen_common_option()
        if not rows:
            rows = "生成通用配置参数失败。"
        print table_template.format(rows=rows)

if __name__ == "__main__":
    main()