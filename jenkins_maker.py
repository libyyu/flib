# -*- coding: utf-8 -*-
"""
curl -X POST http://10.236.100.108:8080/view/策划视图/job/cehua_make_client_dev_win/build \
--user lidengfeng:cd53836aa8f9213659b8d13420e43074 \
--data-urlencode json='{"parameter": {"SVN_BRANCH":"trunk"}}'

curl -X POST http://10.236.100.108:8080/view//策划视图//job/cehua_make_client_dev_win/buildWithParameters \
--user lidengfeng:cd53836aa8f9213659b8d13420e43074 \
--data-urlencode json='{"parameter": {"SVN_BRANCH":"trunk"}}'

curl -X POST http://10.236.100.233:8080/view/1-%E7%AD%96%E5%88%92/job/sync_samba_cehua_data/buildWithParameters \
--user lidengfeng:cd53836aa8f9213659b8d13420e43074 \
--data-urlencode json='{"parameter": {"OPTION":"NONE","BUILD_USER_NAME":"lidengfeng"}}'

"""

import os, sys
import jenkins

server_url = "http://10.243.65.75:8080"
user_id = "lidengfeng"
api_token = "cd53836aa8f9213659b8d13420e43074"

server = jenkins.Jenkins(server_url, username=user_id, password=api_token)
# next_build_number = server.get_job_info('view_zdir_info')['nextBuildNumber']
# respond = server.build_job("view_zdir_info", parameters={"PLAT":"PC"})
# print(respond)
# from time import sleep; sleep(10)
# while True:
#     build_info = server.get_build_info('view_zdir_info', next_build_number)
#     print(build_info)
#     break
# from time import sleep; sleep(10)
# build_info = server.get_build_info('cehua_make_client_dev_win', next_build_number)
# print(build_info)

#runing_info = server.get_running_builds()
#print(runing_info)
#job = server.get_job_info("获取资源版本号")
#print(job)



def main():
	try:
		istr = sys.argv[1] if len(sys.argv) >1 else "$BUILD_USER_ID"
		next_build_number = server.get_job_info('sync_samba_cehua_data')['nextBuildNumber']
		print("next_build_number:", next_build_number)
		respond = server.build_job("sync_samba_cehua_data", parameters={"OPTION":"NONE", "BUILD_USER_NAME":istr})
		#print(respond)
		from time import sleep; sleep(0.5)
	except Exception as e:
		sys.exit(1)

if __name__ == '__main__':
	main()
