# -*- coding: utf-8 -*-
'''
#----------------------------------------------------------------------------------------
# 功能：python工具库
#----------------------------------------------------------------------------------------
'''
import contextlib
import os
import platform
import select
import shlex
import socket
import subprocess
import multiprocessing
import sys
import threading
import time
from functools import wraps

import flib
from flib import chardet
from flib.tools.console_util import print_with_color

def singleton(cls):
    """
    单例
    使用装饰器(decorator),
    这是一种更pythonic,更elegant的方法,
    单例类本身根本不知道自己是单例的,因为他本身(自己的代码)并不是单例的
    """
    instances = {}
    @wraps(cls)
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

def SetReadOnly(filename, readonly = False):
    """
    设置是否只读属性
    """
    if not os.path.isfile(filename):
        os.system('attrib -r ' + filename + '//*.* /s')
        return
    import stat
    os.chmod(filename, stat.S_IWRITE) if not readonly else os.chmod(filename, ~stat.S_IWRITE)

class dict_to_object(dict):
    """docstring for dict_to_object"""
    def __getattr__(self, key):
        try:
            return self[key]
        except :
            return ''
        pass

    def __setattr__(self, key, value):
        self[key] = value
        pass

def getEncoding(s):
    try:
        enc = chardet.detect(s)
        return enc
    except:
        return

def toUnicode(s):
    if not s:
        return
    if flib.PY2 and isinstance(s, unicode):
        return s
    elif flib.PY3 and isinstance(s, str):
        return s
    try:
        enc = chardet.detect(s)['encoding']
        #print enc
        if enc == 'ISO-8859-2' or enc == "TIS-620":
            enc = 'gbk'
            if flib.PY2:
                return unicode(s, enc, 'ignore')
            elif flib.PY3:
                return s.decode('utf-8', 'ignore')
    except Exception as e:
        flib.printf(str(e))
        return
    ###
    charsets = ('gbk', 'gb18030', 'gb2312', 'iso-8859-1', 'utf-16', 'utf-8', 'utf-32', 'ascii')
    for charset in charsets:
        try:
            #print charset
            if flib.PY2:
                return unicode(s, charset)
            elif flib.PY3:
                return s.decode('utf-8')
        except:
            continue

def toUTF8(s):
    try:
        if flib.PY2:
            if not isinstance(s, unicode) and not isinstance(s, str) and not isinstance(s, bytes):
                return
        elif flib.PY3:
            if not isinstance(s, str) and not isinstance(s, bytes):
                return
        if flib.PY2 and isinstance(s, unicode):
            return s.encode('utf-8')
        elif flib.PY3 and isinstance(s, str):
            return s.encode('utf-8')
        enc = chardet.detect(s)['encoding']
        if enc == 'utf-8':
            return s
        else:
            s = toUnicode(s)
            if s:
                return s.encode('utf-8')
    except Exception as e:
        flib.printf(str(e))
        return

def toGB2312(s):
    try:
        enc = getEncoding(s)
        if enc and enc['encoding'] == "utf-8":
            s = s.decode('utf-8')
    except Exception as e:
        pass
    s = toUnicode(s)
    if s:
        return s.encode('gb2312')

def toGBK(s):
    try:
        enc = getEncoding(s)
        if enc and enc['encoding'] == "utf-8":
            s = s.decode('utf-8')
    except Exception as e:
        pass
    s = toUnicode(s)
    if s:
        return s.encode('gbk')

def toStr(s):
    if not s: return ""
    try:
        if flib.PY2:
            if not isinstance(s, unicode) and not isinstance(s, str) and not isinstance(s, bytes):
                return str(s)
        elif flib.PY3:
            if not isinstance(s, str) and not isinstance(s, bytes):
                return str(s)
            if isinstance(s, str):
                return s
            elif isinstance(s, bytes):
                return s.decode('utf-8')
        if sys.stdout.encoding == "cp936":
            return toGBK(s)
        return toUTF8(s)
    except Exception as e:
        flib.printf( str(e) )
        return s

# 环境变量
def getenv(key, default=None):
    return os.environ[key] if key in os.environ else default
def setenv(key, v):
    os.environ[key] = v

# 全局唯一uuid
def newuuid():
    import uuid
    return uuid.uuid1()

# 日志输出
def __print__(s, newLine = True, color = None):
    print_with_color(s, newLine=newLine, color=color)

def __log__(tag, color, *args):
    if tag: __print__(toStr(tag), newLine=False, color=color)
    __index__ = 0
    for s in args:
        __index__ = __index__ + 1
        tmp = toStr(s)
        __print__(tmp if tmp else str(s), newLine=False, color=color)
        __print__(" " if __index__ != len(args) else "", newLine=False, color=color)
    __print__("", newLine=True, color=color)
    sys.stdout.flush()

class Log(object):
    """log util"""
    _lock = threading.Lock()
    _lock2 = multiprocessing.Lock()
    @classmethod
    def logWithColor(cls, color, *args):
        cls._lock2.acquire()
        cls._lock.acquire()
        __log__("", color, *args)
        cls._lock.release()
        cls._lock2.release()
    @staticmethod
    def log(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("", None, *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def i(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("[info]", None, *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def d(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("[debug]", "blue", *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def w(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("[warning]", "yellow", *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def e(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("[error]", "red", *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def s(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        __log__("[session]", "green", *args)
        Log._lock.release()
        Log._lock2.release()
    @staticmethod
    def expt(*args):
        Log._lock2.acquire()
        Log._lock.acquire()
        err_msg = " ".join([toStr(x) for x in args])
        Log._lock.release()
        Log._lock2.release()
        raise Exception(err_msg)

def ZLPrint(*args):
    __log__("", None, *args)

#quit
def quit(func):
    def quit_call(*arg, **kw):
        result = func(*arg, **kw)
        if not result:
            exit(-1)
        return result
    return quit_call

def execute(cmds="", logout=True, finalcallback=None, try_exec = False, communicate=None, **kwargs):
    def unbuffered(proc, stream='stdout'):
        newlines = ['\n', '\r\n', '\r']
        stream = getattr(proc, stream)
        with contextlib.closing(stream):
            while True:
                out = []
                last = stream.read(1)
                # Don't loop forever
                if not last or last == '' and proc.poll() is not None:
                    break
                while last not in newlines:
                    # Don't loop forever
                    if last == '' and proc.poll() is not None:
                        break
                    out.append(last)
                    last = stream.read(1)
                out = ''.join(out)
                yield out
    try:
        if logout: Log.log("---->  " + cmds)
        sysstr = platform.system()
        # 变参调整
        args_tpl = {
            "bufsize" : True,
            "executable": True,
            "stdin": True,
            "stdout": True,
            "stderr": True,
            "preexec_fn": True,
            "close_fds": True,
            "shell": True,
            "cwd": True,
            "env": True,
            "universal_newlines": True,
            "startupinfo": True,
            "creationflags": True,
            "restore_signals": flib.PY3,
            "start_new_session": flib.PY3,
            "pass_fds": flib.PY3,
            "errors": flib.PY3,
            "encoding": flib.PY3
        }
        p_args = {}
        for v in kwargs:
            if v not in args_tpl or not args_tpl[v]:
                continue
            p_args[v] = kwargs[v]
        if args_tpl['encoding'] and 'encoding' not in p_args:
            p_args['encoding'] = flib.env_encoding
        p_args['stdout'] = subprocess.PIPE if 'stdout' not in p_args else p_args['stdout']
        p_args['stderr'] = subprocess.PIPE if 'stderr' not in p_args else p_args['stderr']
        p_args['shell'] = True if 'shell' not in p_args else p_args['shell']
        p = subprocess.Popen(shlex.split(cmds) if sysstr == "Windows" else cmds, **p_args)
        result = []
        if communicate: communicate(p.stdin)
        if sysstr == "Windows":
            if flib.PY2:
                if p_args['stdout']:
                    for line in unbuffered(p):
                        if line:
                            result.append(line)
                            if logout: Log.log (line.strip('\r\n'))
                if p_args['stderr']:
                    for line in unbuffered(p, "stderr"):
                        if line and not try_exec: Log.e(line)
            elif flib.PY3:
                while p_args['stdout']:
                    line = p.stdout.readline()
                    if not line or line == '': break
                    result.append(line.rstrip())
                    if logout: Log.log(line.rstrip('\r\n').rstrip('\n'))
                while not try_exec and p_args['stderr']:
                    line = p.stderr.readline()
                    if not line or line == '': break
                    Log.e(line.rstrip('\r\n').rstrip('\n'))
            else:
                raise Exception("Unknow python version")
        else:
            rlist = [p.stdout,p.stderr]
            while rlist:
                readable, _, _ = select.select(rlist, [], [])
                for r in readable:
                    if r is p.stdout:
                        line = r.readline()
                        if not line:
                            rlist.remove(r)
                            continue
                        line = line.rstrip('\n').rstrip('\r\n')
                        if not line: continue
                        result.append(line)
                        if logout: Log.log (line)
                    elif r is p.stderr:
                        line = r.readline()
                        if not line:
                            rlist.remove(r)
                            continue
                        line = line.rstrip('\n').rstrip('\r\n')
                        if not line: continue
                        if not try_exec: Log.e (line)
        p.wait()

        returncode = p.returncode

        if p.stdin:
            p.stdin.close()
        if p.stdout:
            p.stdout.close()
        if p.stderr:
            p.stderr.close()
        try:
            p.kill()
        except OSError:
            pass

        if returncode != 0:
            if not try_exec: Log.e ("Failed to execute command '" + cmds + "'")
            return False
        else:
            if len(result) == 0: return True
            return result
    except Exception as e:
        if not try_exec: Log.e (str(e))
        if not try_exec: Log.e ("Failed to execute command '" + cmds + "'")
        return False
    finally:
        if finalcallback: finalcallback()

def exec_sh(cmds="", logout=False, args=list()):
    name = os.path.join(os.getcwd(), str(newuuid()) + ".sh").replace("\\", "/")
    with flib.open(name, "w+") as f:
        f.write(cmds)
        f.close()
        param = " " + " ".join([str(x) for x in args]) if args else ""
        return execute(cmds="sh " + name + param, finalcallback=lambda:os.remove(name), logout=logout)

@quit
def safe_execute(cmds="", logout=True, finalcallback = None):
    return execute(cmds=cmds, logout=logout, finalcallback=finalcallback)

def exec_command(*args, **kwargs):
    param = " ".join([str(x) for x in args])
    return execute(cmds=param.format(**kwargs), logout=True, finalcallback=None)

def check_output(*args, **kwargs):
    param = " ".join([str(x) for x in args])
    return execute(cmds=param.format(**kwargs), logout=False, finalcallback=None)

def simple_exec(*args, **kwargs):
    try:
        param = " ".join([str(x) for x in args])
        p = subprocess.Popen(shlex.split(param.format(**kwargs)), shell=True)
        p.wait()
        if p.returncode != 0:
            Log.e ("Failed to execute command '" + param.format(**kwargs) + "'")
            return False
        else:
            return True
    except Exception as e:
        Log.e (e)
        return False

# netcat 服务器
class nc_server(threading.Thread):
    """netcat for nc_server"""
    class nc_client(threading.Thread):
        def __init__(self, client_socket, server):
            super(nc_server.nc_client, self).__init__()
            self.socket = client_socket
            self.server = server
            self.lock = threading.Lock()
            self.stopped = False
        def __del__(self):
            self.stop()
        def stop(self):
            try:
                self.lock.acquire()
                self.stopped = True
                self.lock.release()
                self.socket.close()
            except:
                pass
        def run(self):
            while True:
                try:
                    self.lock.acquire()
                    if self.stopped:
                        break
                    data = self.socket.recv(1024)
                    recv_len = len(data)
                    if recv_len == 0:
                        __print__("")
                        break
                    tmp = toStr(data) or data
                    color = None
                    if tmp and tmp.startswith("[error]"):
                        color = "red"
                    # elif tmp and tmp.startswith("[warning]"):
                    #     color = "yellow"
                    __print__(tmp.strip('\r\n').strip('\n'), newLine=True if recv_len < 1024 else False, color=color)
                except:
                    time.sleep(0.01)
                    pass
                finally:
                    self.lock.release()
            Log.i("client_handler finished")

    def __init__(self, host="0.0.0.0", port=0):
        super(nc_server, self).__init__()
        self.stopped = False
        self.clients = []
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(0)
        self.server.setblocking(0)
        self.lock = threading.Lock()
        Log.i("start nc server [{0}:{1}]!".format(host, self.get_port()))

    def get_port(self):
        a = self.server.getsockname()
        self.port = a[1]
        return self.port

    def get_ip(self):
        a = self.server.getsockname()
        self.host = a[0]
        return self.host

    def stop(self):
        self.lock.acquire()
        self.stopped = True
        self.lock.release()
        Log.i("stop netcat.")

    def isStoped(self):
        self.lock.acquire()
        try:
            return self.stopped
        finally:
            self.lock.release()

    def run(self):
        while True:
            try:
                self.lock.acquire()
                if self.stopped:
                    break
                client_socket, addr = self.server.accept()
                client_socket.setblocking(0)
                Log.i("accept client:{0}".format(addr))
                client_thread = nc_server.nc_client(client_socket, self) #threading.Thread(target=nc_server.client_handler, args=(client_socket, self))
                client_thread.start()
                self.clients.append(client_thread)
            except Exception as e:
                time.sleep(0.01)
                pass
            finally:
                self.lock.release()

        self.server.close()
        for subthread in self.clients:
            subthread.stop()

@singleton
class dir_op:
    """
    目录操作,更改目录操作，
    离开当前作用域后，自动还原到以前路径
    """
    old_dir = os.getcwd()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.old_dir is not None:
            Log.log("Leave Directory:", os.getcwd())
            os.chdir(self.old_dir)
            self.old_dir = os.getcwd()
    @classmethod
    def Enter(cls, _dir):
        old_dir = os.getcwd()
        os.chdir(_dir)
        Log.log("Enter Directory:", _dir)
        return cls()
    @property
    def curdir(self):
        return os.getcwd()

class guard_op:
    """
    安全锁操作
    """
    def __init__(self, lock):
        self._lock = lock
    def __enter__(self):
        self.Lock()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.UnLock()
    def Lock(self):
        if not self._lock:
            return
        if hasattr(self._lock, "acquire"):
            self._lock.acquire()
        elif hasattr(self._lock, "lock"):
            self._lock.lock()
        elif hasattr(self._lock, "tryLock"):
            self._lock.tryLock()
    def UnLock(self):
        if not self._lock:
            return
        if hasattr(self._lock, "release"):
            self._lock.release()
        elif hasattr(self._lock, "unlock"):
            self._lock.unlock()
        elif hasattr(self._lock, "tryUnLock"):
            self._lock.tryUnLock()

def getJavaProperty(key):
    if key.startswith('-D'): key = key[2:]
    jar = os.path.join(flib.__plugin_path__, "getProperty.jar")
    outputs = check_output('''java -jar "{bin}" {key}''', bin=jar, key=key)
    if outputs:
        value = outputs[0]
        return value.rstrip('\r\n')

__jenkins_encoding = None

def toJenkinsEncoding(s):
    if not s: return ""
    try:
        if flib.PY2:
            if not isinstance(s, unicode) and not isinstance(s, str) and not isinstance(s, bytes):
                return str(s)
        elif flib.PY3:
            if not isinstance(s, str) and not isinstance(s, bytes):
                return str(s)
        global __jenkins_encoding
        if not __jenkins_encoding:
            __jenkins_encoding = getJavaProperty("file.encoding")
        if __jenkins_encoding.lower() == 'gbk':
            return toGBK(s)
        elif __jenkins_encoding.lower() == 'gb2312':
            return toGB2312(s)
        else:
            return toUTF8(s)
    except Exception as e:
        flib.printf( str(e) )
        return s

#测试
def main():
    from locale import getpreferredencoding
    flib.printf( sys.stdout.encoding, getpreferredencoding() )
    Log.log("b", "a")
    #Log.expt("Tesxt你好")
    flib.printf(toUTF8('Hello你好'))
    # p = subprocess.Popen(shlex.split("svn log -l 10"), shell=True, stdout=subprocess.PIPE)
    # print(p.stdout.read())
    # p.wait()
    exec_sh("svn info $1", args=["F:/Seven/ElementUnityWin"], logout=True)
    exec_command('''svn info "{path}"''', path="F:/Seven/ElementUnityWin")
    safe_execute('''svn info "F:/Seven/ElementUnity"''', logout=True)
    # print platform.system()
    # Log.log("b", "a")
    # __log__('',"为什么")
    # print toStr("为什么")
    #nc_server().start()
    print (getJavaProperty("-Dfile.encoding"))
    #print toStr("你好"), toJenkinsEncoding('你好')

if __name__ == '__main__':
    main()
