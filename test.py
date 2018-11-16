# -*- coding: utf-8 -*-
"""
curl -X POST http://10.236.100.108:8080/view/策划视图/job/cehua_make_client_dev_win/build \
--user lidengfeng:cd53836aa8f9213659b8d13420e43074 \
--data-urlencode json='{"parameter": {"SVN_BRANCH":"trunk"}}'

curl -X POST http://10.236.100.108:8080/view//策划视图//job/cehua_make_client_dev_win/buildWithParameters \
--user lidengfeng:cd53836aa8f9213659b8d13420e43074 \
--data-urlencode json='{"parameter": {"SVN_BRANCH":"trunk"}}'

"""
import jenkins

server_url = "http://10.236.100.108:8080"
user_id = "lidengfeng"
api_token = "cd53836aa8f9213659b8d13420e43074"

server = jenkins.Jenkins(server_url, username=user_id, password=api_token)
print(server)
next_build_number = server.get_job_info('cehua_make_client_dev_win')['nextBuildNumber']
print (server.build_job("cehua_make_client_dev_win", parameters={"SVN_BRANCH":"trunk"}))
from time import sleep; sleep(10)
build_info = server.get_build_info('cehua_make_client_dev_win', next_build_number)
print(build_info)
