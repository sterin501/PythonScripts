#!/bin/python

import rpyc,datetime,os,subprocess,socket,logging,logging.handlers
import lxml.etree as ET
from rpyc.utils.server import ThreadedServer


LOG_FILENAME = '/tmp/monitorServer.log'
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s -   %(message)s")
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1024, backupCount=5)
handler.setFormatter(formatter)

my_logger.addHandler(handler)



def pidChecker(pid):
 RunningProccess=False
 try :
       ds=os.getpgid(int (pid) )
       RunningProccess=True
 except OSError :
       now = datetime.datetime.now()
       my_logger.info ( pid +' is not responding at ' + str  (now) )
 return RunningProccess


def processFinder(keyword):
 commandtouse = 'grep -w "'+keyword+'"'
 pc1 = subprocess.Popen('ps -ef', stdout=subprocess.PIPE, shell=True)
 pc2 = subprocess.Popen(commandtouse, stdin=pc1.stdout, shell=True,
                      stdout=subprocess.PIPE)
 pc3 = subprocess.Popen('grep -v client.py ' , stdin=pc2.stdout,shell=True,
                       stdout=subprocess.PIPE)
 pc4 = subprocess.Popen('grep -v grep ' , stdin=pc3.stdout,shell=True,
                       stdout=subprocess.PIPE)
 return pc4.communicate()[0]



def keywordInfile(filepath,keyword,tostartRead):
 #my_logger.info ('File '+ filepath + ' Keyword  ' + keyword + 'To Read from ' + str   (tostartRead) )
 try :
  with open (filepath) as fin:
   for num, line in enumerate(fin, 1):
    if (tostartRead > num):
     continue
    if keyword in line:
     returnstring='YES:'+str(num)+':'+line
     my_logger.info (returnstring)
     return (returnstring)
  return('NO:'+str(num))
 except IOError:
  return('File NOT FOUND')


def weblogicDomainStatus(domainPath):
 configLoc=domainPath+"/config/config.xml"
 if (os.path.exists(configLoc)):
  print 'Valid Domain'
  return getWeblogiServers(configLoc)
 else:
   print 'Not valid'
   return 'Not valid'


def getWeblogiServers(configLoc):
 f = open(configLoc,'rb')
 tree = ET.parse(f)
 root = tree.getroot()
 namespace="http://xmlns.oracle.com/weblogic/domain"
 servers = tree.findall('.//{%s}server' % namespace)
 count=0
 servDetails=["","",""]
 for server in servers:
  name=''
  port=''
  add=''
  for child in server:
    tag = child.tag
    val = child.text
    if tag == "{http://xmlns.oracle.com/weblogic/domain}name":
       name=val
    elif tag == "{http://xmlns.oracle.com/weblogic/domain}listen-port":
       port=val
    elif tag == "{http://xmlns.oracle.com/weblogic/domain}listen-address":
       add=val
  servDetails[count]=[name,port,add]
  count=count+1
 return servDetails
 



class MyService(rpyc.Service):
    def exposed_echo(self, text):
         now = datetime.datetime.now()
         my_logger.info ( 'got request at  '+ str (now) +' from ' + text)
         return "OK"
    def exposed_pid(self,pid,PrintOutput):
        if (PrintOutput):
         my_logger.info ('pid to monitor ' + pid)
        if  pidChecker(pid):
         if (PrintOutput):
          my_logger.info ('pid  ' + pid + '  is still running ')
         return True
        else :
         my_logger.info ('pid  ' + pid + ' is Stooped ')
         return False
    def exposed_processFinder(self,keyword):
        return processFinder(keyword)
    def exposed_portChecker(self,serverIP,serverPORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock.connect_ex((serverIP,serverPORT))
    def exposed_keyWordSearchInFile(self,filepath,keyword,tostartRead):
        return keywordInfile(filepath,keyword,tostartRead)
    def exposed_weblogicDomain(self,domainPath):
        return weblogicDomainStatus(domainPath)
    
 
      
    
if __name__ == "__main__":
    server = ThreadedServer(MyService, port = 18812)
    my_logger.info(" Listening at 18812")
    server.start()


