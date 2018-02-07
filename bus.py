import hashlib
import datetime
from datetime import time
import urllib, json
from urllib.request import urlopen
# Edit busconfig.py file to change configuration
from busconfig import *

now = datetime.datetime.now()
nowTime = now.time()
Time = now.strftime("%Y%m%d%H")
UpdateTime = now.strftime("%H:%M")
TimeStamp = now.strftime("%Y-%m-%d %H:%M")

# Only run if App set to be on - this is useful if using something else like crontab to scehdule the app
if busAppOn=="Y":
        if nowTime >= timeStart and nowTime <= timeEnd:
            # convert API key into correct format
            h = hashlib.new('md5')
            h.update(Key.encode())
            h.update(Time.encode())
            AppKey = h.hexdigest()

            url="http://ws.mybustracker.co.uk/?module=json&key="+AppKey+"&function=getBusTimes&stopId="+busStop

            with urllib.request.urlopen(url) as url:
                JSONdata=json.loads(url.read().decode())
            
            data_list=JSONdata['busTimes']

            busList=[]
            for service in JSONdata['busTimes']:
                    for bus in service['timeDatas']:
                        busList.append([service['mnemoService'],bus['minutes']]) 

            # Sort buses by length of time until next one, ignore buses in 5 minutes or less, or over 2 hours. Only show first 6.
            busListFilter = sorted(i for i in busList if i[1]>5 and i[1]<120)
            busListSorted=sorted(busListFilter, key=lambda x: x[1])
            busListTrim = (busListSorted[:6])
            
            # Write to an html file - this is to pick up the output for use in another App
            with open("bustimes.htm", "w") as output:
                output.write("Bus            Minutes\n")
                output.write('\n'.join('{:<15} {:>6}'.format(x[0],x[1]) for x in busListTrim))
                output.write('\n' +' \n' + 'Updated ' + UpdateTime+ '\n')
            print(TimeStamp + " " + str(busListTrim))
        else:
            print(TimeStamp + " outwith time period")
else:
    print("App is switched off")
 