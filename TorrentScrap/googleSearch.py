#!/bin/python
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


def getFromGoogleAPI(keyword):

  pnr_data =                 {

                            'q'      : keyword,
                        'googleHost' : 'google.co.in',
                            'num' :  googleResultCount,
                            'key'    : googleKey,
                            'cx'     : gooelcx
                              }
  url="https://www.googleapis.com/customsearch/v1"
  result = session_requests.get(url,params=pnr_data,proxies=proxyDict)
  results = json.loads(result.content)
  data = results['items']
  URLS=[]
  for kk in data:
    print kk['link']
    URLS.append(kk['link'])
  return URLS 


def getFrommGoogle(keyword):
    pnr_data =                 {


                            'q'      : keyword,
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
    print URLS

def simpleUCM():
  url="http://10.184.36.144:16471/cs/idcplg?IdcService=GET_SEARCH_RESULTS&SortField=dInDate&SortOrder=Desc&ResultCount=20&QueryText="
  result = session_requests.get(url,proxies=proxyDict)
  print result.content

 
if __name__ == '__main__':
 #URLS=getGoogleData("malayalam")
 #print URLS
 #getFrommGoogle("Ajith lv")
 simpleUCM()
