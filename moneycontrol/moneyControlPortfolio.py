#!/bin/python
import requests
import re
import bs4

USERNAME = "AjithAgarkar"
PASSWORD = "cricket1234"

LOGIN_URL = "https://accounts.moneycontrol.com/login/index"
URL= "http://www.moneycontrol.com/bestportfolio/wealth-management-tool/investments#port_top"

session_requests = requests.session()
# Create payload
payload = {
          'email' : USERNAME,
          'pwd' : PASSWORD ,
    }
result = session_requests.post(LOGIN_URL, data = payload)
newresult = session_requests.get("http://www.moneycontrol.com/bestportfolio/wealth-management-tool/investments#port_top")
## BeautifulSoup
soup = bs4.BeautifulSoup(newresult.content,"lxml")
table  = soup.find_all("div", "rightCont")

#print table
commodittTableRows =  table[0].find_all("div")
cl = commodittTableRows[0].find_all("p")

words=''


for jj in cl:

 if ( re.search('networth_disp',repr(jj))):
  for kk in  repr(jj).split('span'):
   if 'networth_disp' in kk:
    words = 'Net Worth is '+ kk.split('>')[1][:-2]
   if '"r_18"' in kk:
     words = "31;40m"+words + '  '+ u"\u25BC" + kk.split('strong>')[1][:-2]
   if '"r_16"' in kk:
     words = words + '  '+   kk.split('>')[1][:-2]
   if '"gr_18"' in kk:
     words ="32;40m"+ words +'   '+  u"\u25B2"  + kk.split('strong>')[1][:-2]
   if '"gr_16"' in kk:
     words = words + '  '  + kk.split('>')[1][:-2]

CSI="\x1B["
reset=CSI+"m"
#print CSI+"32;40m" +words+CSI + "0m"
print CSI+ words+ CSI + "0m"

