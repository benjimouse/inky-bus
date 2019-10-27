import requests
import argparse
from time import sleep
from datetime import datetime, timezone, date, timedelta
from dateutil.parser import parser, isoparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--type', '-t', type=str, required=True, choices=["inky", "print"], help="Display to inky or to cmd line")
args = argParser.parse_args()


def get_bus_time():
    resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
    if resp.status_code != 200:
        raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    
    reRunTime = isoparse(sortedArrival[0]['timeToLive'])
    print('{}'.format(reRunTime))
    arrivals = []
    for bus in sortedArrival:
        if isoparse(bus['timeToLive']) < reRunTime:
            reRunTime = isoparse(bus['timeToLive'])
            
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
    message = 'Last Check = {}\n'.format(datetime.now().strftime('%H:%M:%S'))
    for bus in arrivals:

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
        message = message + '{} {:02d}m{:02d}s {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'
    
    return message

def displayOnInky():
    from PIL import Image, ImageFont, ImageDraw
    from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
    from font_intuitive import Intuitive
    from inky import InkyPHAT

    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.RED)
    scale_size = 1
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(HankenGroteskBold, int(90 / (len(busTimes)+1)))
    message = formatMessage(busTimes)
    
    #Display at top left
    x = 0
    y = 0

    draw.text((x, y), message, inky_display.RED, font)
    inky_display.set_image(img)
    inky_display.show()

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
        print ('Num busses = {}'.format(len(busTimes)))
        print  (formatMessage(busTimes))
        if args.type == "inky":
            displayOnInky()
        timeToSleep = abs((reRunTime - datetime.now(timezone.utc)).seconds)+1
        timeToSleep = maxSleep if maxSleep < timeToSleep else timeToSleep
    else:
        print('times not changed')
        timeToSleep = maxSleep
    sleep(timeToSleep)
else:
    print('Ended')