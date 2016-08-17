#!/bin/python
import urllib, urllib2, cookielib,re , sys,timeit

if ( len(sys.argv) !=2):
 print 'dID is reqired'
 sys.exit(0)

username = 'weblogic'
password = 'welcome1'

UCMIP='ucm.company.com'
UCMPORT='16201'

print ( 'Loging to '  +UCMIP+':'+UCMPORT)
start_time = timeit.default_timer()
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'j_username' : username, 'j_password' : password})
resp= opener.open('http://'+UCMIP+':'+UCMPORT+'/cs/login/j_security_check', login_data)
print ( 'Time Taken : ' + repr (timeit.default_timer() - start_time))
regex = 'idcToken = ".{13,47}"'
pattern = re.compile(regex)
dDocName=''
dOriginalName=''
dID=sys.argv[1]
if (re.search('IntradocLoginState=1',str(cj))):
 for line in resp:
  if  re.findall(pattern,line):
   idctoken = line.split('"')[1]
 docinfo_data = urllib.urlencode({
                                    'dID'            : dID,
                                    'idcToken'       : idctoken,
                                    'IdcService'     : 'DOC_INFO',
                                    'IsSoap'         : '1'
                                  })
 print ('Getting Doc info ' + dID)
 start_time = timeit.default_timer()
 resp = opener.open('http://'+UCMIP+':'+UCMPORT+'/cs/idcplg?',docinfo_data)
 regex ='dOriginalName="*"'
 c = 0
 pattern = re.compile(regex)
 for line in resp:
  if  re.findall(pattern,line):
   tempwor = line.split('="')
   for wor in line.split('="'):
    if ( re.search('dDocName',wor)):
     dDocName = (tempwor[c+1].split('"')[0])
    elif ( re.search('dOriginalName',wor)):
     dOriginalName = (tempwor[c+1].split('"')[0])
    c+=1
 print ( 'Time Taken : ' + repr (timeit.default_timer() - start_time))
 if ( dDocName == ''):
  print ( ' wrong dID .. exiting')
  sys.exit(0)
 file = open(dOriginalName, 'w+')
 print ( 'Downloadig dDocName: '+ dDocName + ' ,FileName: ' + dOriginalName)
 download_data =  urllib.urlencode({
                                    'dID'            : dID,
                                    'dDocName'       : dDocName ,
                                    'allowInterrupt' : '1' ,
                                    'IdcService'     : 'GET_FILE' ,
                                    'idcToken'       : idctoken 
                  })
 start_time = timeit.default_timer()
 resp = opener.open('http://'+UCMIP+':'+UCMPORT+'/cs/idcplg?',download_data)
 file.write(resp.read())
 file.close()
 print (dOriginalName + ' is created  \nTime Taken : ' + repr (timeit.default_timer() - start_time))
else:
 print (' IN VALID Login')
