#! /usr/bin/env python

import re
import urllib
import time
import smtplib
import difflib

sender = 'xxx@local'
receiver = ['Xxx@gmail.com']

keywords = ["mercedes", "BMW"]    # multiple entries like 'BMW+2009+545'
min = '&minAsk=19000'
max = '&maxAsk=27000'

# &srchType=T means Title only, and =A means entire post.

maxtime = 24*3600
timestart = time.time()

cities = ["boston", "southcoast", "worcester","providence", "newlondon"]

while (time.time()-timestart < maxtime):
    msg = "Hi, Welcome to use AutoPriceChecker! \n\n"
    newresult = []
    for city in cities :
        for keyword in keywords :
            url = "http://" + city + ".craigslist.org/search/cto?query=" + keyword + "&srchType=T"+min+max
            # print url
            page = urllib.urlopen(url)
                        
            line = page.readline()
            line2 = ' '
                        
            while (line != '') and (line2 != ''):
                # m = re.search('\s*(Mar  ?\d{1,2})', line)
                m = re.search('\s*([A-Za-z]+  ?\d{1,2}) - \<a href=\"(http:\/\/[a-z]+\.craigslist\.org\/[a-z]+\/?[a-z]*\/[0-9]{10}\.html)\"\>[\w\s]*(200[3-8])[A-Za-z !\*]*(([eEsS]|[Cc][Ll][Kk]?) ?(500|350))[A-Za-z !\*]*', line)
                if m:
                    line2 = page.readline()
                    mm = re.search('\s*(\$[0-9]+)\<', line2)
  
                    # m2 = re.search('\.html\"\>([A-Za-z !\$\*\/])-\<\/a\>', line)
                    # if m2:
                    #	print m2.group(1)
                    if mm:
                        newresult.append(mm.group(1)+'  '+m.group(3)+'  ' +keyword+'  '+ m.group(4)+'\tposted on '+m.group(1)+'  :  '+m.group(2)+'\n' )
                        # print line
                                
                m = re.search('\s*([A-Za-z]+  ?\d{1,2}) - \<a href=\"(http:\/\/[a-z]+\.craigslist\.org\/[a-z]+\/?[a-z]*\/[0-9]{10}\.html)\"\>[\w\s]*(200[3-8])[A-Za-z !\*]*((530|545) ?(i|xi))[A-Za-z !\*]*', line)
                if m:
                    line2 = page.readline()
                    mm = re.search('\s*(\$[0-9]+)\<', line2)
                    if mm:
                        newresult.append(mm.group(1) + '  '+  m.group(3) + '  ' +keyword +'  ' +m.group(4) + '\tposted on ' + m.group(1) + '  :  ' +  m.group(2)+'\n' )
                                
                        line = page.readline()
        
    history = open('history.txt', 'r')
    oldresult = []
    h = history.readline()
    while h != '':
        oldresult.append(h)
        h = history.readline()
        difference = difflib.Differ()
        difflist = list(difference.compare(newresult, oldresult))
        flag = 0
        for atlist in difflist:
            if atlist[0] == '-':
                msg += atlist[2:]
                flag = 1
        history.close()
        
        if flag == 1:
            newhistory = open('history.txt', 'w')
                for newh in newresult :
                    print >> newhistory, newh
                
                msg +='Searched on '+time.asctime()+'\n'
                sub = 'New car found'
                
                message = "From: xxx <xxx@local> \r\nTo: XXX <XXX@gmail.com>\r\nSubject: %s \r\n \n%s " % (sub, msg)
                
                s = smtplib.SMTP('localhost')
                s.sendmail(sender, receiver, message)
                print "Successfully sent email."
                s.quit()
                
    time.sleep(1800) # in seconds


print 'Done: maxtime is up.', time.asctime()

