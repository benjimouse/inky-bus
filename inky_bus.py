import requests
import argparse
from time import sleep
from datetime import datetime, timezone, date, timedelta
from dateutil.parser import parser, isoparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--type', '-t', type=str, required=True, choices=["inky", "print"], help="Display to inky or to cmd line")
args = argParser.parse_args()

_lastCheck = datetime.now()

    

def get_bus_time():
    resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
    if resp.status_code != 200:
        raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    _lastCheck = datetime.now()
    arrivals = []
    for bus in sortedArrival:
            
       # print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
        #print('time to live {}'.format(isoparse(bus['timeToLive'])))
        bus_arrival = {}
        bus_arrival['timeToStation'] = bus['timeToStation']
        bus_arrival['lineName'] = bus['lineName']
        bus_arrival['ttl'] = isoparse(bus['timeToLive'])
        bus_arrival['destinationName'] = bus['destinationName']
        arrivals.append(bus_arrival)
       # arrivals = arrivals + '{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'

    return arrivals

def formatMessage(arrivals):
    #message = '{}\n'.format(datetime.now().strftime('%H:%M:%S'))
    message = ''
    for bus in arrivals:

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
        message = message + '{} {:02d}m{:02d}s {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'
    
    return message

def displayOnInky(busTimes):
    from PIL import Image, ImageFont, ImageDraw
    from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
    from font_fredoka_one import FredokaOne
    from inky import InkyPHAT

    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.RED)
    scale_size = 1
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    lastCheckSize = 15
    lastCheckFont = ImageFont.truetype(FredokaOne, lastCheckSize)
    lastCheckMessage = '{}\n'.format(_lastCheck.strftime('%H:%M:%S'))
    messageFont = ImageFont.truetype(FredokaOne, int(78 / (len(busTimes))))
    message = formatMessage(busTimes)
    
    #Display at top left
    x = 0
    y = 0
    draw.text((x, y), lastCheckMessage, inky_display.RED, lastCheckFont)
    draw.text((x, y+lastCheckSize), message, inky_display.BLACK, messageFont)
    inky_display.set_image(img)
    inky_display.show()

def displayOnCmd(busTimes):
    print('**************\n')
    print('{}\n'.format(_lastCheck.strftime('%H:%M:%S')))
    print ('Num busses = {}'.format(len(busTimes)))
    print(formatMessage(busTimes))
    print('**************\n')


# Run only if I need to 
today = datetime.now(timezone.utc)
one_day = timedelta(days=1)
yesterday = today - one_day

reRunTime = yesterday
oldTimes = []
maxSleep = 20

while True:
    print ('getting times')
    busTimes = get_bus_time()
    if oldTimes != busTimes:
        print('times changed')
        oldTimes = busTimes
        reRunTime = busTimes[0]['ttl']
        for bus in busTimes:
            if bus['ttl'] < reRunTime:
                reRunTime = bus['ttl']
        displayOnCmd(busTimes)
        if args.type == "inky":
            displayOnInky(busTimes)
        timeToSleep = abs((reRunTime - datetime.now(timezone.utc)).seconds)+1
        timeToSleep = maxSleep if maxSleep < timeToSleep else timeToSleep
    else:
        print('times not changed')
        timeToSleep = maxSleep
    sleep(timeToSleep)
else:
    print('Ended')