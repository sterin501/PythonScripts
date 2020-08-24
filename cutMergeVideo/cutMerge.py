#!/bin/python

import time,subprocess

## ffmpeg -i 2.mkv -ss 00:10:03.500 -to 00:20:08.500 -async 1 cut.mp4 -y
## ffmpeg -i "concat:input1|input2" -codec copy output

#subprocess.Popen("pwd", shell=True)

processList=[]

def creatCutCommad(inputfile,time1,time2,outputfile):
    return "ffmpeg -i "+inputfile+"  -ss "+time1+ "  -to "+time2+"  -async 1   "+ outputfile+" -y"

def runCommand(comand):
        print "running __________________________________"+comand
        subprocess.Popen(comand+" ; echo '1' >> done ",shell=True,stdout=subprocess.PIPE)




if __name__ == '__main__':
    #print creatCutCommad("2.mkv","00:10:03.500","00:20:08.500","cut.mp4")
    filename="details.txt"
    temp=[]
    comands=[]
    part=0
    paS=""

    with open (filename) as engfin:
        for line in engfin:
           if line.startswith('#'):
                 continue
           else:
                cc=line.split()
                comands.append(creatCutCommad(cc[0],cc[1],cc[2],"part"+str(part)+".mp4")    )
                paS=paS+"file part"+str(part)+".mp4\n"
                part=part+1

    f = open("mylist.txt", "w")
    f.write(paS)
    ca='ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4'
    #comands.append(ca)
    #print comands
    f = open("done", "w")
    f.write("")

    for kk in comands:
        runCommand(kk)
    while True:
        print "checking cut job  status\n\n\n "
        time.sleep (2)
        num_lines = sum(1 for line in open('done'))
        print "number of lines " + str (num_lines)
        print "part " + str (part)
        if num_lines == part:
            runCommand(ca)
            break
