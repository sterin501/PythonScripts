#!/bin/python



import rpyc,argparse,time,platform,os,socket
from plyer import notification



parser = argparse.ArgumentParser()
parser.add_argument('-port', '--port', default='',help='port to monitor')
parser.add_argument('-pid', '--pid', default='',help='process to monitor')
parser.add_argument('-p', '--p', default='',help='Serach for the process and monitor')
parser.add_argument('-s','--server',default='localhost',help='Server to connect , default is localhost')
parser.add_argument('-file','--file',default='',help='File to Search')
parser.add_argument('-keyword','--keyword',default='',help='Keyword To Search')
parser.add_argument('-name','--name',default='name',help='Client User Name to track in server')
parser.add_argument('-domain','--domain',default='',help='weblogic domain to monitor')
parser.add_argument('-ping','--ping',default='',help='ping a server or server with port .IP or IP:PORT')
args = parser.parse_args()
currentPortMessage=''



def clientPIDMonitor(pidtocheck):
 try:
   runtheloop=c.root.pid(pidtocheck,True)
   if (runtheloop):
    print 'Process is running will monitor '
    while runtheloop:
     time.sleep(1)
     runtheloop=c.root.pid(pidtocheck,False)
    print ' Proces is over , will alert'
    alertDesktop('Process is stopped',(pidtocheck + '  is stopped on server ' + args.server))
   else:
     print 'Process is not  running '
 except KeyboardInterrupt :
  print 'Stopping'

def clientProcessSearch():
 kk =  c.root.processFinder(args.p).split("\n")
 if len (kk) == 2:
  print kk
  togetPID=kk[0].split(' ')
  for po in togetPID:
   try:
    if int (po) > 1:
      ppm=po
      break
   except :
    continue
  print 'Only one process and it will monitor  ' +ppm
  clientPIDMonitor(ppm)
 elif len (kk) > 1:
  for it in kk:
   print it
  print '...... Multiple process found , so please provide pid and monitor again. use -pid option'
 else:
  print 'No process found' 



def portMonitor(server,port):
 global currentPortMessage
 print ( ' Monitoring port ' + port + ' on server ' + server + ' To stop use CTR+C ') 
 runloop=True
 mainFlag=getPortStatus (c.root.portChecker(server,int (port)  ) )
 print (' Current status : ' +  port + ' on server ' + server +  currentPortMessage ) 
 try:
   while runloop:
    tempStatus=getPortStatus(c.root.portChecker(server,int (port)))
    if (tempStatus != mainFlag):
     print ' Change in status will alert  :: Now Port  ' + currentPortMessage
     alertDesktop('PORT STATUS CHANGE',( port + ' on  ' +  server + currentPortMessage))
     mainFlag=tempStatus
    time.sleep(1)
 except KeyboardInterrupt as e:
  print 'Stopping ..' 

def getPortStatus(status):
 global currentPortMessage
 if status == 0:
   currentPortMessage=  '  is UP '
   return True
 else:
  currentPortMessage= ' is down '
  return False

def getKeywordInFile(filename,keyword):
 runloop=True
 readc=0
 alertNow=False
 try:
   while runloop:
    readstatus = c.root.keyWordSearchInFile(filename,keyword,readc)
    if ("YES:" in readstatus):
     print (readstatus)
     readc= int ( readstatus.split(':')[1] ) +1
     if alertNow:
      print ('it will alert')
      alertDesktop('Keyword Found',( keyword + ' found on file'))
      alertNow=False
    else :
     if (readc != int (readstatus.split(':')[1]) ):
      print(readstatus)
      readc= int ( readstatus.split(':')[1] )
     alertNow=True
    time.sleep(1)
 except KeyboardInterrupt as e:
  print 'Stopping ..' 


def alertDesktop (summary,stringtodisplay):
 try :
  notification.notify(
     title=summary,
     message=stringtodisplay,
     app_name='MonitoTool',
                       )
 except Exception as e:
  print ' Not able to alert desktop'
  print e 
  

def weblogicDomain(domainpath):
 dd = c.root.weblogicDomain(  domainpath) 
 if ( dd == "Not valid" ):
  print ' no config.xml found, Not valid weblogic domain'
 else :
  print 'Valid Weblogic domain  '
  print ' .... Servers ....\n\n'
  count=0
  for kk in dd:
   if (  len (kk)  > 1 ):
    if (kk [2]):
     print kk[0] + '  '  + kk[2]+':'+ kk[1]
     dd[count]=[kk[0],kk[1],kk[2]]
    else:
     print kk[0] + '  ' +  args.server+':'+ kk[1]
     dd[count]=[kk[0],kk[1],args.server]
    if ( len (kk[1]) < 4 ):
     dd[count]=[kk[0],"7001",args.server] 
   else :
     del dd [count] 
   count=count+1
 monitorWeblogic(dd)

def monitorWeblogic(servers):
 runloop=True
 message=''
 print ' \n\n.. Going to Monitor the servers \n\n' 
 alertNow=False
 try :
  while runloop:
   time.sleep(1)
   messageInloop=''
   for server in servers:
    mainFlag=getPortStatus (c.root.portChecker(server[2],int (server[1])  ) )
    messageInloop =messageInloop+ ( server[0] + '  ' + server[2]+':'+server[1] + ' '+  currentPortMessage )+'\n'
   if (message != messageInloop):
    if alertNow:
     for test, correct in zip(message.split('\n'), messageInloop.split('\n')):
      if (test != correct):
       alertDesktop("Weblogic Domain",correct)
    print messageInloop
    message=messageInloop
    alertNow=True
 except KeyboardInterrupt as e:
  print 'Stopping ..' 

def offlinePing(URL):
 if (":" in URL):
   serverIP=URL.split(":")[0]
   serverPort=URL.split(":")[1]
   monitorOfflinePort(serverIP,int (serverPort) )
 else:
  hostname=URL
  if platform.system() == "Windows":
        command = "ping "+hostname+" -n 1"
  else:
        command = "ping -c 1 " + hostname +" &>/dev/null"
  monitorPing(command)

def monitorPing(command):
 runloop=True
 response = os.system(command)
 if response == 0:
     print ( args.ping + "  is UP , will monitor" )
 else :
     print ( args.ping + "  is Down will monitor" )
 try :
  while runloop:
   time.sleep(1)
   responseTemp = os.system(command)
   if responseTemp != response:
    print (' Change status , will alert ')
    if responseTemp == 0: 
     print ( args.ping + "  is UP ")
     alertDesktop("PING STATUS CHANGE",args.ping + "  is UP ")
    else :
     print ( args.ping + "  is down" )
     alertDesktop("PING STATUS CHANGE",args.ping + "  is Down ")
    response=responseTemp
 except KeyboardInterrupt as e:
  print 'Stopping ..' 



def monitorOfflinePort(serverIP,serverPort):
 sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 result = sock.connect_ex((serverIP,serverPort))
 print result
 runloop=True
 if result == 0:
     print ( args.ping + "  is UP , will monitor" )
 else :
     print ( args.ping + "  is Down will monitor" )
 try :
  while runloop:
   time.sleep(1)
   sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   responseTemp = sock.connect_ex((serverIP,serverPort))
   if responseTemp != result:
    print (' Change status , will alert ')
    if responseTemp == 0: 
     print ( args.ping + "  is UP ")
     alertDesktop("PING STATUS CHANGE",args.ping + "  is UP ")
    else :
     print ( args.ping + "  is down" )
     alertDesktop("PING STATUS CHANGE",args.ping + "  is Down ")
    result=responseTemp
 except KeyboardInterrupt as e:
  print 'Stopping ..' 


if __name__ == '__main__':
 try:
  if (args.ping):
    offlinePing(args.ping)
  else:
   print ('Connecting '+ args.server)
   c = rpyc.connect(args.server, 18812)
   print c.root.echo(args.name)
   if (args.pid):
    clientPIDMonitor(args.pid)
   elif (args.p):
    clientProcessSearch()
   elif (args.port):
    portMonitor(args.server,args.port)
   elif (args.file):
    if (args.keyword):
     getKeywordInFile ( args.file , args.keyword)
    else:
     print 'Keyword is required '
   elif (args.domain):
    weblogicDomain(args.domain)
 except Exception as e:
  print e
 
