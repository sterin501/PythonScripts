#!/bin/python
import requests
import re
from lxml import html

USERNAME = "weblogic"
PASSWORD = "welcome1"

#LOGIN_URL = "http://10.184.36.144:16471/cs/login/j_security_check"
#URL = "http://10.184.36.144:16471/cs/idcplg?IdcService=DOC_INFO&dID=3223&dDocName=STJACOBPC1IDCO003622&IsSoap=1"

LOGIN_URL = "http://ucm.company.com:16200/cs/login/j_security_check"
URL = "http://ucm.company.com:16200/cs/idcplg?IdcService=DOC_INFO&dID=414&dDocName=AWSECM000414&IsSoap=1 "


session_requests = requests.session()

# Get login csrf token
result = session_requests.get(LOGIN_URL)

# Create payload
payload = {
        "j_username": USERNAME, 
        "j_password": PASSWORD, 
    }

flag = 0 
# Perform login
result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
regex = 'idcToken = ".{13,47}"'
pattern = re.compile(regex)
for line in result:
     role = re.findall(pattern,line)
     if role:
        print line
        flag=1

if (flag==1):
 result = session_requests.get(URL, headers = dict(referer = URL))
 for line in result:
     print(line)
else:
 print("In Valid Login")


