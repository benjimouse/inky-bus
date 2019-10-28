import requests
import argparse
from time import sleep
from datetime import datetime, timezone, date, timedelta
from dateutil.parser import parser, isoparse
argParser = argparse.ArgumentParser()
argParser.add_argument('--inky', '-i', type=str, required=False, choices=["true", "false"], default="false", help="Display to inky default false")
argParser.add_argument('--cmd', '-c', type=str, required=False, choices=["true", "false"], default="true", help="Display to command line default true")
args = argParser.parse_args()    

def get_bus_time():
    resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
    if resp.status_code != 200:
        if args.cmd=='true':
            print('Failed - {}'.format(resp.status_code))
            print('{}'.format(resp.text))
        # I'll assume that if this is failing that there's a timeout issue
        sleep(60)

    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    arrivals = []
    for bus in sortedArrival:
        bus_arrival = {}
        bus_arrival['timeToStation'] = bus['timeToStation']
        bus_arrival['lineName'] = bus['lineName']
        bus_arrival['ttl'] = isoparse(bus['timeToLive'])
        bus_arrival['destinationName'] = bus['destinationName']
        arrivals.append(bus_arrival)

    return arrivals

def formatMessage(arrivals):
    message = ''
    for bus in arrivals:

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
        message = message + '{} {:02d}m{:02d}s {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'
    
    return message

def displayOnInky(busTimes):
    from PIL import Image, ImageFont, ImageDraw
    from font_anonymous_pro import AnonymousProRegular
    from inky import InkyPHAT

    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.RED)
    scale_size = 1
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    lastCheckSize = 15
    lastCheckFont = ImageFont.truetype(AnonymousProRegular, lastCheckSize)
    lastCheckMessage = '{}\n'.format(datetime.now(timezone.utc).strftime('%H:%M:%S'))
    messageFont = ImageFont.truetype(AnonymousProRegular, int(78 / (len(busTimes))))
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
    print('{}\n'.format(datetime.now(timezone.utc).strftime('%H:%M:%S')))
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
    busTimes = get_bus_time()
    if oldTimes != busTimes and len(busTimes) >0 :
        oldTimes = busTimes
        reRunTime = busTimes[0]['ttl']
        for bus in busTimes:
            if bus['ttl'] < reRunTime:
                reRunTime = bus['ttl']
        if args.cmd == "true":
            displayOnCmd(busTimes)
        if args.inky == "true":
            displayOnInky(busTimes)
        timeToSleep = abs((reRunTime - datetime.now(timezone.utc)).seconds)+1
        timeToSleep = maxSleep if maxSleep < timeToSleep else timeToSleep
    else:
        if args.cmd == "true":
            print('No change')
        timeToSleep = maxSleep
    sleep(timeToSleep)
else:
    print('Ended')