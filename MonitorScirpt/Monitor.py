#!/usr/bin/python

import smtplib
import os,datetime
import socket
import urllib


def ping(hosts):               ## will use ping commnad of linux , in windows different format 
 check=False
 for host in hosts.split(','):
  response = os.system("ping -c1 -W1 -q  " + host +" &>/dev/null")
  if (response ==0):
   check=True
  #print ('Pinging  '+host+" "+response)
 return check

def sendEmail(sender, receivers, message):             ## API to send email
 try:
   smtpObj = smtplib.SMTP('SMTPSERVER')
   smtpObj.sendmail(sender, receivers.split(','), message)         
   print "Successfully sent email"
 except smtplib.SMTPException as e:
   print "Error: unable to send email"
   print str(e)


def checkLockFile(server):                       ### one alert email per day 
 sendemail=False
 if (os.path.exists("lock/"+server)):
  filetime = datetime.datetime.fromtimestamp(os.path.getmtime ("lock/"+server))
  now =  datetime.datetime.now()
  print ( str (now) +"    "+  str (filetime) )
  difference = now - filetime
  print (  str (difference) )
  if ( difference.days > 0 ):  ## difference.days will be used
   sendemail=True
 else:
  file = open("lock/"+server, 'w+')
  file.close()
  sendemail=True
 return   sendemail     
  

def pingPort (URL):                                                ## will ping to port using socket API
 check=False
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 serverIP=URL.split(':')[0]
 serverPORT=int (URL.split(':')[1])
 result = sock.connect_ex((serverIP,serverPORT))
 if result == 0:
  check=True
 return check

def  JDBCORCL (URL):
  check=False
  response=os.popen("./runJDBC.sh  "+URL).read()
  if (response == "0\n"):                            ## Some how new line is there in the output \n added for verification  .strip() can be used
    check=True
  return check

def URLPING (URL):                                         ## urlib is used to ping the server , will return 200 for success
 check=False
 try:
  response=urllib.urlopen(URL).getcode()
  if ( response == 200):
   check=True
 except Exception as e:
  print e
 return check


def checkAndCreateEmail (server):                            ## it will create and send email when server went down
 defaultmessage = """From: PingServer <user@email.com>
To: FristNAme LastName <user@email.com>
MIME-Version: 1.0
Content-type: text/html
Subject: """
 sender = 'user@email.com'
 emailMessage=''
 if (checkLockFile(server)):
         print ('Email will send')
         with open("message/"+server+".txt") as messagefin:          ## it will read form meassge folder with alert message . html tag can be used there .servename
          for messageline in messagefin:                             ## should match with server.txt
           emailMessage=emailMessage+messageline
          message=defaultmessage+server+""" is down





  

"""+emailMessage+"""     
"""     
        # print (receivers + "^^^^^^^^\n" + message)
        # #sendEmail(sender,receivers,message)
         file = open("lock/"+server, 'w+')
         file.write("DOWN")
         file.close()
         sendEmail(sender,receivers,message)


def checkAndCreateEmailUP (server):                       ## it will create and  send email when server back on line 
 defaultmessage = """From: PingServer <user@email.com>
To: MYBAME <user@email.com>
MIME-Version: 1.0
Content-type: text/html
Subject: """
 sender = 'user@email.com'
 emailMessage=server+' is back'
 print ('Email will send')
 message=defaultmessage+server+""" is up and running





  

"""+emailMessage+"""     
"""     
        # print (receivers + "^^^^^^^^\n" + message)
        # #sendEmail(sender,receivers,message)
 file = open("lock/"+server, 'w+')
 file.write("UP")
 file.close()
 sendEmail(sender,receivers,message)


def grepSerchServer (word):                        ## to check server back again once it was down
 with open("server.txt") as fin:
  for line in fin:
   if line.startswith('#'):
    continue
   if (word in line):
    print line
    activity=line.split()[0]
    server=word
    URL=line.split()[2]
    receivers=line.split()[3]
    emailMessage=''
    if (activity in ('PING')):
       if  (ping (URL)):
        print (server + ' is up')
        checkAndCreateEmailAfterUP (server)
        
    elif (activity in ('PINGPORT')):
       if  ( pingPort(URL)):
        print ( server+ ' is up') 
        checkAndCreateEmailAfterUP (server)
        
    elif  (activity in ('JDBCORCL')):
       if  ( JDBCORCL(URL)):
        print ( server+ ' is up') 
        checkAndCreateEmailAfterUP (server)

    elif  (activity in ('URLPING')):
      if  ( URLPING(URL)):
        print ( server+ ' is up') 
        checkAndCreateEmailAfterUP (server)


with open("server.txt") as fin:   ## It will check the servers from server.txt , it should match with meassge folder
    for line in fin:
     if line.startswith('#'):
      continue
     activity=line.split()[0]
     server=line.split()[1]
     URL=line.split()[2]
     receivers=line.split()[3]
     emailMessage=''
     print ( str (datetime.datetime.now()) + " " + activity + " " + server)
     if (activity in ('PING')):
       #print 'will do ping'
       if not (ping (URL)):
        print (server + ' is down')
        checkAndCreateEmail (server)
        
     elif (activity in ('PINGPORT')):
       if not ( pingPort(URL)):
        print ( server+ ' is down') 
        checkAndCreateEmail (server)
        
     elif  (activity in ('JDBCORCL')):
       if not ( JDBCORCL(URL)):
        print ( server+ ' is down') 
        checkAndCreateEmail (server)

     elif  (activity in ('URLPING')):
      if not ( URLPING(URL)):
        print ( server+ ' is down') 
        checkAndCreateEmail (server)
print 'Checking UP status'
folder="lock"
for kk in os.listdir(folder):
 with open(folder+"/"+kk) as fin:
  for line in fin:
   if  line=="DOWN":
    grepSerchServer(kk)










