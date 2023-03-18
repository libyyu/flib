# -*- coding: utf-8 -*-
#先前操作太多重复代码，现在进行封装
#SVN操作工具类
import re
from flib.utils import *

SVNSEP="------------------------------------------------------------------------"

class SvnRecord:
    '''svn一条记录信息'''
    def __init__(self, version, author, date, log):
        self.version = version
        self.author = author
        self.date = date
        self.log = log
    def __str__(self):
        return "{version}:{log}@{author}@{date}".format(version=self.version,author=self.author,date=self.date,log=self.log)
    def filter(self, filters):
        if self.log in filters:
            return True
        elif "{log}@{author}".format(log=self.log,author=self.author) in filters:
            return True
        else:
            return False
    @classmethod
    def createSvnRecordFromString(cls,content):
        record = SvnRecord(1, "", "", "")
        pos = content.find(':')
        if pos == -1:
            version = int(content)
            record.version = version
            return record
        version = int(content[:pos])
        record.version = version
        s = content[pos + 1:].split('@')
        if s:
            if len(s) >= 1: record.log = s[0]
            if len(s) >= 2: record.author = s[1]
            if len(s) >= 3: record.date = s[2]
        return record
    @classmethod
    def parseSVNRecord(cls,logs):
        info = logs[0].split(' | ')
        message = ""
        for x in range(1, len(logs)):
            message += '\n' + logs[x]
        return SvnRecord(int(info[0][1:]), toStr(info[1]), toStr(info[2]), toStr(message))


class SVN:
    """提供一些svn操作"""
    username = ""
    password = ""

    @classmethod
    def get_svn_host(cls, local_dir):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        result =  check_output('''svn info "{local_dir}" {identify}'''.format(local_dir=local_dir,identify=identify))
        if not result:return
        return result[2][5:]

    @classmethod
    def get_merge_records(cls,url):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        return try_check_output("svn propget svn:mergeinfo {url} {identify}".format(url=url,identify=identify))

    @classmethod
    def get_start_version(cls,url):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        logs = check_output("svn log {url} --stop-on-copy {identify}".format(url=url,identify=identify))
        last = None
        for x in range(len(logs[1:]) - 1, -1, -1):
            if logs[x] == SVNSEP and last:
                info = last.split(' | ')
                return int(info[0][1:])
            else:
                last = logs[x]

    @classmethod
    def get_records(cls,url,maxlimit=1000):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        slog = check_output("svn log -l {maxlimit} {url} {identify}".format(url=url, maxlimit=maxlimit,identify=identify))
        if not slog: return
        result = []
        record_begin = None
        record_end = None
        num = len(slog)
        x = 0
        while True:
            if x >= num: break
            line = slog[x]
            if line == SVNSEP and record_begin == None:
                record_begin = x
            elif record_begin != None and line == SVNSEP and record_end == None:
                if x < num - 1 and slog[x + 1] != SVNSEP or x == num - 1:
                    record_end = x
                elif x < num:
                    n = x + 1
                    while n < num - 1 and slog[n] != SVNSEP:
                        record_end = n - 1
                else:
                    record_end = x
            if record_begin != None and record_end != None:
                infolist = slog[record_begin + 1:record_end]
                record = SvnRecord.parseSVNRecord(infolist)
                result.append(record)
                x = record_end
                record_begin = None
                record_end = None
            else:
                x = x + 1

        return result

    @classmethod
    def get_version_log(cls,url,version):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        slog = check_output("svn log -r {version} {url} {identify}".format(url=url, version=version,identify=identify))
        info = slog[1].split(' | ')
        logmessage = ""
        for x in slog[2:]:
            if x == SVNSEP:
                break
            logmessage += '\n' + x
        return SvnRecord(int(info[0][1:]), toUTF8(info[1]), toUTF8(info[2]), toUTF8(logmessage))

    @classmethod
    def get_latest_version(cls, url):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        slog = check_output("svn log -l 1 {url} {identify}".format(url=url, identify=identify))
        info = slog[1].split(' | ')
        return int(info[0][1:])

    @classmethod
    def get_merge_record_from_branch(cls,url, branch):
        records = SVN.get_merge_records(url)
        if not records:return []
        if type(records) == bool: return []
        for v in records:
            s = '{prefix}/{branch}:'.format(prefix='' if branch == "trunk" else '/branches', branch=branch)
            if v.startswith(s):
                str_versions = v[len(s):]
                versions = str_versions.split(',')  # 合并记录按照逗号分隔
                result = []
                for vs in versions:
                    p = re.match(r'^(?P<v1>\d+)\-?(?P<v2>\d*)', vs)
                    if p and "v1" in p.groupdict() and "v2" in p.groupdict():
                        v1 = p.groupdict()['v1']
                        v2 = p.groupdict()['v2']
                        if v1 and v2:
                            for x in range(int(v1), int(v2) + 1):
                                result.append(x)
                        else:
                            result.append(int(v1))
                return sorted(result, lambda a, b: cmp(b, a))

    @classmethod
    def make_svn_url(cls, host, branch):
        if branch == "trunk":
            return host + "/trunk"
        else:
            return host + "/branches/" + branch

    @classmethod
    def get_unmerge_records(cls,url, from_branch, to_branch, maxlimit, filters = list(), stop_on_copy = True):
        from_url = SVN.make_svn_url(url, from_branch)
        to_url = SVN.make_svn_url(url, to_branch)
        if stop_on_copy:
            startVersion = SVN.get_start_version(to_url)
            if not startVersion:return
        else:
            startVersion = 0
        merged_records = SVN.get_merge_record_from_branch(to_url, from_branch)
        records = SVN.get_records(from_url, maxlimit)
        if not records:return
        results = []
        for record in records:
            if record.version > startVersion and not record.version in merged_records and not record.filter(filters):
                results.append(record)
        return results

    @classmethod
    def get_version_diffs(cls,url,vb,ve):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        logs = check_output("svn diff {url} -r {vb}:{ve} --summarize {identify}".format(url=url, vb=vb,ve=ve, identify=identify))
        # 长度小于3（A、M、D、AM即增加且修改）即是更新标识
        if not logs: return
        if isinstance(logs, bool): return
        result = []
        for x in logs:
            if x[0:1] == "D": continue
            result.append(x[1:].lstrip(' ').replace(url+'/',""))
        return result

    @classmethod
    def export_diffs(cls, url,dst, vb, ve):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        diff_list = SVN.get_version_diffs(url, vb, ve)
        if diff_list is not None:
            result = []
            for x in diff_list:
                file_url = url + "/" + x
                file_path = dst + "/" + x
                file_dir = os.path.split(os.path.realpath(file_path))[0]
                if not os.path.exists(file_dir): os.makedirs(file_dir)
                if not check_output('''svn export {file_url} "{file_path}" {identify} --force'''.format(
                        file_url=file_url,
                        file_path=file_path.replace('\\', '/'),
                        identify=identify)):
                    raise "export error."
                if os.path.isfile(file_path): result.append(file_path)
            return result


    @classmethod
    def export_record(cls,url,dst,version):
        identify = ""
        if SVN.username: identify += " --username=" + SVN.username
        if SVN.password: identify += " --password=" + SVN.password
        diff_list = SVN.get_version_diffs(url,version-1,version)
        if not diff_list:return
        result = []
        for x in diff_list:
            file_url = url + "/" + x
            file_path = dst + "/" + x
            file_dir = os.path.split(os.path.realpath(file_path))[0]
            if not os.path.exists(file_dir): os.makedirs(file_dir)
            if not check_output('''svn export -r {version} {file_url} "{file_path}" {identify} --force'''.format(version=version,
                                                                                                file_url=file_url,
                                                                                                file_path=file_path.replace('\\','/'),
                                                                                                identify=identify)):
                #raise "export error."
                print("export error file_url : " + file_url)
            if os.path.isfile(file_path): result.append(file_path)
        return result

if __name__ == "__main__":
    #result = SVN.get_version_diffs("http://10.236.192.18/svn/seven_client/trunk",29830,29831)
    #print result
    SVN.export_record("http://10.236.192.18/svn/seven_client/trunk","F:/export",29831)