#!/bin/python
import urllib, urllib2,re,bs4,cookielib,sys,time,argparse
from gi.repository import Notify

LIVGETURL="http://m.cricbuzz.com/cricket-match/live-scores"
cj = cookielib.CookieJar()
IsMatchLive=True
AlertInWords=''
AlertInWordsLatest=''
IsSecondBatting=False
IsTestMatch=False
Is4thInningsInTest=False
MatchSummaryURL=''
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--team', default='ind-',help='Team Name to search ,default team is india (ind).')
parser.add_argument('-p', '--proxy', default='',help='http proxy details to connect')
parser.add_argument('-r', '--refreshtime', default=30.0,help='Refresh time . Default is 30 sec')
args = parser.parse_args()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
if (len (args.proxy) > 0):
 proxy = urllib2.ProxyHandler({'http': args.proxy})
 opener = urllib2.build_opener(proxy)





def getIndiaURL(teamName):
    global IsTestMatch
    global MatchSummaryURL
    MatchSummaryURL=''
    try :
     resp= opener.open(LIVGETURL)
    except Exception as e:
     print e
     print 'check the proxy setting http_proxy'
     sys.exit()
    soup = bs4.BeautifulSoup(resp.read(),"lxml")
    table  = soup.find_all("div", "btn-group cbz-btn-group")
    for k in table:
     hreftuple = k.find_all("a","btn btn-default")
     for hrefmember in  hreftuple:
       stringURL = str (hrefmember)
       if ( re.search(teamName, stringURL)):
        spliting = stringURL.split('"')
        if('cricket-match-summary' in spliting[3]):
           MatchSummaryURL = 'http://m.cricbuzz.com/'+spliting[3]
           if ('test' in MatchSummaryURL):
             print 'Test Match'
             IsTestMatch=True
    return MatchSummaryURL
    

def getLiveScore (MatchSummaryURL):
 CricketObject = ['SUMMARY',['TEAM1',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0],['TEAM2',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0]]
 if IsTestMatch:
  CricketObject = ['SUMMARY',['TEAM1',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0],['TEAM2',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0],['TEAM1',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0],['TEAM2',0,0,0.0],['BATNAME1',0,0,'BATNAME2',0,0]]
 for loopc in range (0,6):
  try :
    resp= opener.open(MatchSummaryURL)
    soup = bs4.BeautifulSoup(resp.read(),"lxml")
    table  = soup.find_all("div", "list-group")
    arrycount=1
    for k in table:
        if (re.findall('cbz-ui-status',str (k))):
          CricketObject[0]=getFormatedScore (str (k))
    miniscore = k.find_all("div","cb-list-item miniscore-data ")
    for km in miniscore:
     stringMiniscore = str (km)
     if ( re.search("team-totals",stringMiniscore)):
      TeamTotel=bs4.BeautifulSoup(stringMiniscore,"lxml")
      TeamTable=TeamTotel("span", "team-totals")
      CricketObject[arrycount] = getTeamRunWickets ( getFormatedScore (str (TeamTable)))
      arrycount=arrycount+1
     if ( re.search("Batting",stringMiniscore)):
      BattingSoup =bs4.BeautifulSoup(stringMiniscore,"lxml")
      ScoreTable = BattingSoup.find_all("b", "")
      CricketObject[arrycount] = getBatsManRuns (getFormatedScore ( str (ScoreTable))) 
      arrycount=arrycount+1
  except Exception as e:
    print ('Connection isssue : Atempt '+ str (loopc) )
    time.sleep(2)
    if (loopc == 5):
     print ('Connection is not resolved , check the network , exiting')
     sys.exit()
 return CricketObject 

  
def getTeamRunWickets(TeamScore):
  TeamRunWickets = ['TEAM',0,0,0.0]
  spliting = TeamScore.split(' ')
  TeamRunWickets[0] = spliting[0]
  splitingRun = spliting[1].split('/')
  TeamRunWickets[1]= int (splitingRun[0])
  TeamRunWickets[2]= int (splitingRun[1])
  TeamRunWickets[3]= float (spliting[2].replace("(",""))
  return TeamRunWickets
  


def getFormatedScore (stringToProcess):
 finalString=''
 ff = re.findall('>(.*?)<',stringToProcess)
 for val in ff:
  if ( len (val) > 2 ):
   finalString=finalString+val
 return finalString
   
 
def batString_split(s):
    return filter(None, re.split(r'(\d+)', s))


def getBatsManRuns(TeamScore):
   Batsmen = ['NAME',0,0,'NO',0,0]
   Details =  batString_split(TeamScore)
   Batsmen[0]=Details[0]
   Batsmen[1]= int (Details[1])
   Batsmen[2]= int (Details[3])
   if (Details[4]):
    Batsmen[3]=Details[4].replace(")","")
    Batsmen[4]=int (Details[5])
    Batsmen[5]=int (Details[7])
   return Batsmen



def printCricketScore ( CricketObject ):
 global IsSecondBatting
 global IsTestMatch
 global Is4thInningsInTest
 psummary = 'Summary   : '+CricketObject[0]
 plines=''
 for i in range (0, len (psummary)):
  plines=plines+'_'
 print plines+'\n'
 print psummary
 print plines+'\n'
 if (CricketObject[3][3] == 0.0 ):
   print (CricketObject[1][0] + '   ' + str (CricketObject[1][1]) + '/'+str (CricketObject[1][2]) + ' in ' + str (CricketObject[1][3]) + '  in Overs .')
   print plines+'\n'
   print (CricketObject[2][0] + '   ' + str ( CricketObject[2][1])+ '('+str (CricketObject[2][2])+')')
   if ( CricketObject[2][3] != 'BATNAME2'):
    print (CricketObject[2][3] + '   ' + str (CricketObject[2][4])+ '('+str (CricketObject[2][5])+')')
    print plines+'\n'
 elif ( not IsTestMatch or CricketObject[5][3] == 0.0  ):
   IsSecondBatting=True
   print (CricketObject[1][0] + '   ' + str (CricketObject[1][1]) + '/'+str (CricketObject[1][2]) )
   print (CricketObject[3][0] + '   ' + str (CricketObject[3][1]) + '/'+str (CricketObject[3][2]) + ' in ' + str (CricketObject[3][3]) + '  in Overs ..')
   print plines+'\n'
   print (CricketObject[4][0] + '   ' + str ( CricketObject[4][1])+ '('+str (CricketObject[4][2])+')')
   if ( CricketObject[4][3] != 'BATNAME2'):
    print (CricketObject[4][3] + '   ' + str (CricketObject[4][4])+ '('+str (CricketObject[4][5])+')')
    print plines+'\n'
 elif ( CricketObject[7][3] == 0.0 ):
   print (CricketObject[1][0] + '   ' + str (CricketObject[1][1]) + '/'+str (CricketObject[1][2]) )
   print (CricketObject[3][0] + '   ' + str (CricketObject[3][1]) + '/'+str (CricketObject[3][2]) )
   print (CricketObject[5][0] + '   ' + str (CricketObject[5][1]) + '/'+str (CricketObject[5][2]) + ' in ' + str (CricketObject[5][3]) + '  in Overs ...')
   print plines+'\n'
   print (CricketObject[6][0] + '   ' + str ( CricketObject[6][1])+ '('+str (CricketObject[6][2])+')')
   if ( CricketObject[6][3] != 'BATNAME2'):
    print (CricketObject[6][3] + '   ' + str (CricketObject[6][4])+ '('+str (CricketObject[6][5])+')')
   print plines+'\n' 
 else:
     Is4thInningsInTest=True
     print (CricketObject[1][0] + '   ' + str (CricketObject[1][1]) + '/'+str (CricketObject[1][2]) )
     print (CricketObject[3][0] + '   ' + str (CricketObject[3][1]) + '/'+str (CricketObject[3][2]) )
     print (CricketObject[5][0] + '   ' + str (CricketObject[5][1]) + '/'+str (CricketObject[5][2]) )
     print (CricketObject[7][0] + '   ' + str (CricketObject[7][1]) + '/'+str (CricketObject[7][2]) + ' in ' + str (CricketObject[7][3]) + '  in Overs ....')
     print plines+'\n'
     print (CricketObject[8][0] + '   ' + str ( CricketObject[8][1])+ '('+str (CricketObject[8][2])+')')
     if ( CricketObject[8][3] != 'BATNAME2'):
       print (CricketObject[8][3] + '   ' + str (CricketObject[8][4])+ '('+str (CricketObject[8][5])+')')
     print plines+'\n'


def CompareCricketObjects (CricketObject,CricketObjectInLopp):
 global IsSecondBatting
 global IsTestMatch
 global Is4thInningsInTest
 returnValue=False
 #print ( str (IsSecondBatting) + "  " +  str (IsTestMatch) + "  "+ str (Is4thInningsInTest))
 if (CricketObject[0] != CricketObjectInLopp[0]):       ## Summary
  if ( 'runs' in CricketObjectInLopp[0]):
   if (IsTestMatch):
    if ( ( 'trail' in  CricketObject[0] ) and  ( 'lead' in CricketObjectInLopp [0]) ):
     print ('Trail to Lead   Alert')
  else:
   print 'chage in Summary , alret'
   returnValue=True
   alertDesktop("Alert",CricketObjectInLopp[0])
   return  returnValue 
 if  IsSecondBatting:
   if (CompareTeamRunsWickets (CricketObject[3],CricketObjectInLopp[3])):
    returnValue=True
 elif ( IsTestMatch and  Is4thInningsInTest):
   if (CompareTeamRunsWickets (CricketObject[7],CricketObjectInLopp[7])):
    returnValue=True
 elif (IsTestMatch and CricketObject[5][3] != 0.0):
   if (CompareTeamRunsWickets (CricketObject[5],CricketObjectInLopp[5])):
    returnValue=True
 else:
   if (CompareTeamRunsWickets (CricketObject[1],CricketObjectInLopp[1])):
    returnValue=True
 return returnValue

def CompareTeamRunsWickets (TeamRuns,TeamRunsInLoop):
  global AlertInWordsLatest
  global AlertInWords
  returnValue=False
  wicketinloop = TeamRunsInLoop[2]
  wicket=TeamRuns[2]
  #print  ( str (wicket) + '..' + str (wicketinloop)  )
  #print  ( TeamRunsInLoop)
  TeamRunsinloop = TeamRunsInLoop[1]
  TeamRuns=TeamRuns[1]
  OverinLoop=TeamRunsInLoop[3]
  if (wicket != wicketinloop):
   print (str (wicket)+' --> '+str (wicketinloop) +' Wicket Gone')
   returnValue=True
   LiveCricketOb=getBatsManBlowerPRC()
   print ("\nLast Wicket   : "+LiveCricketOb[3][1]+"")
   alertDesktop("Wicket"+str (wicket)+' --> '+str (wicketinloop),LiveCricketOb[3][1])
  if (TeamRunsinloop >= ((TeamRuns/50)+1)*50 ):
    AlertInWordsLatest=TeamRunsInLoop[0]+' Scored '+ str (TeamRunsinloop) +"/"+ str (wicketinloop) +' in  '+str (OverinLoop)+' Overs'
    if ( AlertInWordsLatest != AlertInWords):
     print (AlertInWordsLatest + ' Alert')
     AlertInWords=AlertInWordsLatest
     returnValue=True
     alertDesktop("ScoreUpdate",AlertInWordsLatest)
  if (OverinLoop%10.0 == 0.0):
   AlertInWordsLatest=TeamRunsInLoop[0]+" "+ str (TeamRunsinloop) +"/"+str (wicketinloop) +' in  '+str (OverinLoop)+' Overs'
   if ( AlertInWordsLatest != AlertInWords):
     print (AlertInWordsLatest + ' Alert')
     AlertInWords=AlertInWordsLatest
     returnValue=True
     alertDesktop("ScoreUpdate",AlertInWordsLatest)
  return returnValue
 


def isMatchLiveNow (CricketObject,InLoop):
 global IsMatchLive
 stopStrings=['won','Stumps','Break','drawn']
 for kk in  stopStrings:
  if ( kk in CricketObject[0]):
   IsMatchLive=False
   print 'Not Live Now'
   if InLoop:
    alertDesktop("Summary",CricketObject[0])


def printLiveCricketScore(CricketObjectInLopp):
 finalStringToprint=''
 psummary = 'Summary   : '+CricketObjectInLopp[0]
 plines=''
 for i in range (0, len (psummary)):
  plines=plines+'_'
 finalStringToprint=finalStringToprint+plines+'\n\n'+psummary+'\n\n'+plines+'\n\n'
 count=1
 while (count < len (CricketObjectInLopp)):
  if not ('TEAM' in CricketObjectInLopp[count][0] ):
   finalStringToprint="\n"+finalStringToprint+CricketObjectInLopp[count][0]+"  "+str (CricketObjectInLopp[count][1])+"/"+str (CricketObjectInLopp[count][2])+"  "+str (CricketObjectInLopp[count][3])+" Over \n"
  count=count+2 
 LiveCricketOb=getBatsManBlowerPRC()
 finalStringToprint="\n"+finalStringToprint+LiveCricketOb[0]+"\n"
 finalStringToprint="\n"+finalStringToprint+plines+"\n"+plines+"\n\nBatting1 :  "+LiveCricketOb[1][0]+"    "+LiveCricketOb[1][1]+LiveCricketOb[1][2]+"  "+LiveCricketOb[1][3]+"  "   +LiveCricketOb[1][4]+"  " + LiveCricketOb[1][5]+"\n"
 if (LiveCricketOb[1][6] != "BAT2"):
  finalStringToprint=finalStringToprint+"Batting2 :  "+LiveCricketOb[1][6]+"    "+LiveCricketOb[1][7]+LiveCricketOb[1][8]+"  "+LiveCricketOb[1][9]+"  "   +LiveCricketOb[1][10]+"  " + LiveCricketOb[1][11]+"\n"
 finalStringToprint=finalStringToprint+"\n\n"+"Bowler  :  "+LiveCricketOb[2][0]+"    "+LiveCricketOb[2][1]+"    "+LiveCricketOb[2][2]+"    "+LiveCricketOb[2][3]+"    "+LiveCricketOb[2][4]+"\n\n"
 finalStringToprint=finalStringToprint+"\nPartnership   : "+LiveCricketOb[3][0]+""
 finalStringToprint=finalStringToprint+"\nLast Wicket   : "+LiveCricketOb[3][1]+""
 finalStringToprint=finalStringToprint+"\nRec Balls     : "+LiveCricketOb[3][2]+""
 finalStringToprint=finalStringToprint+"\n\n"+plines
 print finalStringToprint



def getBatsManBlowerPRC():
 global MatchSummaryURL 
 liveCricketObject=['RUNRATE',['BAT1',0,'BALS','4s','6s','SR','BAT2',0,'BALS','4s','6s','SR'],['BOW','O','M','R','W'],['PAT','Last Wicket','REC']]
 commentry=MatchSummaryURL.replace('cricket-match-summary','cricket-commentary')
 resp= opener.open(commentry)
 soup = bs4.BeautifulSoup(resp.read(),"lxml")
 table  = soup.find_all("div", "list-group")
 for k in table:
  miniscore = k.find_all("div","list-content")
  for kkm in miniscore:
    if ( re.search("CRR",str (kkm))):
     liveCricketObject[0]=(getFormatedScore ( str (kkm))).replace('\xc2\xa0', ' ')
    if (re.search("Batting",str (kkm))):
     liveCricketObject[1]= getLiveBatsMan(getFormatedScoreForBBPRC ( str (kkm)))
    if (re.search("Bowling",str (kkm))):
     liveCricketObject[2]= getLiveBolwer (getFormatedScoreForBBPRC ( str (kkm)))
    if (re.search("Recent balls",str (kkm))):
     liveCricketObject[3]= getPatLastRec  (getFormatedScoreForBBPRC ( str (kkm)))
 return liveCricketObject

def getFormatedScoreForBBPRC (stringToProcess):
 finalString=''
 ff = re.findall('>(.*?)<',stringToProcess)
 for val in ff:
  if ( len (val) > 0 ):
   finalString=finalString+'-'+val
 return finalString


def getLiveBatsMan (stringToProcess):
 newSrin=stringToProcess.split('-')
 BatsMan=['BAT1',0,'BALS','4s','6s','SR','BAT2',0,'BALS','4s','6s','SR']
 count=6
 arr=0
 for i in range (count,len (newSrin) ): 
  BatsMan[arr]=newSrin[count]
  arr=arr+1
  count=count+1
 return BatsMan

def getLiveBolwer (stringToProcess):
 newSrin=stringToProcess.split('-')
 Bolwer=['BOW','O','M','R','W']
 count=6
 arr=0
 for i in range (count,len (newSrin) ): 
  Bolwer[arr]=newSrin[count]
  arr=arr+1
  count=count+1
 return Bolwer


def getPatLastRec(stringToProcess):
 newSrin=stringToProcess.split('-')
 PatLastRec=['0','Las','REC']
 PatLastRec[0]=newSrin[2]
 count=0
 LastWiIndex=0
 RecIndex=0
 for kk in newSrin:
  if kk == "Last wkt: ":
   LastWiIndex=count
  if kk == "Recent balls: ":
   RecIndex=count
  count=count+1
 LastWi=''
 for i in range (LastWiIndex+1,RecIndex):
  LastWi=LastWi+newSrin[i]
 if ('Partnership:' in LastWi):
   LastWi=''
 PatLastRec[1]= LastWi
 PatLastRec[2]= newSrin[RecIndex+1]
 return PatLastRec

#def alertDesktop (summary,stringtodisplay):
# try :
#  notification.notify(
#     title=summary,
#     message=stringtodisplay,
#     app_name='CricketUpdate',
#                       )
# except Exception as e:
#  print ' Not able to alert desktop'
#  print e 


def alertDesktop (summary,stringtodisplay):
 try :
  Notify.init("CricketUpdate")
  notification = Notify.Notification.new(summary,stringtodisplay)
  notification.show()
 except Exception as e:
  print ' Not able to alert desktop'
  print e 


if __name__ == '__main__':
  MatchSummaryURL = getIndiaURL(args.team)
  if ( len (MatchSummaryURL) > 1):
     print MatchSummaryURL
  else :
     print 'No Live URL avalible for team ' +  args.team 
     sys.exit()
  CricketObject=getLiveScore(MatchSummaryURL)
  isMatchLiveNow (CricketObject,False)
  printCricketScore(CricketObject)
  count=0
  towaitSec=float (args.refreshtime)
  try:
   while IsMatchLive:
    print ( str (count * towaitSec) + ' Sec Live')
    CricketObjectInLopp=getLiveScore(MatchSummaryURL)
    printLiveCricketScore(CricketObjectInLopp)
    isMatchLiveNow(CricketObjectInLopp,True)
    time.sleep( towaitSec )
    if (CompareCricketObjects(CricketObject,CricketObjectInLopp)):
     CricketObject=CricketObjectInLopp
     print 'SWAPPED'
    count=count+1
  except KeyboardInterrupt :
    print 'Stopping'
    sys.exit()
