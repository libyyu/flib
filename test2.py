# -*- coding: utf-8 -*-
import jenkins

server_url = "http://10.236.100.108:8080/"
user_id = "lidengfeng"
api_token = "199010"

server = jenkins.Jenkins(server_url, username=user_id, password=api_token)
print (server)
