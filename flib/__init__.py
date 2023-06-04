# -*- coding: utf-8 -*-

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass
import os,sys
from sys import version_info
import locale
__author__ = 'lidengfeng'
__date__ = '2016/10/28'
__version__ = '1.0'
__comment__ = '对之前的工具库目录结构调整'
__libpath__ = os.path.join(os.path.split(os.path.realpath(__file__))[0], "..") #__path__不能用
__is_jenkins__ = "WINSW_EXECUTABLE" in os.environ or 'JENKINS_HOME' in os.environ
__plugins_path__ = os.path.join(__libpath__, "plugins")

#解决python版本兼容问题
if version_info < (3, 0):
    PY3 = False
elif version_info >= (3, 0):
    PY3 = True

env_encoding = locale.getpreferredencoding()

def import_driver(drivers, preferred=None):
    """Import the first available driver or preferred driver.
    """
    if preferred:
        drivers = [preferred]

    for d in drivers:
        try:
            return __import__(d, None, None, ['x'])
        except ImportError:
            pass
    raise ImportError("Unable to import " + " or ".join(drivers))

def import_path(paths):
    """import absolute path
    """
    for dirpath in paths:
        if os.path.isfile(dirpath):
            (dirpath, filename) = os.path.split(dirpath)
        if dirpath not in sys.path: sys.path.append(dirpath)

def import_file(file):
    """Import file with absolute path
    """
    (dirpath, filename) = os.path.split(file)
    (fname, fext) = os.path.splitext(filename)
    if dirpath not in sys.path: sys.path.append(dirpath)
    return import_driver([fname])

def open(name, mode='r', encoding='utf-8'):
    if not PY3:
        import __builtin__
        return __builtin__.open(name, mode=mode)
    else:
        import builtins
        return builtins.open(name, mode=mode, encoding=encoding)

# 日志输出
# def printf(*args, **kwargs):
#     from .tools.console_util import print_with_color
#     param = " ".join([str(x) for x in args])
#     print_with_color(param.format(**kwargs), newLine=True, color=None)

# def has_key(d, k):
#     if version_info < (3,0):
#         return d.has_key(k)
#     else:
#         return k in d
#printf("python:{python}, env_encoding:{env_encoding}", env_encoding=env_encoding, python='python3' if PY3 else 'python2')
