#!/bin/python


#import urllib,urllib2,cookielib,re,time,json,requests

import  json,requests,bs4



session_requests = requests.session()
configJson=json.load(open('config.json'))

googleResultCount=configJson['googleResultCount']
googleKey=configJson['googleKey']
gooelcx=configJson['gooelcx']
googleURLend=configJson['googleURLend']

proxyDict = {
  "http" : configJson['proxyserver'] ,
  "https":configJson['proxyserver'],
}


torrentsite=configJson['torrentsite']
malayalamFroum=configJson['malayalamFroum']
language=configJson['language']


def getLKD():
 LKD=".we"
 with open ("domain.txt", "r") as myfile:
   LKD = myfile.read()
 print "From history domain name is "+LKD.strip()
 return LKD.strip()


def saveLKD(LKD):
  filepnr=open("domain.txt", 'w+')
  filepnr.write(LKD)
  filepnr.close()      

def getFromGoogleAPI(LKD):

  pnr_data =                 {

                            'q'      : torrentsite+LKD,
                        'googleHost' : 'google.co.in',
                            'num' :  googleResultCount,
                            'key'    : googleKey,
                            'cx'     : gooelcx
                              }
  url="https://www.googleapis.com/customsearch/v1"
  result = session_requests.get(url,params=pnr_data,proxies=proxyDict)
  results = json.loads(result.content)
#print results
  try:
     data = results['items']
     URLS=[]
     for kk in data:
        print kk['link']
        URLS.append(kk['link'])
     return URLS 
  except Exception as e: 
     print e
     return False

def getFrommGoogle(LKD):
    pnr_data =                 {


                            'q'      : torrentsite+LKD,
                            'gws_rd' : "cr"
                              }
   
    url="https://www.google.co.in/search"
    result = session_requests.get(url,params=pnr_data,proxies=proxyDict)
    #print result.content
    soup = bs4.BeautifulSoup(result.content,"lxml")
    #with open ("result.html", "r") as myfile:
    #   LKD = myfile.read()
    #soup =   bs4.BeautifulSoup(LKD,"lxml") 
    hrf=soup.find_all('a', href=True)
    URLS=[]
    for kk in hrf:
      url1 = kk['href']
      if  url1.startswith("/url?q="):
           url2=url1.split("http")[-1]
           url3=url2.split(googleURLend)[0]
           URLS.append("http"+url3)
    return URLS


def verifyURLS(URLS):
  domainName=[]
  for URL in URLS:
    if URL.startswith("http://"+torrentsite):
       fg=URL.split(".")[0]
       secon=URL.split(".")[1].split("/")[0]
       domainName.append(fg+"."+secon)
  domainName=list (set  (domainName))
  print domainName
  for URL in domainName:
    if  verifyDNS(URL):
      return URL
  return False
       
def verifyDNS(dns):
      goodURL=False
      try :
          print ("Trying with "+dns)
          result = session_requests.get(dns,proxies=proxyDict)
          if "Malayalam" in result.content:
            print "GoodURL URL" 
            goodURL=True
          else:
            print"Blocked"  
      except Exception as e:
          print e
      return goodURL 


def getMalayalamThreads(URL):
  URL=URL+malayalamFroum
  result = session_requests.get(URL,proxies=proxyDict)
  soup = bs4.BeautifulSoup(result.content,"lxml")
  #table  = soup.find_all("div", "ipsBox")
  table= soup.find_all("td","col_f_content ")
  #print "PRINT tables"
  links=[]
  movieDistEmpty={"Name":"","Links":links}
  ListofmovieDist=[]
  ListofmovieDist.append(movieDistEmpty)
  for k in table:
         spanchec = k.find_all("span","ipsBadge ipsBadge_green")
         if spanchec:
           continue
         subt =  k.find_all("a","topic_title")
         #print subt
         for kk in subt:
             #print kk['href'] + "  " + kk['title']
             movieLink=kk['href']
             movieName=kk['title'].split(language)[0]
             #print ( movieName +"-->"+movieLink)
             index=searchinList(ListofmovieDist,movieName)
             if index:
               #print ("Same Moview"+movieName+" "+movieLink)
               ListofmovieDist[index]['Links'].append(movieLink)
             else:
                #print "New movie found  "+movieName + "  "+movieLink
                #movieDist["Name"]= movieName
                #movieDist["Links"]=[movieLink]
                movieDist=createMovieDist(movieName,movieLink)
                ListofmovieDist.append(movieDist)
  del ListofmovieDist[0]
  return      ListofmovieDist
               
             
def createMovieDist(Name,link):
     links=[link]
     movieDist={"Name":Name,"Links":links}     
     return   movieDist   

def searchinList(ListtoSearch,movieName):
   index=0
   for kk in ListtoSearch:
      #print (movieName + "-->"+kk['Name'])
      if movieName == kk['Name']:
        return index
      index=index+1  
   return False     
   
def searchinArray (key,currentList):
   for kk in currentList:
     #print kk +" --" +key
     if kk in key:
        #print "TRUEE MATCH"
        return True
   return False   
          
def compareAndSave (movieList):
   ListtoAdd=[]
   currentList=[]
   with open ("movie.txt") as engfin:
     for line in engfin:
                  if line.startswith('#'):
                           continue
                  currentList.append(line.strip())
     for kk in  movieList:                     
         index=searchinArray(kk['Name'],currentList)
         if not index:
            #print "New movie "+kk['Name'] 
            ListtoAdd.append(kk['Name'])
            printNewMovie(kk) 
   currentList=currentList+ ListtoAdd
   print "New Movies " + str (ListtoAdd)
   filepnr=open("movie.txt", 'w+')
   for st in  currentList:
       filepnr.write(st+"\n")
     #print st
   filepnr.close()        


def printNewMovie(MovieDist):
   print ("^^^^^^^^^^^^^^^^^^^^^^^^^^^")
   print ("New Movie found "+ MovieDist["Name"]  + "\nDownload Link" )
   for kk in MovieDist["Links"]:
     print kk
   print ("***************************")
           
if __name__ == '__main__':
 #movieList=readThreads()
 #compareAndSave(movieList)
 #exit(0)
 LKD=getLKD()                   ## LKD -> Last Know domain 
 URL="http://"+torrentsite+"."+LKD
 if verifyDNS(URL):
   print "Cache looks fine "+URL
 else:
     print "Will search in google using API"  
     URLS=getFromGoogleAPI(LKD)
     if not URLS:
        print "Google API is failed , Scrapping from google.com"  
        URLS=getFrommGoogle(LKD)
     validDomain=verifyURLS(URLS)
     if validDomain:
             print "working domain "+validDomain
             URL=validDomain
             LKD=URL.split(".")[1]
             saveLKD(LKD)
     else:
        print"None of the URL from google search works . Try with different Key words"  
        exit(0)
 print "will do things with "+    URL+malayalamFroum
 movieList=getMalayalamThreads(URL)  
 compareAndSave(movieList)
