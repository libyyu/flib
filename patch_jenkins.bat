@echo off
@rem chcp 936
@set local_self_path=%~dp0
@set local_self_path=%local_self_path:~,-1%


pyinstaller -Fc %local_self_path%\test.py -n jenkins_maker
@pause
