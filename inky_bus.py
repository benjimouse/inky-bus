import requests
from datetime import datetime, timezone
from dateutil.parser import parser, isoparse
from PIL import Image, ImageFont, ImageDraw
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from inky import InkyPHAT


def get_bus_time():
    resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
    if resp.status_code != 200:
        raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    
    reRunTime = isoparse(sortedArrival[0]['timeToLive'])
    print('{}'.format(reRunTime))
    arrivals = ""
    for bus in sortedArrival:
        if isoparse(bus['timeToLive']) < reRunTime:
            reRunTime = isoparse(bus['timeToLive'])
            

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
       # print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
        #print('time to live {}'.format(isoparse(bus['timeToLive'])))
        arrivals = arrivals + '{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'

    return arrivals

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.RED)
scale_size = 1
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(HankenGroteskBold, int(10 * scale_size))

message = get_bus_time()
#Display at top left
x = 0
y = 0

draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()





print  (get_bus_time())